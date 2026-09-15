# Project Acetone — Requirements

**SIH Problem Statement:** SIH26183
**Project Type:** Blockchain Forensics and Crypto-Fraud Investigation Assistance Platform
**Team Size:** 6 Members
**Document Owner:** Team Leader

---

## 1. Project Objective

Acetone is an investigator-assistance platform designed to help investigators analyze and trace suspicious cryptocurrency transactions.

The system follows funds from a victim-reported wallet, identifies suspicious transaction patterns using explainable rules, estimates the likely Virtual Asset Service Provider (VASP) destination, and generates an evidence-backed investigation report.

Acetone assists investigators. It does not replace human investigation or legal processes.

---

## 2. Target Users

The primary users are:

* Cybercrime investigators
* State cyber cells
* Supervisors
* Administrators
* Investigators working with NCRP/I4C-related workflows

---

## 3. Core Functional Requirements

### FR-01 — User Authentication

The system shall allow authorized users to securely log in.

The system shall support role-based access for:

* Investigator
* Supervisor
* Admin

---

### FR-02 — Case Creation

An investigator shall be able to create a case using a wallet address reported by a victim.

A case shall contain relevant information such as:

* Case ID
* Reported wallet address
* Blockchain/chain
* Case status
* Creation timestamp
* Associated evidence

---

### FR-03 — Wallet Monitoring

The system shall monitor a reported wallet for new transaction activity.

The MVP shall use near-real-time monitoring through blockchain data providers.

---

### FR-04 — Transaction Ingestion

The system shall retrieve blockchain transaction data from supported public blockchain data providers.

The initial primary blockchain target shall be Ethereum/Sepolia.

---

### FR-05 — Fund-Flow Tracing

The system shall trace cryptocurrency fund movement from the reported wallet across multiple transaction hops.

The MVP shall use bounded tracing with a default target of approximately 6–8 hops.

The tracing engine shall use:

* Breadth-First Search
* Priority-based processing
* Amount-decay pruning
* Node limits
* Time limits

---

### FR-06 — Transaction Graph

The system shall represent wallets as graph nodes and transactions as relationships between wallets.

Investigators shall be able to visually inspect the traced transaction network.

---

### FR-07 — Suspicious Pattern Detection

The system shall detect suspicious transaction patterns including:

* Fan-out / splitting
* Fan-in / consolidation
* Rapid forwarding
* High transaction velocity
* Large transfers to new wallets
* Other research-backed suspicious behaviours

---

### FR-08 — Explainable Fraud Scoring

The system shall calculate a risk score using explainable rules.

Each risk flag shall contain:

* Reason
* Weight
* Supporting transaction/evidence

The system shall not present the risk score as an autonomous determination of criminal activity.

---

### FR-09 — VASP Attribution

The system shall compare traced wallet addresses against publicly available labelled VASP/address datasets.

The system shall provide:

* Likely VASP
* Attribution confidence
* Supporting evidence
* Source of the address label

The result shall be presented as probabilistic attribution rather than identity confirmation.

---

### FR-10 — Investigator Playbook Mode

The system shall provide suggested next investigative actions based on the evidence discovered during tracing.

Suggestions shall remain within the applicable lawful investigative process.

---

### FR-11 — Alert Generation

The system shall generate an investigator alert when defined risk conditions are met.

Alerts shall contain:

* Case reference
* Risk level
* Triggering evidence
* Timestamp
* Recommended next action

---

### FR-12 — Mock NCRP/SAHYOG Integration

The system shall include a clearly labelled mock integration representing communication with an external government system.

The prototype shall not claim to have a real NCRP/SAHYOG connection.

All mock interactions shall clearly state:

**MOCK — NOT A REAL GOVERNMENT SYSTEM**

---

### FR-13 — Evidence Integrity

The system shall calculate a SHA-256 integrity hash for generated evidence/report content.

The system shall maintain an audit trail of relevant investigative actions.

---

### FR-14 — Report Generation

The system shall generate:

* PDF investigation reports
* Machine-readable JSON reports

Reports shall contain relevant case, transaction, risk, attribution, and evidence information.

---

## 4. Non-Functional Requirements

### NFR-01 — Performance

The tracing engine shall use configurable node and time limits to prevent graph explosion.

---

### NFR-02 — Security

The system shall implement:

* JWT authentication
* Role-based access control
* Input validation
* Rate limiting
* Secure secrets management
* Appropriate CORS configuration
* Security logging

---

### NFR-03 — Reliability

The system shall handle temporary blockchain-provider failures using:

* Retry mechanisms
* Provider fallback where available
* Cached responses
* Local fallback/demo data

---

### NFR-04 — Explainability

Important system outputs shall provide supporting evidence and reasons rather than presenting unexplained conclusions.

---

### NFR-05 — Auditability

Sensitive actions shall be recorded in an audit log containing information such as:

* User
* Action
* Case
* Timestamp

---

## 5. Technology Requirements

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy

### Frontend

* React
* TypeScript
* Vite
* TailwindCSS

### Databases

* PostgreSQL
* Neo4j
* Redis

### Background Processing

* Celery

### Blockchain Access

* Alchemy
* Etherscan
* web3.py

### Graph Visualization

* Cytoscape.js

### Reporting

* WeasyPrint

### Infrastructure

* Docker
* Docker Compose

---

## 6. MVP Scope

The following features are mandatory for the MVP:

* Case creation
* Wallet monitoring
* Transaction ingestion
* 6–8 hop fund tracing
* Graph visualization
* Fan-out/fan-in detection
* Explainable rule-based fraud scoring
* VASP attribution
* Investigator Playbook Mode
* Authentication and RBAC
* Alerts
* Evidence integrity hashing
* PDF/JSON reporting
* Mock NCRP/SAHYOG integration

---

## 7. Out of Scope

The prototype shall NOT:

* Identify the real-world identity of a wallet owner
* Freeze cryptocurrency funds
* Access private exchange databases
* Claim universal 20-hop tracing
* Claim universal cross-chain tracing
* Provide universal mixer/privacy-coin tracing
* Claim instantaneous blockchain monitoring
* Claim certainty in VASP attribution
* Claim that an automated score proves criminal activity
* Provide a real NCRP/SAHYOG government connection

---

## 8. Stretch Goals

These features shall only be implemented after the MVP is stable:

* Bitcoin support
* ML-based anomaly scoring
* Limited cross-chain bridge tracing
* Victim-facing case-status portal
* Advanced performance benchmarking

---

## 9. Success Criteria

The MVP shall be considered successful when the team can demonstrate the following complete workflow:

**Login → Create Case → Submit Wallet → Monitor → Detect Transaction → Trace Funds → Visualize Graph → Detect Suspicious Pattern → Calculate Explainable Risk → Attribute Likely VASP → Generate Alert → Mock Government Sync → Generate Evidence Report → Verify Integrity Hash**

---

## 10. Project Boundaries

Acetone is an investigative assistance system.

It provides publicly observable blockchain information, analytical signals, evidence organization, and suggested investigative actions.

Final investigative decisions, identification of individuals, legal requests, account actions, and fund-freezing decisions remain the responsibility of authorized human investigators and relevant authorities.

---

## 11. Requirement Priority

### P0 — Must Have

Required for the core demonstration and MVP.

### P1 — Should Have

Strengthens the system but can be reduced if development time becomes limited.

### P2 — Stretch

Implemented only after all P0 requirements are stable and tested.
