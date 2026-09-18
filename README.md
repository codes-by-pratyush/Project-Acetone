# Project Acetone 🔍
**Advanced Blockchain Forensics & Intelligence Platform**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)](https://neo4j.com/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)

---

## 💡 The Problem
As cryptocurrency adoption grows, so does its use in illicit activities. Financial Intelligence Units (FIUs) and forensic investigators struggle to manually trace stolen funds across thousands of obfuscated transactions, multiple hops, and complex wallet networks. Traditional methods are slow, manual, and prone to human error.

## 🚀 Our Solution
**Project Acetone** is a multi-service, graph-powered investigation platform engineered to automate the tracing of EVM-compatible fund flows. We provide investigators with an interactive, hop-by-hop visual graph, probabilistic exchange attribution, and automated risk scoring—turning raw blockchain data into actionable intelligence in seconds.

---

## ✨ Key Features & Technical Innovation

* **Interactive Threat Tracing (Neo4j + Cytoscape.js):** 
  We model EVM wallets as nodes and transactions as directed edges. This allows investigators to visually expand transaction paths hop-by-hop to discover where stolen funds are pooling.
* **Role-Based Access Control (JWT Authentication):** 
  Strict separation of duties. *Investigators* analyze data, *Supervisors* manage case lifecycles, and *Admins* handle infrastructure.
* **Hardened Security Posture:** 
  Inbound RPC queries are strictly sanitized using EVM regex patterns (`^0x[a-fA-F0-9]{40}$`). Sensitive endpoints are protected from brute-force attacks via Redis-backed rate limiting.
* **Microservice-Ready Architecture:** 
  Containerized deployment separating relational data (PostgreSQL), graph traversal (Neo4j), and caching (Redis) to ensure high throughput and scalability.

---

## 🏗️ System Architecture

```text
┌────────────────────────────────────────────────────────┐
│               Investigator UI (React)                  │
│       Cytoscape.js Network Graph • TailwindCSS         │
└───────────────────────────┬────────────────────────────┘
                            │ REST / Bearer JWT
┌───────────────────────────▼────────────────────────────┐
│                 Core Engine (FastAPI)                  │
│   Auth & RBAC • Address Sanitization • Query Engine    │
└───────┬───────────────────┬────────────────────┬───────┘
        │                   │                    │
┌───────▼──────┐     ┌──────▼──────┐      ┌──────▼──────┐
│  PostgreSQL  │     │    Neo4j    │      │    Redis    │
│ Cases, Audits│     │ Graph Hops  │      │ Cache/Queue │
└──────────────┘     └─────────────┘      └─────────────┘


Markdown
# Project Acetone 🔍
**Advanced Blockchain Forensics & Intelligence Platform**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)](https://neo4j.com/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)

---

##  The Problem
As cryptocurrency adoption grows, so does its use in illicit activities. Financial Intelligence Units (FIUs) and forensic investigators struggle to manually trace stolen funds across thousands of obfuscated transactions, multiple hops, and complex wallet networks. Traditional methods are slow, manual, and prone to human error.

##  Our Solution
**Project Acetone** is a multi-service, graph-powered investigation platform engineered to automate the tracing of EVM-compatible fund flows. We provide investigators with an interactive, hop-by-hop visual graph, probabilistic exchange attribution, and automated risk scoring—turning raw blockchain data into actionable intelligence in seconds.

---

##  Key Features & Technical Innovation

* **Interactive Threat Tracing (Neo4j + Cytoscape.js):** 
  We model EVM wallets as nodes and transactions as directed edges. This allows investigators to visually expand transaction paths hop-by-hop to discover where stolen funds are pooling.
* **Role-Based Access Control (JWT Authentication):** 
  Strict separation of duties. *Investigators* analyze data, *Supervisors* manage case lifecycles, and *Admins* handle infrastructure.
* **Hardened Security Posture:** 
  Inbound RPC queries are strictly sanitized using EVM regex patterns (`^0x[a-fA-F0-9]{40}$`). Sensitive endpoints are protected from brute-force attacks via Redis-backed rate limiting.
* **Microservice-Ready Architecture:** 
  Containerized deployment separating relational data (PostgreSQL), graph traversal (Neo4j), and caching (Redis) to ensure high throughput and scalability.

---

## 🏗️ System Architecture

```text
┌────────────────────────────────────────────────────────┐
│               Investigator UI (React)                  │
│       Cytoscape.js Network Graph • TailwindCSS         │
└───────────────────────────┬────────────────────────────┘
                            │ REST / Bearer JWT
┌───────────────────────────▼────────────────────────────┐
│                 Core Engine (FastAPI)                  │
│   Auth & RBAC • Address Sanitization • Query Engine    │
└───────┬───────────────────┬────────────────────┬───────┘
        │                   │                    │
┌───────▼──────┐     ┌──────▼──────┐      ┌──────▼──────┐
│  PostgreSQL  │     │    Neo4j    │      │    Redis    │
│ Cases, Audits│     │ Graph Hops  │      │ Cache/Queue │
└──────────────┘     └─────────────┘      └─────────────┘


- Tech Stack
Frontend: React, TypeScript, Vite, TailwindCSS, Cytoscape.js (Graph UI), Recharts (Analytics)
Backend: Python, FastAPI, Uvicorn, Passlib/JWT (Security), Pydantic (Data Validation)
Databases: PostgreSQL (Relational), Neo4j (Graph), Redis (Cache)
DevOps: Docker, Docker Compose, Git

- The Team
Pratyush Ranjan Sahu – Team Leader & Backend Lead
Saishree Mohanty – Frontend & UX/UI Lead
Asad Ahemad – Blockchain Integration Engineer
Subham Sahoo 4 – Database & Infrastructure Engineer
Jyotirmaye Dalai – Cybersecurity & AppSec Developer
Anshuman Pani – OSINT & Research Lead