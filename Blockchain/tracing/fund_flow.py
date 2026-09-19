from heapq import heappush, heappop
from itertools import count
from time import monotonic

from Blockchain.storage.neo4j_store import driver


TRACE_CHAIN = "sepolia"


def get_outgoing_transactions(wallet_address):
    """
    Get outgoing transactions from a wallet.

    Wallet address matching is case-insensitive because Ethereum
    addresses may be represented using different letter casing.
    """

    query = """
    MATCH (wallet:Wallet)
    WHERE toLower(wallet.address) = $wallet_address
      AND wallet.chain = $chain

    MATCH (wallet)-[tx:SENT]->(destination:Wallet)

    RETURN
        destination.address AS to_address,
        tx.hash AS hash,
        tx.amount AS amount,
        tx.asset AS asset,
        tx.timestamp AS timestamp,
        tx.fee AS fee
    """

    with driver.session() as session:
        result = session.run(
            query,
            wallet_address=wallet_address.lower(),
            chain=TRACE_CHAIN,
        )

        transactions = []

        for record in result:
            transactions.append(
                {
                    "to_address": record["to_address"],
                    "hash": record["hash"],
                    "amount": record["amount"],
                    "asset": record["asset"],
                    "timestamp": record["timestamp"],
                    "fee": record["fee"],
                }
            )

        return transactions


def _build_path(wallets, transactions):
    """
    Convert the current traversal state into the
    machine-readable path format used by the rest of M3.
    """

    return {
        "wallets": wallets,
        "transactions": transactions,
        "hops": len(transactions),
    }


def trace_funds(
    start_wallet,
    max_hops=6,
    min_amount_pct=10.0,
    max_nodes=1000,
    max_seconds=5.0,
):
    """
    Trace outgoing fund flow using bounded priority BFS.

    Traversal behavior:

    - max_hops limits investigation depth.
    - min_amount_pct applies amount-decay pruning.
    - max_nodes limits the number of unique wallet nodes
      expanded during one trace.
    - max_seconds prevents an unexpectedly large graph from
      consuming the worker indefinitely.
    - cycles are prevented within each individual path.
    - higher-value transactions are explored first within
      the same hop depth.

    Returns:
        list[dict]: Machine-readable fund-flow paths.
    """

    start_wallet = start_wallet.strip().lower()

    max_hops = max(1, int(max_hops))
    min_amount_pct = max(0.0, float(min_amount_pct))
    max_nodes = max(1, int(max_nodes))
    max_seconds = max(0.1, float(max_seconds))

    start_time = monotonic()

    queue = []
    sequence = count()

    heappush(
        queue,
        (
            0,
            float("-inf"),
            next(sequence),
            start_wallet,
            [start_wallet],
            [],
            {start_wallet},
        ),
    )

    paths = []

    expanded_wallets = set()

    timed_out = False

    while queue:

        # -----------------------------------------------------
        # Time budget
        # -----------------------------------------------------

        if monotonic() - start_time >= max_seconds:
            timed_out = True

            while queue:
                (
                    _queued_hops,
                    _queued_priority,
                    _queued_sequence,
                    _queued_wallet,
                    queued_wallets,
                    queued_transactions,
                    _queued_visited,
                ) = heappop(queue)

                if queued_transactions:
                    paths.append(
                        _build_path(
                            queued_wallets,
                            queued_transactions,
                        )
                    )

            break

        (
            hops,
            _priority,
            _sequence,
            current_wallet,
            wallets,
            transactions,
            visited,
        ) = heappop(queue)

        # -----------------------------------------------------
        # Hop limit
        # -----------------------------------------------------

        if hops >= max_hops:
            if transactions:
                paths.append(
                    _build_path(
                        wallets,
                        transactions,
                    )
                )

            continue

        # -----------------------------------------------------
        # Prevent expanding the same wallet repeatedly
        # -----------------------------------------------------

        if current_wallet in expanded_wallets:
            if transactions:
                paths.append(
                    _build_path(
                        wallets,
                        transactions,
                    )
                )

            continue

        # -----------------------------------------------------
        # Node budget
        # -----------------------------------------------------

        if len(expanded_wallets) >= max_nodes:

            if transactions:
                paths.append(
                    _build_path(
                        wallets,
                        transactions,
                    )
                )

            while queue:
                (
                    _queued_hops,
                    _queued_priority,
                    _queued_sequence,
                    _queued_wallet,
                    queued_wallets,
                    queued_transactions,
                    _queued_visited,
                ) = heappop(queue)

                if queued_transactions:
                    paths.append(
                        _build_path(
                            queued_wallets,
                            queued_transactions,
                        )
                    )

            break

        expanded_wallets.add(current_wallet)

        # -----------------------------------------------------
        # Read outgoing transactions
        # -----------------------------------------------------

        outgoing = get_outgoing_transactions(
            current_wallet
        )

        outgoing.sort(
            key=lambda tx: tx.get("amount") or 0,
            reverse=True,
        )

        if not outgoing:
            if transactions:
                paths.append(
                    _build_path(
                        wallets,
                        transactions,
                    )
                )

            continue

        extended = False

        for transaction in outgoing:

            # -------------------------------------------------
            # Time budget
            # -------------------------------------------------

            if monotonic() - start_time >= max_seconds:
                timed_out = True
                break

            amount = transaction.get("amount")

            # Ignore malformed or non-positive transfers.
            if amount is None or amount <= 0:
                continue

            # -------------------------------------------------
            # Amount-decay pruning
            # -------------------------------------------------

            if transactions:

                previous_amount = transactions[-1].get(
                    "amount"
                )

                if (
                    previous_amount is None
                    or previous_amount <= 0
                ):
                    continue

                minimum_amount = previous_amount * (
                    min_amount_pct / 100.0
                )

                if amount < minimum_amount:
                    continue

            next_wallet = transaction.get(
                "to_address"
            )

            if not next_wallet:
                continue

            next_wallet = next_wallet.lower()

            # -------------------------------------------------
            # Cycle prevention
            # -------------------------------------------------

            if next_wallet in visited:
                continue

            # -------------------------------------------------
            # Create next traversal state
            # -------------------------------------------------

            new_wallets = wallets + [
                next_wallet
            ]

            new_transactions = transactions + [
                transaction
            ]

            new_visited = visited | {
                next_wallet
            }

            extended = True

            heappush(
                queue,
                (
                    hops + 1,
                    -float(amount),
                    next(sequence),
                    next_wallet,
                    new_wallets,
                    new_transactions,
                    new_visited,
                ),
            )

        # -----------------------------------------------------
        # Timeout while processing transactions
        # -----------------------------------------------------

        if timed_out:

            if transactions:
                paths.append(
                    _build_path(
                        wallets,
                        transactions,
                    )
                )

            while queue:
                (
                    _queued_hops,
                    _queued_priority,
                    _queued_sequence,
                    _queued_wallet,
                    queued_wallets,
                    queued_transactions,
                    _queued_visited,
                ) = heappop(queue)

                if queued_transactions:
                    paths.append(
                        _build_path(
                            queued_wallets,
                            queued_transactions,
                        )
                    )

            break

        # -----------------------------------------------------
        # Dead-end path
        # -----------------------------------------------------

        if not extended and transactions:
            paths.append(
                _build_path(
                    wallets,
                    transactions,
                )
            )

    return paths