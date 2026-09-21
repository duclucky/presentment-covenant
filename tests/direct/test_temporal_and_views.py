import hashlib

from .conftest import SOURCE_BYTES, activate, address_text, deploy_contract, present, valid_invoice


def deploy_with_final_adjudication_deadline(
    direct_deploy, direct_alice, direct_bob
):
    return direct_deploy(
        "contracts/presentment_covenant.py",
        "PC-DEADLINE-REGRESSION",
        address_text(direct_alice),
        address_text(direct_bob),
        "2026-01-01T00:00:10Z",
        "2026-01-01T00:00:20Z",
        "2026-01-01T00:01:00Z",
        "2026-01-01T00:00:30Z",
        "2026-01-01T00:00:40Z",
        "2026-01-01T00:00:50Z",
    )


def submit_regression_presentation(
    contract, direct_vm, direct_bob, direct_alice, presentation_id
):
    invoice = valid_invoice(direct_alice, direct_bob).replace(
        "PC-DEMO-001", "PC-DEADLINE-REGRESSION"
    )
    direct_vm.sender = direct_bob
    contract.submit_presentation(
        presentation_id,
        "INV-PC-001",
        invoice,
        hashlib.sha256(invoice.encode()).hexdigest(),
    )


def test_activation_exact_deadline_is_late(
    direct_vm, direct_deploy, direct_owner, direct_alice, direct_bob
):
    contract = deploy_contract(direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_owner
    direct_vm.value = 2 * 10**18
    direct_vm.warp("2026-01-01T00:00:10Z")
    with direct_vm.expect_revert("activation deadline passed"):
        contract.activate_credit()
    assert contract.get_credit()["state"] == "DRAFT"
    assert contract.get_accounting()["liability"] == 0


def test_duplicate_presentation_is_rejected(
    direct_vm, direct_deploy, direct_owner, direct_alice, direct_bob
):
    contract = deploy_contract(direct_deploy, direct_alice, direct_bob)
    activate(contract, direct_vm, direct_owner)
    present(contract, direct_vm, direct_bob, direct_alice)
    with direct_vm.expect_revert("presentation state is not open"):
        present(contract, direct_vm, direct_bob, direct_alice)


def test_unauthorized_waiver_and_close_are_rejected(
    direct_vm, direct_deploy, direct_owner, direct_alice, direct_bob
):
    contract = deploy_contract(direct_deploy, direct_alice, direct_bob)
    activate(contract, direct_vm, direct_owner)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only applicant"):
        contract.waive_discrepancies()
    with direct_vm.expect_revert("only issuer"):
        contract.close_credit()


def test_cure_accepted_near_cure_deadline_remains_adjudicable(
    direct_vm, direct_deploy, direct_owner, direct_alice, direct_bob
):
    contract = deploy_with_final_adjudication_deadline(
        direct_deploy, direct_alice, direct_bob
    )
    activate(contract, direct_vm, direct_owner)
    submit_regression_presentation(
        contract, direct_vm, direct_bob, direct_alice, "PRES-ORIGINAL"
    )
    direct_vm.mock_web(r".*dcsaorg.*", {"status": 200, "body": SOURCE_BYTES})
    direct_vm.mock_llm(
        r".*SOURCE_DATA_START.*",
        '{"status":"DISCREPANT","covered_document_ids":["dcsa-ebl","beneficiary-invoice"],"discrepancy_codes":["CROSS_DOCUMENT_CONFLICT"],"reason":"bounded conflict"}',
    )
    direct_vm.warp("2026-01-01T00:00:21Z")
    contract.adjudicate()
    assert contract.get_credit()["state"] == "DISCREPANT_OPEN"

    direct_vm.warp("2026-01-01T00:00:39Z")
    submit_regression_presentation(
        contract, direct_vm, direct_bob, direct_alice, "PRES-CURE"
    )
    direct_vm.clear_mocks()
    direct_vm.mock_web(r".*dcsaorg.*", {"status": 200, "body": b"tampered"})
    direct_vm.warp("2026-01-01T00:00:41Z")
    contract.adjudicate()
    assert contract.get_attempt()["attempt_nonce"] == 2
    assert contract.get_credit()["state"] == "UNVERIFIABLE_OPEN"


def test_retry_accepted_near_retry_deadline_remains_adjudicable(
    direct_vm, direct_deploy, direct_owner, direct_alice, direct_bob
):
    contract = deploy_with_final_adjudication_deadline(
        direct_deploy, direct_alice, direct_bob
    )
    activate(contract, direct_vm, direct_owner)
    submit_regression_presentation(
        contract, direct_vm, direct_bob, direct_alice, "PRES-ORIGINAL"
    )
    direct_vm.mock_web(r".*dcsaorg.*", {"status": 200, "body": b"tampered"})
    direct_vm.warp("2026-01-01T00:00:21Z")
    contract.adjudicate()
    assert contract.get_credit()["state"] == "UNVERIFIABLE_OPEN"

    direct_vm.sender = direct_bob
    direct_vm.warp("2026-01-01T00:00:49Z")
    contract.retry_unverifiable()
    direct_vm.warp("2026-01-01T00:00:51Z")
    contract.adjudicate()
    assert contract.get_attempt()["attempt_nonce"] == 2
    assert contract.get_credit()["state"] == "UNVERIFIABLE_OPEN"
