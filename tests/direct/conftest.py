import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

# genlayer-test 0.29.2 duplicates the message temp file onto fd 0 and unlinks
# it immediately. Windows keeps that handle open, so the otherwise unrelated
# loader raises WinError 32 before a contract is imported. Keep this narrow
# test-only compatibility shim; it ignores only that exact temporary-file case.
_loader_unlink = os.unlink


def _unlink_loader_temp(path, *, dir_fd=None):
    try:
        if dir_fd is None:
            _loader_unlink(path)
        else:
            _loader_unlink(path, dir_fd=dir_fd)
    except PermissionError:
        if os.name != "nt" or "\\Temp\\tmp" not in str(path):
            raise


os.unlink = _unlink_loader_temp


ROOT = Path(__file__).resolve().parents[2]
SOURCE_BYTES = (ROOT / "fixtures" / "ebl-api-3.0.0-negotiable-bl.json").read_bytes()
SOURCE_DIGEST = hashlib.sha256(SOURCE_BYTES).hexdigest()


@pytest.fixture(autouse=True)
def reset_vm_clock(direct_vm):
    # The plugin reuses a VM context in a session; each test must start before
    # the activation deadline so temporal assertions remain independent.
    original_warp = direct_vm.warp

    def synchronized_warp(timestamp):
        original_warp(timestamp)
        gl = sys.modules.get("genlayer.gl")
        if gl is not None and getattr(gl, "message_raw", None) is not None:
            gl.message_raw["datetime"] = timestamp

    direct_vm.warp = synchronized_warp
    synchronized_warp("2026-01-01T00:00:01Z")
    direct_vm.value = 0


def deadlines():
    return (
        "2026-01-01T00:00:10Z",
        "2026-01-01T00:00:20Z",
        "2026-01-01T00:00:30Z",
        "2026-01-01T00:00:40Z",
        "2026-01-01T00:00:50Z",
        "2026-01-01T00:01:00Z",
    )


def address_text(value):
    if isinstance(value, bytes):
        return "0x" + value.hex()
    return str(value)


def deploy_contract(direct_deploy, direct_alice, direct_bob):
    return direct_deploy(
        "contracts/presentment_covenant.py",
        "PC-DEMO-001",
        address_text(direct_alice),
        address_text(direct_bob),
        *deadlines(),
    )


def valid_invoice(direct_alice, direct_bob):
    return json.dumps(
        {
            "invoice_id": "INV-PC-001",
            "credit_id": "PC-DEMO-001",
            "beneficiary": address_text(direct_bob),
            "applicant": address_text(direct_alice),
            "amount_gen": 2,
            "currency": "GEN",
            "goods_description": "Refined Soybean Oil",
        },
        sort_keys=True,
    )


def present(contract, direct_vm, direct_bob, direct_alice, invoice=None):
    if invoice is None:
        invoice = valid_invoice(direct_alice, direct_bob)
    direct_vm.sender = direct_bob
    contract.submit_presentation(
        "PRES-001",
        "INV-PC-001",
        invoice,
        hashlib.sha256(invoice.encode()).hexdigest(),
    )


def activate(contract, direct_vm, direct_owner):
    direct_vm.warp("2026-01-01T00:00:01Z")
    direct_vm.sender = direct_owner
    direct_vm.value = 2 * 10**18
    contract.activate_credit()
    direct_vm.value = 0
