from Blockchain.playbook.investigation_report import (
    build_investigation_report,
)


def test_investigation_report():
    wallet = (
        "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    )

    trace_result = [
        {
            "wallets": [
                wallet.lower(),
                "0xdddddddddddddddddddddddddddddddddddddddd",
                "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            ],
            "transactions": [],
            "hops": 2,
        }
    ]

    risk_result = {
        "score": 20,
        "signals": {
            "new_wallet": True,
            "round_number_transfer": True,
        },
        "evidence": [
            {
                "rule": "new_wallet",
                "points": 10,
            },
            {
                "rule": "round_number_transfer",
                "points": 10,
            },
        ],
    }

    attribution_result = {
        "overall": {
            "attributed": False,
            "vasp": None,
            "confidence": 0.0,
            "matched_address": None,
        },
        "paths": [],
    }

    playbook_result = {
        "evidence": [
            {
                "type": "fund_flow",
                "path_id": 1,
            }
        ],
        "recommendations": [
            "Preserve relevant evidence."
        ],
    }

    report = build_investigation_report(
        wallet,
        trace_result,
        risk_result,
        attribution_result,
        playbook_result,
    )

    assert report["report_type"] == (
        "blockchain_investigation"
    )

    assert report["wallet"] == wallet.lower()

    assert report["summary"]["trace_paths"] == 1

    assert report["summary"]["risk_score"] == 20

    assert report["summary"]["attributed"] is False

    assert report["summary"][
        "attribution_confidence"
    ] == 0.0

    assert len(report["trace"]["paths"]) == 1

    assert report["risk_analysis"]["score"] == 20

    assert len(report["evidence"]) == 1

    assert len(report["recommendations"]) == 1