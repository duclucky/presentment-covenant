from scripts.studionet_lifecycle import canonical_lifecycle_status, safe_receipt


def test_primary_leader_receipt_wins_over_mismatched_normalized_result():
    transaction = {
        "hash": "0x01",
        "tx_execution_result_name": "ERROR",
        "result_name": "MAJORITY_AGREE",
        "lifecycle": {"state": "finalized"},
        "consensus_data": {
            "leader_receipt": [
                {"execution_result": "SUCCESS"},
                {"execution_result": "ERROR"},
            ],
            "votes": {"a": "agree", "b": "agree"},
        },
    }

    parsed = safe_receipt(transaction, "adjudicate")

    assert parsed["leader_execution_result"] == "SUCCESS"
    assert parsed["normalized_execution_result"] == "ERROR"
    assert parsed["additional_execution_results"] == ["ERROR"]
    assert parsed["status"] == "FINALIZED"


def test_closed_zero_liability_resume_is_lifecycle_success():
    views = {
        "credit": {"state": "CLOSED"},
        "accounting": {
            "zero_liability": True,
            "total_withdrawn": 2 * 10**18,
        },
        "beneficiary_withdrawable_wei": 0,
        "issuer_withdrawable_wei": 0,
    }

    assert canonical_lifecycle_status(views) == "LIFECYCLE_SUCCESS"


def test_closed_with_liability_is_blocked():
    views = {
        "credit": {"state": "CLOSED"},
        "accounting": {
            "zero_liability": False,
            "total_withdrawn": 0,
        },
        "beneficiary_withdrawable_wei": 2 * 10**18,
        "issuer_withdrawable_wei": 0,
    }

    assert canonical_lifecycle_status(views) == "INVALID_TERMINAL_ACCOUNTING"
