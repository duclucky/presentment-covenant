from .conftest import activate, deploy_contract, present


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
