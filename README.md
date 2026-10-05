# 🛡️ SentinelCore — Distributed Real-Time Financial Fraud & Autonomous AML Detection Platform
![Java](https://img.shields.io/badge/Java-17%2F21-orange?logo=openjdk)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2+-brightgreen?logo=springboot)
![Spring Data JPA](https://img.shields.io/badge/Spring%20Data%20JPA-Hibernate-blue)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi)
![Redis](https://img.shields.io/badge/Redis-In--Memory%20Cache-DC382D?logo=redis)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-FF6F61)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?logo=scikitlearn)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Agentic%20LLM-8E75B2?logo=googlegemini)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker)
![Maven](https://img.shields.io/badge/Maven-Build-C71A36?logo=apachemaven)
![REST API](https://img.shields.io/badge/API-REST-orange)
An institutional-grade, distributed **Real-Time Financial Fraud & Autonomous Anti-Money Laundering (AML) Platform** engineered for tier-1 banking institutions. 
The system pairs a high-performance **Java Spring Boot 3 Core Anchor** with an asynchronous **Python FastAPI AI Worker**, combining microsecond in-memory velocity rate limiting (**Redis**), deterministic statutory banking rules (RBI Section 139A compliance, KYC PAN matching, 30-minute rapid-drain checks), **Machine Learning Anomaly Detection (Isolation Forest)**, **Supervised Transaction Categorization (Random Forest)**, **Vector Knowledge Retrieval (ChromaDB RAG)** with real-time dynamic self-learning memory, and an **Autonomous Agentic AI (ReAct Tool-Calling)** powered by **Google Gemini** capable of investigating crime typologies and executing live administrative account freezes.
---
## 📑 Table of Contents
- [Overview](#-overview)
- [System Architecture](#-system-architecture)
  - [Architectural Separation: Hot Path vs. Cold Path](#architectural-separation-hot-path-vs-cold-path)
  - [System Flow Diagram](#system-flow-diagram)
- [Core Pillars & Key Features](#-core-pillars--key-features)
  - [### 1. Enterprise Anchor (Java Spring Boot 3)](#1-enterprise-anchor-java-spring-boot-3)
  - [### 2. Microsecond Rate Limiting (Redis)](#2-microsecond-rate-limiting-redis)
  - [### 3. Analytical & Machine Learning Engine (Python FastAPI)](#3-analytical--machine-learning-engine-python-fastapi)
  - [### 4. Financial RAG & Dynamic Vector Memory (ChromaDB)](#4-financial-rag--dynamic-vector-memory-chromadb)
  - [### 5. Autonomous Agentic AI (ReAct Framework & Tool Calling)](#5-autonomous-agentic-ai-react-framework--tool-calling)
- [Core Business & Statutory Rules](#-core-business--statutory-rules)
- [Entity Relationships](#-entity-relationships)
- [Project Structure](#-project-structure)
- [API Endpoints Reference](#-api-endpoints-reference)
- [API Payloads & Real-World Scenarios](#-api-payloads--real-world-scenarios)
  - [Scenario 1: Clean Low-Risk Payment (200 OK)](#1-everyday-clean-upi-payment--200-ok)
  - [Scenario 2: Missing PAN on High-Value Transaction (400 Bad Request)](#2-missing-pan-on-high-value-transaction--400-bad-request)
  - [Scenario 3: Velocity Attack Intercepted by Redis (429 Rate Limit)](#3-high-velocity-burst-attack--429-too-many-requests)
  - [Scenario 4: High-Value Fraud Blocked & Kill-Switch Triggered (403 Forbidden)](#4-high-value-fraud-blocked--kill-switch-triggered--403-forbidden)
  - [Scenario 5: Precedent Investigation via RAG (200 OK)](#5-aml-precedent-investigation-via-rag--200-ok)
  - [Scenario 6: Autonomous Agent Investigation & Live Freeze (200 OK)](#6-autonomous-agent-investigation--live-freeze--200-ok)
- [Swagger / OpenAPI Documentation](#-swagger--openapi-documentation)
- [Local Setup & Running](#-local-setup--running)
- [Testing & Verification](#-testing--verification)
- [Author](#-author)
---
## 📌 Overview
Traditional banking fraud systems suffer from two extremes: brittle static `if/else` rules that miss complex behavioral anomalies, or pure black-box machine learning models that lack regulatory explainability, breach strict payment SLAs, and fail statutory compliance checks.
**SentinelCore** solves this via the **Java Anchor + Python Worker Distributed Architecture**:
1. **The Hot Path (Real-Time Payment Rails — <30ms SLA)**:
   - **Redis (Port 6379)**: Enforces sliding-window velocity checks at <0.5ms latency, rejecting automated bot bursts before database saturation.
   - **Java Spring Boot 3 (Port 8080)**: Manages transactional ledger integrity, ACID balance mutations (`@Transactional`), and front-door statutory checks (RBI Rule 114B PAN mandate) backed by **PostgreSQL**.
   - **Python Worker (Port 8000)**: Evaluates behavioral anomalies using **Isolation Forest** and classifies spending with **Random Forest** in under 15ms.
   - **Automated Kill-Switch**: If a transaction triggers a critical fraud block, Spring Boot immediately flips the account status to `FROZEN` in PostgreSQL, instantly locking out subsequent attacks.
2. **The Cold Path (Forensic Investigation & Compliance Desk — Seconds SLA)**:
   - **ChromaDB Vector Store**: Semantic cosine similarity engine indexing historical crime typologies (`CASE-101` to `CASE-105`) with **dynamic vector ingestion** that embeds newly blocked fraud incidents in real time.
   - **Autonomous Agentic AI (ReAct)**: Dispatches a multi-tool agent powered by **Google Gemini** that queries banking ledgers, audits transaction history, matches vector precedents, and executes emergency administrative freezes with complete Explainable AI (XAI) audit trails.
---
## 🏗️ System Architecture
### Architectural Separation: Hot Path vs. Cold Path
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       1. THE HOT PATH (<30ms Latency)                       │
│                   Endpoint: POST /api/v1/payments/authorize                 │
│                                                                             │
│  Client Payment Request                                                     │
│        │                                                                    │
│        ▼                                                                    │
│  [ Redis Cache (:6379) ] ─────────> Velocity Check Exceeded? ──> 429 Block  │
│        │ (<0.5ms)                                                           │
│        ▼                                                                    │
│  [ Spring Boot Anchor (:8080) ] ──> Statutory PAN Check >= ₹50k ─> 400 Block│
│        │                                                                    │
│        ▼ (RestClient HTTP)                                                  │
│  [ ### Python AI Worker (:8000) ]                                               │
│        ├── Random Forest Categorizer                                        │
│        └── Isolation Forest Anomaly Detection (Inference <10ms)             │
│        │                                                                    │
│        ▼                                                                    │
│  Decision: APPROVED ──> Update Ledger Balance in PostgreSQL (:5332)         │
│  Decision: BLOCKED  ──> Trigger Defensive Kill-Switch (Freeze Account)      │
│                         └── Ingest Incident Vector into ChromaDB Memory     │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                         Account Flagged / Escalated
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       2. THE COLD PATH (~5-8s Latency)                      │
│                Endpoint: POST /api/v1/compliance/agent/investigate          │
│                                                                             │
│  Compliance Escalation Alert                                                │
│        │                                                                    │
│        ▼                                                                    │
│  [ Autonomous AML Agent (Gemini ReAct Loop) ]                               │
│        │                                                                    │
│        ├── 1. Sensor Check    ──> GET /api/v1/accounts/{id} (Spring Boot)   │
│        ├── 2. Behavior Audit  ──> GET /api/v1/accounts/{id}/transactions    │
│        ├── 3. Vector Match    ──> ChromaDB Cosine Search (Precedents)       │
│        └── 4. Actuator Trigger──> PATCH /api/v1/accounts/{id}/freeze        │
│        │                                                                    │
│        ▼                                                                    │
│  Outputs Official FIU-IND Suspicious Transaction Report (STR / PMLA)        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### System Flow Diagram
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT / API CONSUMER                             │
│                  (Postman / Web Frontend / External Gateway)                │
└───────────────────────┬─────────────────────────────┬───────────────────────┘
                        │                             │
    POST /payments/authorize                          │ POST /compliance/agent/investigate
                        ▼                             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   JAVA SPRING BOOT CORE ANCHOR (:8080)                      │
│                                                                             │
│  Controllers:                                                               │
│  ├── PaymentController      (Live Payment Authorization)                    │
│  ├── AccountController      (Account DTOs, Transactions & Live Freeze)      │
│  └── ComplianceController   (RAG Investigation & Autonomous Agent Gateway)  │
│                                                                             │
│  Services & Infrastructure:                                                 │
│  ├── VelocityService        <───> Redis In-Memory Sliding Window (:6379)     │
│  ├── PaymentService         <───> PostgreSQL 16 ACID Ledger (:5332)         │
│  └── AiWorkerClient         ───> Spring 6 RestClient (30s GenAI Timeout)    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Internal HTTP Dispatches
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   PYTHON FASTAPI AI WORKER (:8000)                          │
│                                                                             │
│  ML Engines & Knowledge Services:                                           │
│  ├── Features Engine        (Pandas / NumPy Behavioral Derivations)         │
│  ├── Categorizer            (Supervised Random Forest Classifier)           │
│  ├── Anomaly Engine         (Multi-Factor Calibrated Isolation Forest)      │
│  ├── Financial RAG Service  (Persistent ChromaDB Vector Store & Precedents) │
│  └── Autonomous Agent       (Gemini ReAct Agent with Tool-Calling Engine)   │
│                                                                             │
│  Agent Tools (Actuators & Sensors):                                         │
│  ├── get_account_details()    ──> Calls Java GET /api/v1/accounts/{id}      │
│  ├── get_recent_transactions()──> Calls Java GET /accounts/{id}/transactions │
│  ├── search_aml_precedents()  ──> Queries ChromaDB Vector Precedents        │
│  └── freeze_account()         ──> Calls Java PATCH /accounts/{id}/freeze    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🌟 Core Pillars & Key Features
### 1. Enterprise Anchor (Java Spring Boot 3)
🏛️ Layered Domain Architecture: Clear separation of Concerns across Controller, Service, Repository, DTO, Client, and Exception layers.
⚡ Atomic Balance Mutations: @Transactional boundaries guarantee balance deductions/credits and audit logging commit atomically or roll back on error.
🛡️ Defensive Kill-Switch: If a transaction is blocked for critical risk, PaymentService automatically updates the account's state in PostgreSQL to AccountStatus.FROZEN, neutralizing repeated automated attack bursts in 0ms.
🔒 Data Privacy & DPDP Compliance: Exposes clean AccountResponseDTO and TransactionResponseDTO models, strictly omitting raw PAN/PII credentials following the Principle of Least Privilege (PoLP).
🚨 Strict Fail-Closed Exception Handling: Centralized @RestControllerAdvice maps domain exceptions to RFC 7807 standards:
400 Bad Request ➡️ Statutory validation errors (missing PAN).
403 Forbidden ➡️ Account Frozen or Fraud Block decisions.
404 Not Found ➡️ Non-existent account entities.
429 Too Many Requests ➡️ Redis velocity limits exceeded.
503 Service Unavailable ➡️ Downstream AI worker connectivity timeouts.
### 2. Microsecond Rate Limiting (Redis)
⚡ Sliding-Window Velocity Engine: Intercepts automated high-frequency attacks in <0.5ms via StringRedisTemplate.
⏱️ Rule Threshold: Max 3 transactions per 60 seconds per account.
🔄 Atomic Counter with Dynamic TTL: Uses atomic INCR combined with proactive TTL checks to ensure expired counters never leave permanent locks.
### 3. Analytical & Machine Learning Engine (Python FastAPI)
🌲 Supervised Categorization (Random Forest): Classifies transactions into FOOD_DINING, UTILITIES_BILLS, INVESTMENT_WEALTH, TRAVEL_FUEL, ENTERTAINMENT, TRANSFER, or ACCOUNT_DEPOSIT with confidence metrics.
🔬 Multi-Factor Anomaly Detection (Isolation Forest): Calibrated for Indian INR banking distributions, scaling structural tree depth with log-scaled magnitude ratios.
🌍 Spatial-Temporal Impossible Travel: Intercepts impossible geographical velocity changes (e.g., Mumbai to Dubai in 15 minutes).
💾 Sub-5ms Inference: Pre-trained Scikit-Learn models persisted via joblib.
### 4. Financial RAG & Dynamic Vector Memory (ChromaDB)
🧠 Cosine Similarity Vector Search: Uses the all-MiniLM-L6-v2 ONNX embedding model mapping transaction semantics into a 384-dimensional vector space.
📚 Precedent Crime Knowledge Base: Pre-seeded with real-world typologies:
CASE-101: Structuring and Smurfing (evading Section 139A ₹50k PAN limits).
CASE-102: Account Takeover (ATO) & Dormant Account Liquidation.
CASE-103: Pass-Through Money Mule Activity (inward credit + rapid cash drain).
CASE-104: Cyber Fraud / Remote Access Phishing Proceeds.
CASE-105: Trade-Based Layering via Mismatched Beneficiaries.
⚡ Dynamic Continuous Learning: Whenever a transaction is BLOCKED on the live payment path, the system dynamically embeds and writes the incident (INC-{account_id}-{timestamp}) into ChromaDB in real time!
### 5. Autonomous Agentic AI (ReAct Framework & Tool Calling)
🤖 Reason + Act (ReAct) Engine: Powered by Google Gemini 2.5 Flash using Automatic Function Calling (AFC).
🛠️ Real Actuators & Sensors: The agent autonomously reasons about which tools to dispatch:
get_account_details(account_id): Fetches live balance and status from Spring Boot.
get_recent_transactions(account_id): Audits recent transaction velocity from PostgreSQL.
search_aml_precedents(crime_description): Queries ChromaDB vector memory.
freeze_account(account_id, reason): Calls Spring Boot to update the account to FROZEN.
📜 Explainable AI (XAI): Captures step-by-step tool executions and observations, producing an audit-proof trail and an executive FIU-IND Suspicious Transaction Report (STR) citing the Prevention of Money Laundering Act (PMLA).
## 📜 Core Business & Statutory Rules
| Rule Identifier | Trigger Condition | Enforcement Layer | Action Taken |
|---|---|---|---|
| Statutory PAN Requirement | Transaction Amount ≥ ₹50,000 without PAN | Spring Boot Front Door | Instant 400 Bad Request |
| KYC PAN Match Validation | Submitted PAN ≠ Account's Registered PAN | Python Rule Engine | Instant BLOCKED (403) |
| Velocity Burst Protection | > 3 transactions in 60 seconds | Redis In-Memory Cache | Instant 429 Too Many Requests |
| 30-Minute Rapid-Drain Protection | Transfer > ₹1,00,000 within 30 min of prior high-value tx | Spring Data JPA / Python | Instant BLOCKED (403) |
| Impossible Travel Anomaly | Distance velocity > 800 km/h between transactions | Python Spatial Engine | Instant BLOCKED (403) |
| Automated Defensive Kill-Switch | Decision is BLOCKED on high risk | Spring Boot PaymentService | Flips Account to FROZEN in DB |
| Account Sanctions Lock | Account status is FROZEN | Spring Boot Pre-Check | Instant 403 AccountFrozenException |
## 🗄️ Entity Relationships
```text
┌──────────────────────────────────────┐
│               Account                │
├──────────────────────────────────────┤
│ id (PK)                              │
│ account_number (UNIQUE)              │
│ customer_name                        │
│ balance                              │
│ registered_pan                       │
│ status (ACTIVE, FROZEN)              │
└──────────────────┬───────────────────┘
                   │ 1
                   │
                   │ *
┌──────────────────▼───────────────────┐
│             Transaction              │
├──────────────────────────────────────┤
│ id (PK)                              │
│ account_id (FK)                      │
│ amount                               │
│ transaction_type (DEPOSIT, WITHDRAW) │
│ pan_number                           │
│ location                             │
│ decision (APPROVED, MANUAL_REVIEW... )│
│ timestamp                            │
└──────────────────────────────────────┘
```

## 📁 Project Structure
```text
sentinel-core/
│
├── sentinel-anchor/                        # Java Spring Boot 3 Core Backend (Port 8080)
│   ├── src/main/java/com/SentinelAnchor/
│   │   ├── config/
│   │   │   └── RestClientConfig.java       # Spring 6 RestClient with 30s GenAI Read Timeout
│   │   ├── controller/
│   │   │   ├── PaymentController.java      # Live Payment Authorization (/authorize)
│   │   │   ├── AccountController.java      # Account DTOs, Transactions, & Live Freeze
│   │   │   └── ComplianceController.java   # RAG Investigation & Agent Gateways
│   │   ├── dto/
│   │   │   ├── TransactionRequestDTO.java  # Payment request payload
│   │   │   ├── TransactionResultDTO.java   # Payment result payload
│   │   │   ├── AccountResponseDTO.java     # Privacy-compliant account contract
│   │   │   ├── TransactionResponseDTO.java # Ledger history response contract
│   │   │   ├── AmlInvestigationRequestDto.java
│   │   │   ├── AmlInvestigationResponseDto.java
│   │   │   ├── AgentInvestigationRequestDto.java
│   │   │   └── AgentInvestigationResponseDto.java
│   │   ├── entity/
│   │   │   ├── Account.java                # JPA Account entity with KYC PAN
│   │   │   └── Transaction.java            # JPA Transaction ledger entity
│   │   ├── enums/
│   │   │   ├── AccountStatus.java           # ACTIVE, FROZEN
│   │   │   ├── TransactionDecision.java     # APPROVED, MANUAL_REVIEW, BLOCKED
│   │   │   └── TransactionType.java         # DEPOSIT, WITHDRAW
│   │   ├── exception/
│   │   │   ├── GlobalExceptionHandler.java # Centralized @RestControllerAdvice
│   │   │   ├── AccountNotFoundException.java
│   │   │   ├── AccountFrozenException.java
│   │   │   ├── InsufficientBalanceException.java
│   │   │   ├── VelocityLimitExceededException.java
│   │   │   └── AiServiceException.java     # Downstream Python error extractor
│   │   ├── repository/
│   │   │   ├── AccountRepository.java
│   │   │   └── TransactionRepository.java  # Baseline & 30-min velocity query
│   │   └── service/
│   │       ├── PaymentService.java          # ACID orchestrator & Automated Kill-Switch
│   │       ├── VelocityService.java         # Redis sliding-window velocity service
│   │       └── AiWorkerClient.java          # Multi-service HTTP client to Python
│   ├── src/main/resources/
│   │   └── application.properties           # PostgreSQL, Redis & AI Worker config
│   ├── docker-compose.yml                    # Local PostgreSQL & Redis containers
│   └── pom.xml                               # Maven project dependencies
│
└── ai-worker/                               # Python FastAPI Machine Learning Worker (Port 8000)
    ├── venv/                                # Python virtual environment (ignored)
    ├── .env                                 # Google Gemini API credentials (ignored)
    ├── chroma_db/                           # Persistent ChromaDB vector storage (ignored)
    ├── models.py                            # Pydantic schemas (Audit, RAG, Agent)
    ├── ml_service.py                        # Calibrated Isolation Forest anomaly engine
    ├── categorizer.py                       # Supervised Random Forest categorizer
    ├── features.py                          # Pandas/NumPy behavioral feature extractor
    ├── ai_analyst.py                        # Google Gemini SAR narrative generator
    ├── rag_service.py                       # ChromaDB Vector Store & Precedent Search
    ├── agent_tools.py                       # ReAct Actuators & Sensors (Spring Boot Bridge)
    ├── agent_service.py                     # Autonomous Agent Controller & Tool Calling Loop
    ├── requirements.txt                     # Python package dependencies
    └── main.py                              # FastAPI REST microservice & endpoints
```

## 📡 API Endpoints Reference
### Spring Boot Core Anchor (:8080)
| Method | Endpoint | Request Body | Description |
|---|---|---|---|
| POST | `/api/v1/payments/authorize` | `TransactionRequestDTO` | Real-time payment evaluation, Redis velocity, ML audit, & ACID ledger |
| GET | `/api/v1/accounts/{id}` | None | Retrieve account status, balance, and ID (sanitized DTO) |
| GET | `/api/v1/accounts/{id}/transactions` | None | Fetch top 10 historical transactions for behavioral baseline |
| PATCH | `/api/v1/accounts/{id}/freeze` | None | Administrative actuator: atomically freezes account in PostgreSQL |
| POST | `/api/v1/compliance/investigate` | `AmlInvestigationRequestDto` | RAG vector search + Gemini regulatory STR assessment |
| POST | `/api/v1/compliance/agent/investigate` | `AgentInvestigationRequestDto` | Dispatches Autonomous Agent to execute multi-tool forensic audit |
### Python AI Worker (:8000)
| Method | Endpoint | Request Body | Description |
|---|---|---|---|
| GET | `/health` | None | Health check & microservice status |
| POST | `/api/v1/audit` | `TransactionData` | Multimodal ML audit (RF + Isolation Forest + Dynamic ChromaDB Ingestion) |
| POST | `/api/v1/aml/investigate` | `AmlInvestigationRequest` | Vector similarity search across ChromaDB + Gemini legal memo |
| POST | `/api/v1/agent/investigate` | `AgentInvestigationRequest` | Runs ReAct autonomous agent loop with function/tool calling |
## 🧪 API Payloads & Real-World Scenarios

### 1. Everyday Clean UPI Payment — 200 OK

```http
POST http://localhost:8080/api/v1/payments/authorize
Content-Type: application/json
```

**Request:**

```json
{
  "accountId": 1,
  "amount": 350.0,
  "transactionType": "WITHDRAW",
  "location": "Mumbai, India",
  "panNumber": null
}
```

**Response:**

```json
{
  "transactionId": 1,
  "accountNumber": "ACC-1042",
  "amount": 350.0,
  "updatedBalance": 49650.0,
  "status": "APPROVED",
  "riskScore": 8.5,
  "category": "FOOD_DINING",
  "location": "Mumbai, India",
  "complianceNote": "Transaction verified against historical baseline. Low risk profile under frictionless retail rails."
}
```

### 2. Missing PAN on High-Value Transaction — 400 Bad Request

```http
POST http://localhost:8080/api/v1/payments/authorize
Content-Type: application/json
```

**Request:**

```json
{
  "accountId": 1,
  "amount": 60000.0,
  "transactionType": "WITHDRAW",
  "location": "Mumbai, India",
  "panNumber": null
}
```

**Response:**

```json
{
  "error": "VALIDATION_FAILED",
  "message": "RBI Compliance Violation: Transactions of ₹60000.0 (>= ₹50,000) strictly mandate a valid PAN number."
}
```

### 3. High-Velocity Burst Attack — 429 Too Many Requests

Attempting 4 rapid transactions within 60 seconds triggers Redis in <0.5ms.

```http
POST http://localhost:8080/api/v1/payments/authorize
Content-Type: application/json
```

**Request:**

```json
{
  "accountId": 1,
  "amount": 500.0,
  "transactionType": "WITHDRAW",
  "location": "Mumbai, India"
}
```

**Response:**

```json
{
  "status": 429,
  "error": "VELOCITY_LIMIT_EXCEEDED",
  "message": "Velocity Limit Exceeded: Account #1 exceeded 3 transactions in 60s. Cool-down remaining: 58s."
}
```

### 4. High-Value Fraud Blocked & Kill-Switch Triggered — 403 Forbidden

```http
POST http://localhost:8080/api/v1/payments/authorize
Content-Type: application/json
```

**Request:**

```json
{
  "accountId": 1,
  "amount": 250000.0,
  "transactionType": "WITHDRAW",
  "location": "Dubai",
  "panNumber": "ABCDE1234F"
}
```

**Response:**

```json
{
  "transactionId": 32,
  "accountNumber": "ACC-1042",
  "amount": 250000.0,
  "updatedBalance": 49650.0,
  "status": "BLOCKED",
  "riskScore": 86.1,
  "category": "TRANSFER",
  "location": "Dubai",
  "complianceNote": "Critical Alert: High-value anomalous transaction detected. Incident embedded into ChromaDB memory. Account #1 status has been atomically FROZEN to prevent capital flight."
}
```

Subsequent payment attempts on Account #1 are immediately rejected with:

```json
{
  "status": 403,
  "error": "ACCOUNT_FROZEN",
  "message": "Account #ACC-1042 is FROZEN by regulatory order."
}
```

### 5. AML Precedent Investigation via RAG — 200 OK

```http
POST http://localhost:8080/api/v1/compliance/investigate
Content-Type: application/json
```

**Request:**

```json
{
  "query": "Multiple rapid cash ATM withdrawals following inward RTGS transfer",
  "top_k": 2
}
```

**Response:**

```json
{
  "query": "Multiple rapid cash ATM withdrawals following inward RTGS transfer",
  "retrieved_precedents": [
    {
      "case_id": "CASE-103",
      "description": "Money Mule Activity: Student savings account with typical monthly volume of ₹1,500 suddenly received inward RTGS credit of ₹4,50,000 followed by multiple rapid cash ATM withdrawals in different locations.",
      "category": "MULE_ACCOUNT",
      "risk": "HIGH",
      "similarity_score": 0.662
    }
  ],
  "investigative_assessment": "MEMORANDUM: The reported activity matches historical precedent CASE-103 (Money Mule Pass-Through). Inward RTGS settlement followed by rapid multi-location cash extraction indicates layered laundering. Immediate administrative freeze and mandatory STR filing under PMLA guidelines with FIU-IND required."
}
```

### 6. Autonomous Agent Investigation & Live Freeze — 200 OK

```http
POST http://localhost:8080/api/v1/compliance/agent/investigate
Content-Type: application/json
```

**Request:**

```json
{
  "account_id": 1,
  "escalation_notes": "multiple transactions of 48000 to bypass pan validation"
}
```

**Response:**

```json
{
  "account_id": 1,
  "status": "COMPLETED",
  "investigation_steps_executed": [
    {
      "type": "TOOL_EXECUTION",
      "tool_name": "get_account_details",
      "arguments": { "account_id": 1 }
    },
    {
      "type": "TOOL_OBSERVATION",
      "tool_name": "get_account_details",
      "response_summary": "{'id': 1, 'status': 'ACTIVE', 'balance': 103197.0}"
    },
    {
      "type": "TOOL_EXECUTION",
      "tool_name": "get_recent_transactions",
      "arguments": { "account_id": 1 }
    },
    {
      "type": "TOOL_OBSERVATION",
      "tool_name": "get_recent_transactions",
      "response_summary": "{'transactions': [{'id': 32, 'amount': 256000.0, 'location': 'Dubai', 'decision': 'BLOCKED'}, ...]}"
    },
    {
      "type": "TOOL_EXECUTION",
      "tool_name": "search_aml_precedents",
      "arguments": {
        "crime_description": "multiple transactions below reporting threshold to bypass pan validation structuring smurfing"
      }
    },
    {
      "type": "TOOL_OBSERVATION",
      "tool_name": "search_aml_precedents",
      "response_summary": "{'retrieved_precedents': [{'case_id': 'CASE-101', 'category': 'SMURFING_STRUCTURING', 'similarity_score': 0.671}]}"
    },
    {
      "type": "TOOL_EXECUTION",
      "tool_name": "freeze_account",
      "arguments": {
        "account_id": 1,
        "reason": "Confirmed structuring and smurfing activity to bypass PAN limits under Section 139A."
      }
    },
    {
      "type": "TOOL_OBSERVATION",
      "tool_name": "freeze_account",
      "response_summary": "{'status': 'SUCCESS', 'action': 'ACCOUNT_FROZEN', 'database_updated': true}"
    }
  ],
  "final_assessment_report": "AML investigation confirmed Structuring / Smurfing matching precedent CASE-101. Account ID #1 was frozen in PostgreSQL and the remaining balance was locked to prevent capital flight."
}
```

## 📖 Swagger / OpenAPI Documentation
Both microservices generate interactive API specifications out of the box:

- **Python AI Worker Swagger UI:** `http://localhost:8000/docs`
- **Python OpenAPI Specification:** `http://localhost:8000/openapi.json`
- **Spring Boot Actuator / Health:** `http://localhost:8080/actuator/health`
## 🚀 Local Setup & Running

### Prerequisites
- Java 17 or 21
- Python 3.11+
- Docker Desktop
- Git
### Step 1: Start PostgreSQL and Redis via Docker
From the project root:

```bash
docker run -d --name postgres-db -p 5332:5432 -e POSTGRES_DB=sentinel_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres postgres:16-alpine
docker run -d --name redis-cache -p 6379:6379 redis:7-alpine
```

Verify both containers are running:

```bash
docker ps
```

### Step 2: Start Python AI Worker
Navigate to ai-worker/:

```bash
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1    # On Windows
source venv/bin/activate       # On Linux/macOS
# 2. Install dependencies
pip install -r requirements.txt
# 3. Create .env with your Gemini API key
echo GEMINI_API_KEY=your_actual_gemini_key > .env
# 4. Start FastAPI server
uvicorn main:app --reload --port 8000
```

### Step 3: Start Spring Boot Core Anchor
Navigate to sentinel-anchor/:

```bash
# Windows
.\mvnw.cmd spring-boot:run
# Linux / macOS
./mvnw spring-boot:run
```

Spring Boot will start on http://localhost:8080 and connect to PostgreSQL (5332), Redis (6379), and the Python AI Worker (8000).

## 🧪 Testing & Verification

The README scenarios above can be used as manual integration tests with Postman or `curl`.

Recommended verification order:

1. Check Spring Boot health.
2. Check the Python worker health.
3. Submit a normal payment and verify `APPROVED`.
4. Submit a high-value transaction without PAN and verify `400`.
5. Trigger the Redis velocity limit and verify `429`.
6. Submit a high-risk transaction and verify `BLOCKED` plus account freeze.
7. Run the RAG investigation endpoint and verify precedent retrieval.
8. Run the autonomous agent endpoint and verify tool execution and account freeze.

## 👨‍💻 Author
Deendayal Nishad
Electronics & Telecommunication Engineering Student | Aspiring Backend, Cloud & AI Systems Engineer

GitHub: @deendayal038
## ⭐ Support & Feedback
If this architecture helped you understand distributed microservices pairing Spring Boot, Redis, Scikit-Learn, ChromaDB, and Agentic AI, please consider giving the repository a Star!

## 📄 License

This project is provided for educational, portfolio, and hackathon purposes. Add a `LICENSE` file if you plan to distribute the project publicly.
