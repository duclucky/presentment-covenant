from scripts.studionet_lifecycle import safe_receipt


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
