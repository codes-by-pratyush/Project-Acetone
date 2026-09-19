from Blockchain.tasks.celery_app import celery_app
from Blockchain.tracing.fund_flow import trace_funds
from Blockchain.risk.risk_engine import calculate_wallet_risk


def make_json_serializable(value):
    """
    Convert Neo4j DateTime objects and nested structures
    into JSON-serializable Python values.
    """

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
    """
    Run fund-flow tracing and risk analysis for a wallet
    in the background using Celery.
    """

    wallet_address = wallet_address.strip()

    trace_result = trace_funds(
        wallet_address,
        max_hops=6,
        min_amount_pct=10.0,
        max_nodes=1000,
    )

    risk_result = calculate_wallet_risk(wallet_address)

    result = {
        "wallet": wallet_address.lower(),
        "trace": trace_result,
        "risk": risk_result,
    }

    return make_json_serializable(result)