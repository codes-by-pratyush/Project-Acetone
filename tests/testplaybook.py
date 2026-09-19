from Blockchain.playbook.investigation_playbook import (
    build_investigation_playbook,
)


def test_playbook_unknown_vasp():
    trace_result = [
        {
            "wallets": [
                "0xffffffffffffffffffffffffffffffffffffffff",
                "0xdddddddddddddddddddddddddddddddddddddddd",
                "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            ],
            "transactions": [
                {
                    "to_address": "0xDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
                    "hash": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "amount": 8.0,
                    "asset": "ETH",
                    "timestamp": "2026-09-18T11:01:00+00:00",
                    "fee": 0.001,
                },
                {
                    "to_address": "0xEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",
                    "hash": "0xdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
                    "amount": 9.0,
                    "asset": "ETH",
                    "timestamp": "2026-09-18T11:03:00+00:00",
                    "fee": 0.001,
                },
            ],
            "hops": 2,
        }
    ]

    risk_result = {
        "wallet": "0xffffffffffffffffffffffffffffffffffffffff",
        "score": 20,
        "evidence": [
            {
                "rule": "new_wallet",
                "description": "Wallet has a short observed transaction history.",
                "points": 10,
            },
            {
                "rule": "round_number_transfer",
                "description": "Wallet was involved in a round-number transfer.",
                "points": 10,
            },
        ],
    }

    attribution_result = {
        "overall": {
            "attributed": False,
            "vasp": None,
            "confidence": 0.0,
            "matched_address": (
                "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
            ),
        }
    }

    result = build_investigation_playbook(
        "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        trace_result,
        risk_result,
        attribution_result,
    )

    print("\n=== PLAYBOOK UNKNOWN VASP TEST ===")
    print(result)

    assert result["wallet"] == (
        "0xffffffffffffffffffffffffffffffffffffffff"
    )

    assert result["summary"]["trace_paths"] == 1
    assert result["summary"]["risk_score"] == 20
    assert result["summary"]["attributed"] is False
    assert result["summary"]["vasp"] is None
    assert result["summary"]["attribution_confidence"] == 0.0

    assert len(result["evidence"]) == 4
    assert len(result["recommendations"]) >= 2


def test_playbook_known_vasp():
    trace_result = [
        {
            "wallets": [
                "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "0xexchange00000000000000000000000000000001",
            ],
            "transactions": [],
            "hops": 1,
        }
    ]

    risk_result = {
        "wallet": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "score": 45,
        "evidence": [
            {
                "rule": "rapid_forwarding",
                "description": "Funds moved rapidly.",
                "points": 25,
            },
            {
                "rule": "new_wallet",
                "description": "Wallet has a short observed history.",
                "points": 10,
            },
            {
                "rule": "round_number_transfer",
                "description": "Round-number transfer detected.",
                "points": 10,
            },
        ],
    }

    attribution_result = {
        "overall": {
            "attributed": True,
            "vasp": "Demo Exchange",
            "confidence": 0.90,
            "matched_address": (
                "0xexchange00000000000000000000000000000001"
            ),
        }
    }

    result = build_investigation_playbook(
        "0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        trace_result,
        risk_result,
        attribution_result,
    )

    print("\n=== PLAYBOOK KNOWN VASP TEST ===")
    print(result)

    assert result["summary"]["trace_paths"] == 1
    assert result["summary"]["risk_score"] == 45
    assert result["summary"]["attributed"] is True
    assert result["summary"]["vasp"] == "Demo Exchange"
    assert result["summary"]["attribution_confidence"] == 0.90

    assert len(result["evidence"]) == 5

    assert any(
        item["type"] == "vasp_attribution"
        for item in result["evidence"]
    )


if __name__ == "__main__":
    test_playbook_unknown_vasp()
    test_playbook_known_vasp()