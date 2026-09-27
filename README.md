# 🛡️ SentinelCore — Distributed Real-Time Financial Fraud & AML Detection Platform

![Java](https://img.shields.io/badge/Java-17%2F21-orange?logo=openjdk)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2+-brightgreen?logo=springboot)
![Spring Data JPA](https://img.shields.io/badge/Spring%20Data%20JPA-Hibernate-blue)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?logo=scikitlearn)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-LLM%20AI-8E75B2?logo=googlegemini)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker)
![Maven](https://img.shields.io/badge/Maven-Build-C71A36?logo=apachemaven)
![REST API](https://img.shields.io/badge/API-REST-orange)

An institutional-grade, distributed **Real-Time Financial Fraud & Anti-Money Laundering (AML) Detection Platform** engineered for banking environments. 

The system pairs a high-performance **Java Spring Boot 3 Core Anchor** with an asynchronous **Python FastAPI AI Worker**, combining deterministic statutory banking rules (RBI compliance, KYC PAN matching, 30-minute rapid-drain velocity checks) with **Machine Learning Anomaly Detection (Isolation Forest)**, **Supervised Transaction Categorization (Random Forest)**, and **Generative AI (Google Gemini)** to synthesize real-time, regulatory-compliant Suspicious Activity Reports (SAR) citing **FIU-IND** compliance directives.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
  - [Spring Boot Anchor Features](#spring-boot-anchor-features)
  - [Python AI Worker Features](#python-ai-worker-features)
- [Tech Stack](#️-tech-stack)
  - [Enterprise Anchor (Java)](#enterprise-anchor-java)
  - [AI & ML Worker (Python)](#ai--ml-worker-python)
  - [Infrastructure & Data](#infrastructure--data)
- [Architecture](#-architecture)
  - [System Flow](#system-flow)
  - [End-to-End Request Lifecycle](#end-to-end-request-lifecycle)
- [Core Business & Statutory Rules](#-core-business--statutory-rules)
- [Entity Relationships](#-entity-relationships)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [API Payloads & Real-World Scenarios](#-api-payloads--real-world-scenarios)
- [Swagger / OpenAPI Documentation](#-swagger--openapi-documentation)
- [Local Setup & Running](#-local-setup--running)
- [Testing & Verification](#-testing--verification)
- [Roadmap & Upcoming Milestones](#-roadmap--upcoming-milestones)
- [Author](#-author)

---

## 📌 Overview

Traditional banking fraud systems suffer from two extremes: brittle static `if/else` rules that miss complex behavioral anomalies, or pure black-box machine learning models that lack regulatory explainability and fail statutory compliance checks.

**SentinelCore** implements the enterprise **Java Anchor + Python Worker Architecture**:

- **Java Spring Boot 3 Anchor (Port 8080)**: Manages transactional ledger integrity, account state lifecycles (`ACTIVE`, `FROZEN`), ACID balance mutations via `@Transactional`, front-door statutory checks (RBI Rule 114B PAN enforcement), and historical baseline retrieval via **PostgreSQL**.
- **Python FastAPI AI Worker (Port 8000)**: Serves as the analytical and machine learning intelligence layer. It extracts behavioral signals using **Pandas**, classifies transaction categories using **Random Forest**, evaluates multidimensional anomaly risk using **Isolation Forest**, detects impossible travel velocity, and generates human-readable compliance narratives via **Google Gemini LLM**.
- **Resilient Inter-Service Communication**: Orchestrated via Spring 6 `RestClient` with socket timeouts and strict fail-closed error translation.

---

## ✨ Key Features

### Spring Boot Anchor Features
- 🏛️ **Layered Enterprise Architecture**: Strict decoupling of Controller, Service, Client, Repository, Entity, and DTO layers.
- ⚡ **Atomic Balance Mutations**: `@Transactional` boundaries guarantee balance deductions/credits and audit logging commit together or roll back on error.
- 🛡️ **Statutory Front-Door Guard**: Enforces RBI Rule 114B in Java (`amount >= ₹50,000` strictly requires a PAN) with instant `400 Bad Request` rejections before network dispatch.
- 🔍 **Historical Context Aggregation**: Derives baseline metrics (retrieving the customer's last 10 transaction amounts) and detects rapid high-value drain attempts via Spring Data JPA derived queries.
- ⏱️ **30-Minute High-Value Velocity Protection**: Checks PostgreSQL in real time to intercept and block repeated $> ₹1,00,000$ transfers attempted within 30 minutes.
- 🚨 **Strict Fail-Closed Exception Handling**: Centralized `@RestControllerAdvice` intercepts network anomalies, extracts downstream Python error responses, and returns structured RFC 7807-style error contracts.
- 🔄 **Bidirectional Banking Support**: Handles both `DEPOSIT` (inward credit) and `WITHDRAW` (outward debit) with case-insensitive Jackson parsing (`@JsonCreator`).

### Python AI Worker Features
- ⚡ **Asynchronous REST Microservice**: High-throughput FastAPI service running on Uvicorn with Pydantic type validation.
- 🌲 **Supervised Transaction Categorization**: **Random Forest Classifier** trained on tabular features (`amount`, `hour`, `is_weekend`) categorizing payments into `FOOD_DINING`, `UTILITIES_BILLS`, `INVESTMENT_WEALTH`, `TRAVEL_FUEL`, `ENTERTAINMENT`, `TRANSFER`, or `UNCATEGORIZED` with confidence scores.
- 🔬 **Multi-Factor Behavioral Anomaly Detection**: **Isolation Forest** trained on Indian INR retail banking distributions combining structural tree depth with continuous logarithmic magnitude scaling.
- 🌍 **Impossible Travel Velocity Engine**: Automatically flags spatial-temporal anomalies when geographic location changes faster than physically possible within a given time delta.
- 🛡️ **KYC PAN Match Verification**: Compares submitted transaction PAN against the customer's registered KYC PAN, triggering instant security blocks on identity mismatch.
- 🤖 **Explainable AI (XAI) Compliance Narratives**: Utilizes **Google Gemini LLM** with financial prompts to synthesize 2-sentence executive Suspicious Activity Reports (SAR) citing **FIU-IND** AML regulations, backed by a defensive local fallback.
- 💾 **Sub-5ms Model Persistence**: Pre-trained models serialized to disk via `joblib`, eliminating cold-start retraining latency.

---

## 🛠️ Tech Stack

### Enterprise Anchor (Java)
| Technology | Purpose |
|---|---|
| **Java 17 / 21** | Type-safe core programming language |
| **Spring Boot 3.2+** | Enterprise backend application framework |
| **Spring Web MVC** | RESTful HTTP controllers & JSON serialization |
| **Spring 6 RestClient** | Fluent, synchronous inter-service HTTP client |
| **Spring Data JPA** | Data persistence & ORM abstraction |
| **Hibernate 6.x / 7.x** | Object-Relational Mapping (ORM) engine |
| **PostgreSQL Driver** | High-performance JDBC driver |
| **Jakarta Validation** | Bean Validation (`@NotNull`, `@Positive`) |
| **Lombok** | Boilerplate elimination (`@Data`, `@Builder`, `@Slf4j`) |
| **Jackson** | JSON serialization & `@JsonCreator` case-insensitivity |

### AI & ML Worker (Python)
| Technology | Purpose |
|---|---|
| **Python 3.11+** | Analytical & machine learning runtime |
| **FastAPI** | High-performance async microservice framework |
| **Uvicorn** | Lightning-fast ASGI web server |
| **Pydantic v2** | Data contract validation & schema enforcement |
| **Scikit-Learn** | Isolation Forest & Random Forest algorithms |
| **Pandas & NumPy** | In-memory feature engineering & matrix math |
| **Google GenAI SDK** | Gemini 2.5 Flash / 1.5 Flash LLM integration |
| **Joblib** | Serialization and persistence of trained ML models |
| **Python-Dotenv** | Secure environment variable configuration |

### Infrastructure & Data
| Technology | Purpose |
|---|---|
| **PostgreSQL 16** | ACID-compliant relational database |
| **Docker & Docker Compose** | Containerized database deployment |
| **Maven & Maven Wrapper** | Java build and lifecycle management |

---

## 🏗️ Architecture

### System Flow

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT / API CONSUMER                             │
│                  (Postman / Web Frontend / External Gateway)                │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ POST /api/v1/payments/authorize
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   JAVA SPRING BOOT CORE ANCHOR (:8080)                      │
│                                                                             │
│  1. Front-Door Validation (RBI PAN Rule >= ₹50,000)                        │
│  2. Account Lookup & Solvency Check (@Transactional)                        │
│  3. Historical Baseline & 30-min Velocity Query                             │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │      AiWorkerClient (Spring 6 RestClient with Socket Timeouts)        │  │
│  └───────────────────────────────────┬───────────────────────────────────┘  │
└──────────────────────────────────────┼──────────────────────────────────────┘
                                       │ Internal HTTP POST /api/v1/audit
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   PYTHON FASTAPI AI WORKER (:8000)                          │
│                                                                             │
│  ┌───────────────────────┐  ┌───────────────────────┐  ┌─────────────────┐  │
│  │ Feature Engineering   │  │ Random Forest         │  │ Impossible      │  │
│  │ (Pandas / NumPy)      │  │ Categorizer (Joblib)  │  │ Travel Check    │  │
│  └───────────┬───────────┘  └───────────┬───────────┘  └────────┬────────┘  │
│              │                          │                       │           │
│              └──────────────────────────┼───────────────────────┘           │
│                                         ▼                                   │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Isolation Forest Anomaly Engine (Multi-Factor Dynamic Scoring)        │  │
│  └───────────────────────────────────┬───────────────────────────────────┘  │
│                                      │                                      │
│                                      ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Google Gemini LLM (XAI Suspicious Activity Report Generation)         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ JSON Response: Decision, Scores & SAR
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   JAVA SPRING BOOT ENFORCEMENT & LEDGER                     │
│                                                                             │
│  4. Enforce Decision (APPROVED -> Mutate Balance | BLOCKED -> 403)          │
│  5. Persist Immutable Record in PostgreSQL (:5332)                          │
└─────────────────────────────────────────────────────────────────────────────┘
# End-to-End Request Lifecycle

```text
Incoming Payment Request (JSON)
       │
       ▼
Spring Boot Front Door Check
(Is Amount >= ₹50,000 without PAN? → Throw 400 Bad Request)
       │
       ▼
Query PostgreSQL
(Fetch Account, Status, Past 10 Amounts, 30-min High-Value Flag)
       │
       ▼
Package AiWorkerRequestDTO
(Raw financial facts, location, timestamp)
       │
       ▼
Dispatch via RestClient to Python
(http://localhost:8000/api/v1/audit)
       │
       ├── Python extracts hour, weekend, night, and international flags
       ├── Python checks KYC Registered PAN match
       ├── Python verifies 30-min rapid drain velocity
       ├── Random Forest predicts transaction category
       ├── Isolation Forest evaluates multidimensional anomaly score
       └── Gemini LLM drafts official compliance narrative
       │
       ▼
Python returns AuditResponse
(Decision, Category, Risk Score, SAR Narrative)
       │
       ▼
Spring Boot Decision Handler:
       ├── APPROVED
       │   └── Deduct/Credit Account Balance & Save Transaction
       ├── MANUAL_REVIEW
       │   └── Hold Balance & Save Transaction (200 OK)
       └── BLOCKED
           └── Hold Balance & Save Transaction → Return 403 Forbidden
```

# Core Business & Statutory Rules

## Statutory RBI PAN Requirement (Rule 114B)

Any transaction **≥ ₹50,000** strictly requires a valid Indian Permanent Account Number (PAN).

Spring Boot intercepts and rejects missing PAN requests immediately at the front door with `400 Bad Request`.

## KYC Registered PAN Matching

For transactions **> ₹50,000**, the submitted PAN is matched against the account holder's registered KYC PAN in PostgreSQL.

Any mismatch triggers:

```text
PAN_MISMATCH_SECURITY_ALERT
```

The transaction is instantly **BLOCKED (`403 Forbidden`)**.

## 30-Minute Rapid-Drain Protection

If a transfer **> ₹1,00,000** occurs within 30 minutes of a prior high-value transfer on the same account, the system flags:

```text
RAPID_HIGH_VALUE_DRAIN
```

The transaction is instantly blocked to prevent automated bot drains.

## Impossible Travel Velocity

If a transaction's geographic location changes from the account's previous location within an unrealistic timeframe, for example:

```text
Mumbai → Frankfurt in under 60 minutes
```

it triggers an emergency anomaly flag and is **BLOCKED**.

## Deposit ML Bypass

Deposits (`DEPOSIT`) represent incoming funds and bypass the spending anomaly model.

```text
ml_risk_score = 0.0
category      = ACCOUNT_DEPOSIT
confidence    = 100%
```

## Account Sanctions Freeze

Accounts marked with:

```text
AccountStatus.FROZEN
```

are rejected immediately with `403 Forbidden`.

# Entity Relationships

```text
┌──────────────────────────┐
│         Account          │
├──────────────────────────┤
│ id (PK)                  │
│ account_number (UNIQUE)  │
│ customer_name            │
│ balance                  │
│ registered_pan           │
│ status (ACTIVE, FROZEN)  │
└────────────┬─────────────┘
             │ 1
             │
             │ *
┌────────────▼─────────────┐
│       Transaction        │
├──────────────────────────┤
│ id (PK)                  │
│ account_id (FK)          │
│ amount                   │
│ type (DEPOSIT, WITHDRAW) │
│ pan_number               │
│ location                 │
│ decision                 │
│ timestamp                │
└──────────────────────────┘
```

# Project Structure

```text
sentinel-core/
│
├── sentinel-anchor/                        # Java Spring Boot 3 Core Backend
│   ├── src/main/java/com/sentinel/anchor/
│   │   ├── config/
│   │   │   └── RestClientConfig.java       # Spring 6 RestClient factory & socket timeouts
│   │   ├── controller/
│   │   │   └── PaymentController.java      # Payment authorization endpoint
│   │   ├── dto/
│   │   │   ├── TransactionRequestDTO.java  # Client request payload
│   │   │   ├── TransactionResultDTO.java   # Client response payload
│   │   │   ├── AiWorkerRequestDTO.java     # Payload sent to Python microservice
│   │   │   └── AiWorkerResponseDTO.java    # Payload received from Python
│   │   ├── exception/
│   │   │   ├── GlobalExceptionHandler.java # @RestControllerAdvice centralized handler
│   │   │   ├── AccountNotFoundException.java
│   │   │   ├── AccountFrozenException.java
│   │   │   ├── InsufficientBalanceException.java
│   │   │   └── AiServiceException.java     # Extracts Python HTTP error details
│   │   ├── entity/
│   │   │   ├── Account.java                # Account entity with KYC registered PAN
│   │   │   └── Transaction.java            # Clean financial ledger entity
│   │   ├── enums/
│   │   │   ├── AccountStatus.java           # ACTIVE, FROZEN
│   │   │   ├── TransactionDecision.java     # APPROVED, MANUAL_REVIEW, BLOCKED
│   │   │   └── TransactionType.java         # DEPOSIT, WITHDRAW (@JsonCreator enabled)
│   │   ├── repository/
│   │   │   ├── AccountRepository.java
│   │   │   └── TransactionRepository.java  # Baseline history & 30-min velocity query
│   │   ├── service/
│   │   │   ├── PaymentService.java          # Core ACID banking logic & orchestrator
│   │   │   └── AiWorkerClient.java          # Inter-service client calling Python
│   │   └── SentinelAnchorApplication.java   # Spring Boot runner & DB seeder
│   ├── src/main/resources/
│   │   └── application.properties           # DB credentials & AI worker URL config
│   ├── docker-compose.yml                    # PostgreSQL container definition
│   ├── pom.xml                               # Maven build configuration
│   └── .gitignore
│
└── ai-worker/                               # Python FastAPI Machine Learning Worker
    ├── venv/                                # Python virtual environment (ignored)
    ├── .env                                 # Gemini API key credentials (ignored)
    ├── .gitignore
    ├── models.py                            # Pydantic request/response data contracts
    ├── ml_service.py                        # Multi-Factor Isolation Forest anomaly engine
    ├── categorizer.py                       # Supervised Random Forest transaction categorizer
    ├── features.py                          # Pandas/NumPy behavioral feature extraction
    ├── ai_analyst.py                        # Google Gemini LLM SAR narrative generator
    └── main.py                              # FastAPI REST application & hybrid rules engine
```

# API Endpoints

## Spring Boot Anchor (`:8080`)

| Method | Endpoint | Request Body | Status Code | Description |
|---|---|---|---|---|
| `POST` | `/api/v1/payments/authorize` | `TransactionRequestDTO` | `200 OK / 403 Forbidden` | Authorize payment, run AI audit, and mutate balance |

## Python AI Worker (`:8000`)

| Method | Endpoint | Request Body | Status Code | Description |
|---|---|---|---|---|
| `GET` | `/health` | None | `200 OK` | Health check & market identifier |
| `POST` | `/api/v1/audit` | `TransactionData` | `200 OK` | Multimodal audit (RF + Isolation Forest + Gemini) |
| `GET` | `/api/v1/accounts/{id}/audits` | Query Params | `200 OK / 403 Forbidden` | Fetch account historical audit trail |

# API Payloads & Real-World Scenarios

## 1. Everyday Clean UPI Payment — APPROVED

### Request

```http
POST http://localhost:8080/api/v1/payments/authorize
Content-Type: application/json
```

```json
{
  "accountId": 1,
  "amount": 350.0,
  "type": "WITHDRAW",
  "location": "Mumbai, India",
  "panNumber": null
}
```

### Response — `200 OK`

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
  "complianceNote": "Account #1 transaction of ₹350.00 verified against baseline. Risk score of 8.5/100 indicates routine customer activity with no regulatory flags."
}
```

## 2. Missing PAN on High-Value Transaction — 400 Bad Request

### Request

```http
POST http://localhost:8080/api/v1/payments/authorize
Content-Type: application/json
```

```json
{
  "accountId": 1,
  "amount": 60000.0,
  "type": "WITHDRAW",
  "location": "Mumbai, India",
  "panNumber": null
}
```

### Response — `400 Bad Request`

```json
{
  "error": "VALIDATION_FAILED",
  "message": "RBI Compliance Violation: Transactions of ₹60000.0 (>= ₹50,000) strictly mandate a valid PAN number."
}
```

## 3. Impostor PAN Mismatch — 403 Forbidden

Registered KYC PAN on Account #1:

```text
ABCDE1234F
```

### Request

```http
POST http://localhost:8080/api/v1/payments/authorize
Content-Type: application/json
```

```json
{
  "accountId": 1,
  "amount": 65000.0,
  "type": "WITHDRAW",
  "location": "Mumbai, India",
  "panNumber": "XYZPK9999Z"
}
```

### Response — `403 Forbidden`

```json
{
  "transactionId": 2,
  "accountNumber": "ACC-1042",
  "amount": 65000.0,
  "updatedBalance": 49650.0,
  "status": "BLOCKED",
  "riskScore": 85.0,
  "category": "TRANSFER",
  "location": "Mumbai, India",
  "complianceNote": "High-risk alert: Transaction of INR 65,000.00 flagged for immediate freeze due to statutory PAN Mismatch between submitted identity XYZPK9999Z and registered account KYC records. Recommend filing a Suspicious Activity Report (SAR) with FIU-IND."
}
```

## 4. Account Deposit — 200 OK

### Request

```http
POST http://localhost:8080/api/v1/payments/authorize
Content-Type: application/json
```

```json
{
  "accountId": 1,
  "amount": 25000.0,
  "type": "DEPOSIT",
  "location": "Mumbai, India",
  "panNumber": null
}
```

### Response — `200 OK`

```json
{
  "transactionId": 3,
  "accountNumber": "ACC-1042",
  "amount": 25000.0,
  "updatedBalance": 74650.0,
  "status": "APPROVED",
  "riskScore": 0.0,
  "category": "ACCOUNT_DEPOSIT",
  "location": "Mumbai, India",
  "complianceNote": "Account #1 deposit of ₹25,000.00 successfully processed. Zero ML risk assigned to inward credits."
}
```

# Swagger / OpenAPI Documentation

Both microservices generate interactive OpenAPI documentation out of the box.

## Python AI Worker Swagger UI

```text
http://127.0.0.1:8000/docs
```

## Python OpenAPI JSON Specification

```text
http://127.0.0.1:8000/openapi.json
```

# Local Setup & Running

## Prerequisites

- Java 17 or 21
- Python 3.11+
- Docker Desktop
- Git

## Step 1: Start PostgreSQL with Docker

From the `sentinel-anchor` directory:

```bash
docker compose up -d
```

Verify the container is active:

```bash
docker ps
```

The project uses PostgreSQL on port `5332`.

If the `sentinel_db` database is not present, create it with:

```bash
docker exec -it postgres-db createdb -U postgres sentinel_db
```

## Step 2: Configure & Start Python AI Worker

Navigate to the `ai-worker` directory.

### 1. Create and activate virtual environment

```bash
python -m venv venv
```

Windows:

```powershell
.\venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install fastapi "uvicorn[standard]" pydantic scikit-learn numpy pandas google-genai python-dotenv
```

### 3. Create `.env` file

```env
GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY
```

### 4. Start the microservice

```bash
uvicorn main:app --reload
```

The Python AI Worker will start on:

```text
http://127.0.0.1:8000
```

## Step 3: Start Spring Boot Anchor

Open `sentinel-anchor` in your IDE or run it via Maven.

### Windows

```powershell
.\mvnw.cmd spring-boot:run
```

### Linux / macOS

```bash
./mvnw spring-boot:run
```

Spring Boot will start on:

```text
http://localhost:8080
```

It connects to PostgreSQL on port `5332` and auto-seeds Account #1 with a ₹50,000 balance.

# Testing & Verification

You can test the entire pipeline in IntelliJ or Postman or via PowerShell.

## PowerShell Example

```powershell
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/payments/authorize" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{
    "accountId": 1,
    "amount": 350.0,
    "type": "WITHDRAW",
    "location": "Mumbai, India",
    "panNumber": null
  }'
```

# Author

**Deendayal Nishad**

Electronics & Telecommunication Engineering Student | Aspiring Backend & AI/ML Engineer

**GitHub:** `@deendayal038`

# Support

If this architecture helped you understand distributed microservices pairing Spring Boot with Machine Learning, please give the repository a Star!
