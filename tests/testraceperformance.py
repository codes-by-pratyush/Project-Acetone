import time

from Blockchain.storage.neo4j_store import driver
from Blockchain.tracing.fund_flow import trace_funds


def clear_performance_test_data():
    query = """
    MATCH (wallet:Wallet)
    WHERE wallet.chain = 'sepolia'
      AND wallet.address STARTS WITH '0xPERF'
    DETACH DELETE wallet
    """

    with driver.session() as session:
        session.run(query)


def create_branching_graph():
    query = """
    MERGE (root:Wallet {
        address: '0xPERF_ROOT',
        chain: 'sepolia'
    })

    WITH root

    UNWIND range(1, 10) AS branch
    MERGE (level1:Wallet {
        address: '0xPERF_L1_' + toString(branch),
        chain: 'sepolia'
    })

    MERGE (root)-[tx1:SENT {
        hash: '0xPERF_TX_L1_' + toString(branch)
    }]->(level1)

    SET tx1.amount = 10.0,
        tx1.asset = 'ETH',
        tx1.timestamp = '2026-09-19T10:00:00+00:00',
        tx1.fee = 0.001

    WITH level1, branch

    UNWIND range(1, 10) AS child
    MERGE (level2:Wallet {
        address:
            '0xPERF_L2_' + toString(branch) + '_' + toString(child),
        chain: 'sepolia'
    })

    MERGE (level1)-[tx2:SENT {
        hash:
            '0xPERF_TX_L2_' + toString(branch) + '_' + toString(child)
    }]->(level2)

    SET tx2.amount = 9.0,
        tx2.asset = 'ETH',
        tx2.timestamp = '2026-09-19T10:01:00+00:00',
        tx2.fee = 0.001
    """

    with driver.session() as session:
        session.run(query)


def test_trace_branching_performance():
    clear_performance_test_data()
    create_branching_graph()

    start = time.perf_counter()

    paths = trace_funds(
        '0xPERF_ROOT',
        max_hops=2,
        min_amount_pct=10.0,
        max_nodes=1000,
        max_seconds=10.0,
    )

    elapsed = time.perf_counter() - start

    print("\n=== TRACE BRANCHING PERFORMANCE TEST ===")
    print("Paths found:", len(paths))
    print("Elapsed seconds:", round(elapsed, 4))

    assert len(paths) == 100
    assert elapsed < 10.0

    clear_performance_test_data()