"""Resumable, sanitized Studionet deployment and bounded lifecycle demo.

This script never prints or stores private keys, raw receipts, validator config,
stdout, stderr, or traces. It records only an allowlist of canonical status and
view fields. A finalized UNVERIFIABLE/DISCREPANT result is evidence, not a
reason to replay the adjudication write.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from genlayer_py import create_account, create_client, studionet
from genlayer_py.types.transactions import TransactionStatus


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "presentment_covenant.py"
EVIDENCE_DIR = ROOT / "docs" / "evidence" / "studionet"
EVIDENCE = EVIDENCE_DIR / "deployment.json"
CHECKPOINT = EVIDENCE_DIR / "deployment-checkpoint.json"
RPC = studionet.rpc_urls["default"]["http"][0]
CHAIN_ID = int(studionet.id)
EXPLORER = "https://explorer-studio.genlayer.com"
DEPENDS = "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6"
PAYOUT_WEI = 2 * 10**18
APPLICANT_FALLBACK = "0x017d13fe11263159470130ec1f2f96879e8fd40c"


def load_env() -> dict[str, str]:
    """Load the project .env first, then the nearest authorized parent .env."""
    candidates: list[Path] = []
    current = ROOT
    while True:
        candidates.append(current / ".env")
        if current.parent == current:
            break
        current = current.parent
    merged: dict[str, str] = {}
    for path in reversed(candidates):
        if not path.exists():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() and value.strip() and key.strip() not in merged:
                merged[key.strip()] = value.strip().strip('"').strip("'")
    # Project values override parent values.
    for path in candidates:
        if not path.exists():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() and value.strip():
                merged[key.strip()] = value.strip().strip('"').strip("'")
    return merged


def require_key(env: dict[str, str], name: str) -> str:
    value = env.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing authorized environment variable: {name}")
    return value


def json_safe(value: Any) -> Any:
    if isinstance(value, (bytes, bytearray)):
        return "0x" + bytes(value).hex()
    if isinstance(value, int):
        return value
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if hasattr(value, "hex") and not isinstance(value, str):
        try:
            return value.hex()
        except Exception:
            pass
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_hash() -> str:
    return hashlib.sha256(CONTRACT.read_bytes()).hexdigest()


def safe_receipt(tx: dict[str, Any], operation: str) -> dict[str, Any]:
    consensus = tx.get("consensus_data") or {}
    votes = consensus.get("votes") or {}
    counts = Counter(str(v).lower() for v in votes.values())
    leaders = consensus.get("leader_receipt") or []
    execution_results = [str(item.get("execution_result")) for item in leaders if isinstance(item, dict) and item.get("execution_result")]
    leader_execution_result = execution_results[0] if execution_results else "UNKNOWN"
    data = tx.get("data") or {}
    return {
        "operation": operation,
        "transaction_hash": str(tx.get("hash", "")),
        "status": str(tx.get("status_name", "UNKNOWN")),
        "result": str(tx.get("result_name", "UNKNOWN")),
        "leader_execution_result": leader_execution_result,
        "additional_execution_results": execution_results[1:],
        "vote_counts": dict(sorted(counts.items())),
        "contract_address": data.get("contract_address"),
        "finalized_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def wait_finalized(client: Any, tx_hash: str, operation: str) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = client.wait_for_transaction_receipt(
        tx_hash,
        status=TransactionStatus.FINALIZED,
        interval=5000,
        retries=120,
        full_transaction=True,
    )
    tx = json_safe(client.get_transaction(tx_hash))
    safe = safe_receipt(tx, operation)
    if safe["status"] != "FINALIZED":
        raise RuntimeError(f"{operation} did not finalize")
    return safe, tx


def read_views(client: Any, address: str, beneficiary: str, issuer: str) -> dict[str, Any]:
    def read(name: str, args: list[Any] | None = None) -> Any:
        return json_safe(client.read_contract(address, name, args=args or []))

    return {
        "credit": read("get_credit"),
        "accounting": read("get_accounting"),
        "presentation": read("get_presentation"),
        "attempt": read("get_attempt"),
        "discrepancies": read("get_discrepancies"),
        "beneficiary_withdrawable_wei": read("get_withdrawable", [beneficiary]),
        "issuer_withdrawable_wei": read("get_withdrawable", [issuer]),
    }


def submit_step(client: Any, account: Any, address: str, operation: str, method: str, args: list[Any], value: int = 0) -> dict[str, Any]:
    existing: dict[str, Any] = {}
    if CHECKPOINT.exists():
        loaded = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        if loaded.get("operation") == operation and loaded.get("source_sha256") == source_hash():
            existing = loaded
    tx_hash = existing.get("transaction_hash")
    if not tx_hash:
        tx_hash = str(client.write_contract(address, method, account=account, args=args, value=value))
        write_json(
            CHECKPOINT,
            {
                "operation": operation,
                "transaction_hash": tx_hash,
                "status": "SUBMITTED",
                "source_sha256": source_hash(),
                "network": "studionet",
                "chain_id": CHAIN_ID,
                "submitted_at_utc": datetime.now(timezone.utc).isoformat(),
            },
        )
    safe, _ = wait_finalized(client, tx_hash, operation)
    write_json(CHECKPOINT, {**safe, "source_sha256": source_hash(), "network": "studionet", "chain_id": CHAIN_ID})
    if safe["leader_execution_result"] != "SUCCESS":
        raise RuntimeError(f"{operation} finalized without successful execution")
    return safe


def main() -> int:
    env = load_env()
    issuer = create_account(require_key(env, "STUDIONET_PRIVATE_KEY"))
    beneficiary = create_account(require_key(env, "STUDIONET_INTEGRATOR_PRIVATE_KEY"))
    issuer_address = issuer.address
    beneficiary_address = beneficiary.address
    if issuer_address.lower() == beneficiary_address.lower():
        raise RuntimeError("issuer and beneficiary must be distinct")

    client = create_client(chain=studionet, endpoint=RPC, account=issuer)
    current_source_hash = source_hash()
    existing = json.loads(EVIDENCE.read_text(encoding="utf-8")) if EVIDENCE.exists() else {}
    if existing.get("contract_address") and existing.get("source_sha256") != current_source_hash:
        archive = EVIDENCE_DIR / f"deployment-archive-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
        EVIDENCE.rename(archive)
        existing = {}

    address = existing.get("contract_address")
    credit_id = existing.get("credit_id")
    applicant = existing.get("applicant", APPLICANT_FALLBACK)
    if not address:
        checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8")) if CHECKPOINT.exists() else {}
        if checkpoint.get("operation") == "deploy" and checkpoint.get("source_sha256") == current_source_hash:
            tx_hash = checkpoint.get("transaction_hash")
        else:
            tx_hash = None

        now = datetime.now(timezone.utc)
        deadlines = [
            (now + timedelta(minutes=30)).isoformat().replace("+00:00", "Z"),
            (now + timedelta(minutes=45)).isoformat().replace("+00:00", "Z"),
            (now + timedelta(minutes=90)).isoformat().replace("+00:00", "Z"),
            (now + timedelta(minutes=120)).isoformat().replace("+00:00", "Z"),
            (now + timedelta(minutes=150)).isoformat().replace("+00:00", "Z"),
            (now + timedelta(minutes=180)).isoformat().replace("+00:00", "Z"),
        ]
        credit_id = f"PC-{now.strftime('%Y%m%dT%H%M%SZ')}"
        if not tx_hash:
            args = [credit_id, applicant, beneficiary_address, *deadlines]
            tx_hash = str(client.deploy_contract(CONTRACT.read_bytes(), account=issuer, args=args))
            write_json(
                CHECKPOINT,
                {
                    "operation": "deploy",
                    "transaction_hash": tx_hash,
                    "status": "SUBMITTED",
                    "source_sha256": current_source_hash,
                    "network": "studionet",
                    "chain_id": CHAIN_ID,
                    "issuer": issuer_address,
                    "beneficiary": beneficiary_address,
                    "credit_id": credit_id,
                    "submitted_at_utc": datetime.now(timezone.utc).isoformat(),
                },
            )
        deployment_receipt, tx = wait_finalized(client, tx_hash, "deploy")
        address = deployment_receipt.get("contract_address") or (tx.get("data") or {}).get("contract_address")
        if not isinstance(address, str) or len(address) != 42 or not address.lower().startswith("0x"):
            raise RuntimeError("finalized deployment did not expose a contract address")
        if deployment_receipt["leader_execution_result"] != "SUCCESS":
            write_json(EVIDENCE, {"status": "FINALIZED_FAILED", "deployment": deployment_receipt, "source_sha256": current_source_hash})
            raise RuntimeError("deployment finalized without successful execution")

        evidence = {
            "status": "DEPLOYED",
            "network": "studionet",
            "chain_id": CHAIN_ID,
            "rpc": RPC,
            "explorer": EXPLORER,
            "source_sha256": current_source_hash,
            "depends": DEPENDS,
            "contract_address": address,
            "contract_explorer": f"{EXPLORER}/contracts/{address}",
            "credit_id": credit_id,
            "issuer": issuer_address,
            "applicant": applicant,
            "beneficiary": beneficiary_address,
            "purse_wei": PAYOUT_WEI,
            "deployment": deployment_receipt,
            "transactions": {},
            "canonical_reads": {},
            "portal_submit_performed": False,
        }
        evidence["canonical_reads"]["after_deploy"] = json_safe(client.get_contract_schema(address))
        evidence["canonical_reads"]["state_after_deploy"] = read_views(client, address, beneficiary_address, issuer_address)
        write_json(EVIDENCE, evidence)
    else:
        evidence = existing

    def ensure_step(operation: str, account: Any, method: str, args: list[Any], value: int = 0) -> dict[str, Any]:
        existing_step = (evidence.get("transactions") or {}).get(operation)
        if existing_step and existing_step.get("status") == "FINALIZED":
            return existing_step
        record = submit_step(client, account, address, operation, method, args, value)
        evidence.setdefault("transactions", {})[operation] = record
        write_json(EVIDENCE, evidence)
        return record

    evidence.setdefault("transactions", {})
    evidence.setdefault("canonical_reads", {})
    evidence["transactions"]["activate_credit"] = ensure_step("activate_credit", issuer, "activate_credit", [], PAYOUT_WEI)
    evidence["canonical_reads"]["after_activation"] = read_views(client, address, beneficiary_address, issuer_address)
    write_json(EVIDENCE, evidence)

    invoice = {
        "invoice_id": "INV-PC-001",
        "credit_id": credit_id,
        "beneficiary": beneficiary_address,
        "applicant": applicant,
        "amount_gen": 2,
        "currency": "GEN",
        "goods_description": "Refined Soybean Oil",
    }
    invoice_bytes = json.dumps(invoice, sort_keys=True, separators=(",", ":"))
    invoice_digest = hashlib.sha256(invoice_bytes.encode("utf-8")).hexdigest()
    evidence["transactions"]["submit_presentation"] = ensure_step(
        "submit_presentation", beneficiary, "submit_presentation", ["PRES-001", "INV-PC-001", invoice_bytes, invoice_digest]
    )
    evidence["canonical_reads"]["after_presentation"] = read_views(client, address, beneficiary_address, issuer_address)
    write_json(EVIDENCE, evidence)

    evidence["transactions"]["adjudicate"] = ensure_step("adjudicate", issuer, "adjudicate", [])
    after_adjudication = read_views(client, address, beneficiary_address, issuer_address)
    evidence["canonical_reads"]["after_adjudication"] = after_adjudication
    state = (after_adjudication.get("credit") or {}).get("state")

    # Continue only from the finalized canonical state; never replay a write.
    if state == "COMPLIANT":
        evidence["transactions"]["withdraw"] = ensure_step("withdraw", beneficiary, "withdraw", [])
        evidence["canonical_reads"]["after_withdraw"] = read_views(client, address, beneficiary_address, issuer_address)
        evidence["transactions"]["close_credit"] = ensure_step("close_credit", issuer, "close_credit", [])
        evidence["canonical_reads"]["after_close"] = read_views(client, address, beneficiary_address, issuer_address)
        evidence["status"] = "LIFECYCLE_SUCCESS"
    else:
        evidence["status"] = "LIFECYCLE_FINALIZED_NON_CONSEQUENTIAL"
        evidence["resume_condition"] = "Fresh authoritative compatibility evidence is required before retrying UNVERIFIABLE; DISCREPANT requires applicant waiver or beneficiary cure within locked deadlines."

    write_json(EVIDENCE, evidence)
    CHECKPOINT.unlink(missing_ok=True)
    print(json.dumps({"status": evidence["status"], "contract_address": address, "state": state}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        # No exception text is printed: client errors can contain validator config.
        print(json.dumps({"status": "BLOCKED", "reason": "deployment_or_lifecycle_error", "error_type": type(exc).__name__}))
        raise SystemExit(1)
