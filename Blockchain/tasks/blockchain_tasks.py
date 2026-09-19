from Blockchain.tasks.celery_app import celery_app
from Blockchain.tracing.fund_flow import trace_funds
from Blockchain.risk.risk_engine import calculate_wallet_risk
from Blockchain.attribution.vasp_attribution import attribute_trace


def make_json_serializable(value):
    if isinstance(value, dict):
        return {
            key: make_json_serializable(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            make_json_serializable(item)
            for item in value
        ]

    if hasattr(value, "iso_format"):
        return value.iso_format()

    return value


@celery_app.task
def analyze_wallet(wallet_address):
    wallet_address = wallet_address.strip()

    # TRACE
    trace_result = trace_funds(
        wallet_address,
        max_hops=6,
        min_amount_pct=10.0,
        max_nodes=1000,
    )

    # ANALYZE
    risk_result = calculate_wallet_risk(wallet_address)

    # ATTRIBUTE
    attribution_result = attribute_trace(trace_result)

    result = {
        "wallet": wallet_address.lower(),
        "trace": trace_result,
        "risk": risk_result,
        "attribution": attribution_result,
    }

    return make_json_serializable(result)