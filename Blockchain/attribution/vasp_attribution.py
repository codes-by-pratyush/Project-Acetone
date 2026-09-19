from typing import Any


# ============================================================
# PUBLIC / DEMO VASP ADDRESS DIRECTORY
# ============================================================
#
# This is intentionally kept separate from the tracing engine.
# In the real system, these entries can later come from a
# verified public attribution dataset.
#
# Addresses here are DEMONSTRATION placeholders, not claims
# about real exchange ownership.
# ============================================================

KNOWN_VASP_ADDRESSES = {
    "0xexchange00000000000000000000000000000001": {
        "vasp": "Demo Exchange",
        "label": "Known Exchange Deposit Address",
        "source": "demo_dataset",
    },
}


# ============================================================
# ADDRESS NORMALIZATION
# ============================================================

def normalize_address(address: str) -> str:
    """
    Normalize an Ethereum address for comparison.
    """

    if not address:
        return ""

    return address.strip().lower()


# ============================================================
# DIRECT ADDRESS LOOKUP
# ============================================================

def lookup_vasp(address: str) -> dict[str, Any] | None:
    """
    Look up a wallet in the known VASP address directory.

    Returns None when the address is not present.
    """

    normalized_address = normalize_address(address)

    if not normalized_address:
        return None

    match = KNOWN_VASP_ADDRESSES.get(
        normalized_address
    )

    if match is None:
        return None

    return {
        "address": normalized_address,
        "vasp": match["vasp"],
        "label": match["label"],
        "source": match["source"],
    }


# ============================================================
# TRACE PATH ATTRIBUTION
# ============================================================

def attribute_trace_path(path: dict[str, Any]) -> dict[str, Any]:
    """
    Attribute the destination of a traced fund-flow path.

    The final wallet in the trace is checked against the
    known VASP address directory.

    Attribution is expressed as a confidence value rather
    than absolute certainty.
    """

    wallets = path.get("wallets") or []

    if not wallets:
        return {
            "attributed": False,
            "vasp": None,
            "confidence": 0.0,
            "matched_address": None,
            "evidence": [],
        }

    destination = normalize_address(
        wallets[-1]
    )

    match = lookup_vasp(destination)

    if match is None:
        return {
            "attributed": False,
            "vasp": None,
            "confidence": 0.0,
            "matched_address": destination,
            "evidence": [
                "Destination address was not found "
                "in the known VASP address directory."
            ],
        }

    hops = path.get("hops", len(wallets) - 1)

    evidence = [
        "Destination address matched a known "
        "VASP attribution entry.",
        f"Fund-flow trace reached the matched address "
        f"after {hops} hop(s).",
    ]

    # Start with strong confidence for a direct known-address
    # match, then reduce confidence as the tracing depth grows.
    confidence = 0.90

    if hops >= 5:
        confidence = 0.70
    elif hops >= 3:
        confidence = 0.80

    return {
        "attributed": True,
        "vasp": match["vasp"],
        "confidence": confidence,
        "matched_address": destination,
        "label": match["label"],
        "source": match["source"],
        "evidence": evidence,
    }


# ============================================================
# COMPLETE TRACE ATTRIBUTION
# ============================================================

def attribute_trace(paths: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Attribute all paths returned by the fund-flow tracer.

    The result keeps every path's attribution so the API/UI
    can later show investigators the evidence behind each
    possible destination.
    """

    results = []

    for path in paths:
        results.append(
            {
                "path": path,
                "attribution": attribute_trace_path(path),
            }
        )

    attributed_results = [
        result
        for result in results
        if result["attribution"]["attributed"]
    ]

    if attributed_results:
        best_result = max(
            attributed_results,
            key=lambda result: result["attribution"]["confidence"],
        )

        overall = {
            "attributed": True,
            "vasp": best_result["attribution"]["vasp"],
            "confidence": best_result["attribution"]["confidence"],
            "matched_address": best_result["attribution"][
                "matched_address"
            ],
        }
    else:
        overall = {
            "attributed": False,
            "vasp": None,
            "confidence": 0.0,
            "matched_address": None,
        }

    return {
        "overall": overall,
        "paths": results,
    }