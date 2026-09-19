from typing import Any


def build_investigation_report(
    wallet: str,
    trace_result: list[dict[str, Any]],
    risk_result: dict[str, Any],
    attribution_result: dict[str, Any],
    playbook_result: dict[str, Any],
) -> dict[str, Any]:
    wallet = wallet.strip().lower()

    attribution = attribution_result.get(
        "overall",
        {},
    )

    return {
        "report_type": "blockchain_investigation",
        "wallet": wallet,

        "summary": {
            "trace_paths": len(trace_result),
            "risk_score": risk_result.get(
                "score",
                0,
            ),
            "attributed": attribution.get(
                "attributed",
                False,
            ),
            "vasp": attribution.get(
                "vasp"
            ),
            "attribution_confidence": attribution.get(
                "confidence",
                0.0,
            ),
        },

        "trace": {
            "paths": trace_result,
        },

        "risk_analysis": {
            "score": risk_result.get(
                "score",
                0,
            ),
            "signals": risk_result.get(
                "signals",
                {},
            ),
            "evidence": risk_result.get(
                "evidence",
                [],
            ),
        },

        "attribution": attribution_result,

        "evidence": playbook_result.get(
            "evidence",
            [],
        ),

        "recommendations": playbook_result.get(
            "recommendations",
            [],
        ),
    }