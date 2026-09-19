from Blockchain.tasks.celery_app import celery_app
from Blockchain.tracing.fund_flow import trace_funds
from Blockchain.risk.risk_engine import calculate_wallet_risk
from Blockchain.attribution.vasp_attribution import attribute_trace
from Blockchain.playbook.investigation_playbook import (
    build_investigation_playbook,
)
from Blockchain.playbook.investigation_report import (
    build_investigation_report,
)
from Blockchain.monitoring.monitor import WalletMonitor
from Blockchain.providers.ethereum import w3


# Shared monitor instance for the running worker process.
wallet_monitor = WalletMonitor()


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
    risk_result = calculate_wallet_risk(
        wallet_address
    )

    # ATTRIBUTE
    attribution_result = attribute_trace(
        trace_result
    )

    # PLAYBOOK
    playbook_result = build_investigation_playbook(
        wallet_address,
        trace_result,
        risk_result,
        attribution_result,
    )

    # REPORT
    report_result = build_investigation_report(
        wallet_address,
        trace_result,
        risk_result,
        attribution_result,
        playbook_result,
    )

    result = {
        "wallet": wallet_address.lower(),
        "trace": trace_result,
        "risk": risk_result,
        "attribution": attribution_result,
        "playbook": playbook_result,
        "report": report_result,
    }

    return make_json_serializable(
        result
    )


@celery_app.task
def poll_wallet(wallet_address):
    wallet_address = wallet_address.strip().lower()

    if not wallet_monitor.is_watched(
        wallet_address
    ):
        current_block = w3.eth.block_number

        wallet_monitor.add_wallet(
            wallet_address,
            start_block=current_block,
        )

        return {
            "wallet": wallet_address,
            "transfers_found": 0,
            "latest_block": current_block,
            "transfers": [],
            "status": "monitoring_initialized",
        }

    transfers, latest_block = (
        wallet_monitor.check_wallet(
            wallet_address
        )
    )

    return make_json_serializable(
        {
            "wallet": wallet_address,
            "transfers_found": len(transfers),
            "latest_block": latest_block,
            "transfers": transfers,
            "status": "poll_completed",
        }
    )


@celery_app.task
def poll_watched_wallets():
    wallets = (
        wallet_monitor.get_watched_wallets()
    )

    results = []

    for wallet_address in wallets:
        transfers, latest_block = (
            wallet_monitor.check_wallet(
                wallet_address
            )
        )

        results.append(
            {
                "wallet": wallet_address,
                "transfers_found": len(
                    transfers
                ),
                "latest_block": latest_block,
                "transfers": transfers,
                "status": "poll_completed",
            }
        )

    return make_json_serializable(
        results
    )