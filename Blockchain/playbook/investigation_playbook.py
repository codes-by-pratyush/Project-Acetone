from typing import Any


def _build_trace_evidence(trace_result: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evidence = []

    for path_index, path in enumerate(trace_result, start=1):
        wallets = path.get("wallets", [])
        transactions = path.get("transactions", [])
        hops = path.get("hops", len(wallets) - 1)

        evidence.append(
            {
                "type": "fund_flow",
                "path_id": path_index,
                "hops": hops,
                "wallets": wallets,
                "transactions": transactions,
            }
        )

    return evidence


def _build_risk_evidence(risk_result: dict[str, Any]) -> list[dict[str, Any]]:
    evidence = []

    for item in risk_result.get("evidence", []):
        evidence.append(
            {
                "type": "risk_signal",
                "rule": item.get("rule"),
                "description": item.get("description"),
                "points": item.get("points", 0),
                "details": {
                    key: value
                    for key, value in item.items()
                    if key not in {
                        "rule",
                        "description",
                        "points",
                    }
                },
            }
        )

    return evidence


def _build_attribution_evidence(
    attribution_result: dict[str, Any],
) -> list[dict[str, Any]]:
    evidence = []

    overall = attribution_result.get("overall", {})

    if overall.get("attributed"):
        evidence.append(
            {
                "type": "vasp_attribution",
                "vasp": overall.get("vasp"),
                "matched_address": overall.get("matched_address"),
                "confidence": overall.get("confidence", 0.0),
                "statement": (
                    "Destination address matched a known VASP "
                    "attribution entry."
                ),
            }
        )
    else:
        evidence.append(
            {
                "type": "vasp_attribution",
                "vasp": None,
                "matched_address": overall.get("matched_address"),
                "confidence": overall.get("confidence", 0.0),
                "statement": (
                    "No known VASP attribution was established "
                    "for the traced destination."
                ),
            }
        )

    return evidence


def _build_recommendations(
    risk_result: dict[str, Any],
    attribution_result: dict[str, Any],
) -> list[str]:
    recommendations = [
        "Preserve relevant transaction hashes, timestamps, "
        "amounts, and wallet addresses as investigation evidence."
    ]

    if risk_result.get("score", 0) > 0:
        recommendations.append(
            "Review the triggered risk signals and their supporting "
            "transaction evidence."
        )

    overall = attribution_result.get("overall", {})

    if overall.get("attributed"):
        recommendations.append(
            "Review the attributed VASP destination through the "
            "appropriate lawful investigative or reporting process."
        )
    else:
        recommendations.append(
            "Continue reviewing downstream transaction activity "
            "if additional tracing is warranted."
        )

    return recommendations


def build_investigation_playbook(
    wallet: str,
    trace_result: list[dict[str, Any]],
    risk_result: dict[str, Any],
    attribution_result: dict[str, Any],
) -> dict[str, Any]:
    wallet = wallet.strip().lower()

    trace_evidence = _build_trace_evidence(trace_result)
    risk_evidence = _build_risk_evidence(risk_result)
    attribution_evidence = _build_attribution_evidence(
        attribution_result
    )

    evidence = (
        trace_evidence
        + risk_evidence
        + attribution_evidence
    )

    overall_attribution = attribution_result.get("overall", {})

    return {
        "wallet": wallet,
        "summary": {
            "trace_paths": len(trace_result),
            "risk_score": risk_result.get("score", 0),
            "attributed": overall_attribution.get(
                "attributed",
                False,
            ),
            "vasp": overall_attribution.get("vasp"),
            "attribution_confidence": overall_attribution.get(
                "confidence",
                0.0,
            ),
        },
        "evidence": evidence,
        "recommendations": _build_recommendations(
            risk_result,
            attribution_result,
        ),
    }