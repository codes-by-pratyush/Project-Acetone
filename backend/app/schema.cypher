// ==========================================
// T-M4-03: Acetone Neo4j Graph Database Schema
// ==========================================

// 1. Uniqueness Constraints (Fast O(1) Lookup & Deduplication)
CREATE CONSTRAINT unique_wallet_address IF NOT EXISTS
FOR (w:Wallet) REQUIRE w.address IS UNIQUE;

CREATE CONSTRAINT unique_tx_hash IF NOT EXISTS
FOR (t:Transaction) REQUIRE t.tx_hash IS UNIQUE;

CREATE CONSTRAINT unique_vasp_name IF NOT EXISTS
FOR (v:VASP) REQUIRE v.name IS UNIQUE;

// 2. Performance Indexes for Range and Tracing Queries
CREATE INDEX idx_wallet_cluster IF NOT EXISTS
FOR (w:Wallet) ON (w.cluster_id);

CREATE INDEX idx_tx_timestamp IF NOT EXISTS
FOR (t:Transaction) ON (t.timestamp);

CREATE INDEX idx_tx_chain IF NOT EXISTS
FOR (t:Transaction) ON (t.chain);

// 3. Schema Documentation Nodes (Model Reference)
// Nodes:
// (:Wallet {address: STRING, cluster_id: STRING, risk_score: FLOAT, is_vasp: BOOLEAN})
// (:Transaction {tx_hash: STRING, amount: FLOAT, asset: STRING, timestamp: INTEGER, chain: STRING, fee: FLOAT})
// (:VASP {name: STRING, vasp_type: STRING, risk_rating: STRING, jurisdiction: STRING})

// Core Relationships:
// (:Wallet)-[:SENT {tx_hash: STRING, amount: FLOAT, timestamp: INTEGER}]->(:Transaction)
// (:Transaction)-[:RECEIVED_BY {amount: FLOAT, timestamp: INTEGER}]->(:Wallet)
// (:Wallet)-[:CONTROLLED_BY]->(:VASP)