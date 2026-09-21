import hashlib
import json
import os
import sys
import tempfile
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

# genlayer-test 0.30.0rc2 may leave the duplicated stdin handle positioned at
# EOF on Windows after preparing the GenVM message. Rewind only that injected
# handle before the contract SDK imports and decodes it.
from gltest.direct import loader as _direct_loader
from gltest.direct import wasi_mock as _wasi_mock

def _inject_and_rewind(vm):
    calldata = _direct_loader.import_calldata()
    Address = _direct_loader.import_address()
    message_data = {
        "contract_address": Address(vm._contract_address),
        "sender_address": Address(vm.sender),
        "origin_address": Address(vm.origin),
        "stack": [],
        "value": vm._value,
        "datetime": vm._datetime,
        "is_init": False,
        "chain_id": vm._chain_id,
        "entry_kind": 0,
        "entry_data": b"",
        "entry_stage_data": None,
    }
    encoded = calldata.encode(message_data)
    fd, path = tempfile.mkstemp()
    try:
        # Pytest can close stdin on Windows, allowing mkstemp() to reuse fd 0.
        # Move the temp file away from fd 0 before replacing stdin explicitly.
        if fd == 0:
            safe_fd = os.dup(fd)
            os.close(fd)
            fd = safe_fd
            vm._original_stdin_fd = None
        else:
            try:
                vm._original_stdin_fd = os.dup(0)
            except OSError:
                vm._original_stdin_fd = None
        os.write(fd, encoded)
        os.lseek(fd, 0, os.SEEK_SET)
        os.dup2(fd, 0)
    finally:
        os.close(fd)
        os.unlink(path)
    if os.name == "nt":
        import msvcrt

        msvcrt.setmode(0, os.O_BINARY)
    os.lseek(0, 0, os.SEEK_SET)


_direct_loader._inject_message_to_fd0 = _inject_and_rewind

# The v0.3 SDK decodes JSON-mode LLM responses from JSON text. The current
# direct harness eagerly parses mock JSON into a dict first, so put it back on
# the wire as text to match the runtime response shape.
_handle_llm_request = _wasi_mock._handle_llm_request


def _handle_llm_json_text(vm, data):
    response = _handle_llm_request(vm, data)
    if isinstance(response, dict) and isinstance(response.get("ok"), (dict, list)):
        response = {**response, "ok": json.dumps(response["ok"])}
    return response


_wasi_mock._handle_llm_request = _handle_llm_json_text


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
        message = sys.modules.get("genlayer.message")
        if message is not None and getattr(message, "raw", None) is not None:
            message.raw["datetime"] = timestamp

    direct_vm.warp = synchronized_warp
    synchronized_warp("2026-01-01T00:00:01Z")
    direct_vm.value = 0


def deadlines():
    return (
        "2026-01-01T00:00:10Z",
        "2026-01-01T00:00:20Z",
        "2026-01-01T00:01:00Z",
        "2026-01-01T00:00:40Z",
        "2026-01-01T00:00:50Z",
        "2026-01-01T00:00:55Z",
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
