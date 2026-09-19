from heapq import heappush, heappop

from Blockchain.storage.neo4j_store import driver


def get_outgoing_transactions(wallet_address):
    """
    Get outgoing transactions from a wallet.
    """

    query = """
    MATCH (wallet:Wallet {address: $wallet_address, chain: $chain})
          -[tx:SENT]->(destination:Wallet)
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
            chain="sepolia",
        )

        transactions = []

        for record in result:
            transactions.append({
                "to_address": record["to_address"],
                "hash": record["hash"],
                "amount": record["amount"],
                "asset": record["asset"],
                "timestamp": record["timestamp"],
                "fee": record["fee"],
            })

        return transactions


def trace_funds(
    start_wallet,
    max_hops=6,
    min_amount_pct=10.0,
    max_nodes=1000,
):
    """
    Trace outgoing fund flow using priority-ordered BFS.

    Higher-value transactions are explored first.

    A transaction is followed only when its amount is at least
    min_amount_pct of the amount entering the current path.

    max_nodes limits how many destination wallet nodes can be
    expanded, preventing graph explosion.

    Already discovered paths are preserved even when the node
    budget is exhausted.
    """

    start_wallet = start_wallet.lower()

    max_hops = max(1, int(max_hops))
    min_amount_pct = float(min_amount_pct)
    max_nodes = max(1, int(max_nodes))

    queue = []

    heappush(
        queue,
        (
            0,
            float("-inf"),
            start_wallet,
            [start_wallet],
            [],
            {start_wallet},
        ),
    )

    paths = []
    expanded_nodes = 0

    while queue:

        (
            hops,
            priority,
            current_wallet,
            wallets,
            transactions,
            visited,
        ) = heappop(queue)

        # If this path has already reached the hop limit,
        # preserve it without expanding further.
        if hops >= max_hops:
            if transactions:
                paths.append({
                    "wallets": wallets,
                    "transactions": transactions,
                    "hops": len(transactions),
                })
            continue

        outgoing = get_outgoing_transactions(current_wallet)

        outgoing.sort(
            key=lambda tx: tx["amount"] or 0,
            reverse=True,
        )

        if not outgoing:
            if transactions:
                paths.append({
                    "wallets": wallets,
                    "transactions": transactions,
                    "hops": len(transactions),
                })
            continue

        extended = False

        for transaction in outgoing:

            amount = transaction["amount"]

            if amount is None or amount <= 0:
                continue

            # Apply amount-decay pruning.
            if transactions:
                previous_amount = transactions[-1]["amount"]

                minimum_amount = previous_amount * (
                    min_amount_pct / 100
                )

                if amount < minimum_amount:
                    continue

            next_wallet = transaction["to_address"].lower()

            # Prevent cycles such as A -> B -> A.
            if next_wallet in visited:
                continue

            # If expanding this destination would exceed the
            # node budget, preserve the current path instead
            # of exploring further.
            if expanded_nodes >= max_nodes:
                if transactions:
                    paths.append({
                        "wallets": wallets,
                        "transactions": transactions,
                        "hops": len(transactions),
                    })

                # Stop processing additional destinations from
                # this wallet because the global node budget
                # has been reached.
                break

            new_wallets = wallets + [next_wallet]
            new_transactions = transactions + [transaction]
            new_visited = visited | {next_wallet}

            expanded_nodes += 1
            extended = True

            heappush(
                queue,
                (
                    hops + 1,
                    -amount,
                    next_wallet,
                    new_wallets,
                    new_transactions,
                    new_visited,
                ),
            )

        # If nothing could be extended, preserve the current path.
        if not extended and transactions:
            paths.append({
                "wallets": wallets,
                "transactions": transactions,
                "hops": len(transactions),
            })

        # Once the global node budget has been reached,
        # remaining queued paths cannot be expanded.
        if expanded_nodes >= max_nodes:
            while queue:
                (
                    queued_hops,
                    queued_priority,
                    queued_wallet,
                    queued_wallets,
                    queued_transactions,
                    queued_visited,
                ) = heappop(queue)

                if queued_transactions:
                    paths.append({
                        "wallets": queued_wallets,
                        "transactions": queued_transactions,
                        "hops": len(queued_transactions),
                    })

            break

    return paths