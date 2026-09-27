from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import TransactionData, AuditResponse
from ml_service import fraud_model
from ai_analyst import ai_analyst
from categorizer import categorizer
from features import extract_behavioral_features

# Initialize the application (like @SpringBootApplication)
app=FastAPI(
    title="SentinelCore AI worker",
    description="Microservice for Financial Risk & AI Auditing",
    version= "1.0.0"
)

class AccountFrozenException(Exception):
    def __init__(self,account_id:int,reason:str):
        self.account_id=account_id
        self.reason=reason

@app.exception_handler(AccountFrozenException)
def handle_frozen_account(request ,e: AccountFrozenException):
    return JSONResponse(
        status_code=403,
        content={
            "error_code":"Account sanctioned or frozen",
            "account_id":e.account_id,
            "message":e.reason,
            "requested_url":str(request.url)
        }
    )

# A simple GET health-check endpoint (like @GetMapping("/health"))
@app.get("/health")
def health_check():
    return {"status":"UP","service":"ai-worker"}

@app.get("/api/accounts/{account_id}/audits")
def acc_audit_history(
    account_id:int,
    limit: int=10,
    flagged_only:bool=False
):
    if account_id==9999:
        raise AccountFrozenException(
            account_id=account_id,
            reason="This account is under active regulatory freeze by FIU-IND compliance orders."
        )
    return {
        "account_id":account_id,
        "limit_applied":limit,
        "flagged_only_filter":flagged_only,
        "message": f"Retrieved last {limit} audit records for account #{account_id}"
    }

# A POST endpoint receiving our DTO (like @PostMapping("/api/v1/audit"))
@app.post("/api/v1/audit",response_model=AuditResponse)
def audit_transaction(tx: TransactionData):
    rules_triggered=[]

    # Auto-detected from Timestamp
    tx_hour=tx.hour
    tx_weekend=tx.is_weekend
    tx_international=tx.is_international
    tx_night=tx.is_night
    is_deposit=(tx.transaction_type.upper()=="DEPOSIT")

    if tx.amount>=50000:
        if not tx.pan_number:
            rules_triggered.append("MISSING_PAN: Transfer > ₹50,000 strictly requires PAN submission under RBI/PMLA rules.")
        elif tx.registered_pan:
            clean_submitted=tx.pan_number.strip().upper()
            clean_reg=tx.registered_pan.strip().upper()
            if clean_submitted!=clean_reg:
                rules_triggered.append(
                    "PAN_MISMATCH_SECURITY_ALERT: Submitted PAN does NOT match account holder KYC PAN!"
                )

    if tx.amount>=100000 and tx.has_recent_high_value_tx:
        rules_triggered.append("RAPID_HIGH_VALUE_DRAIN: Repeated >₹1,00,000 transfer attempted within 30 minutes of prior high-value transfer!")

    # Location & Impossible Travel Velocity Rule
    if tx.last_known_location and tx.minutes_since_last_tx is not None:
        if tx.location.lower()!=tx.last_known_location.lower() and tx.minutes_since_last_tx<20:
            rules_triggered.append(
                f"IMPOSSIBLE_TRAVEL: location changed from '{tx.last_known_location}' to '{tx.location}'"
                f"in only {tx.minutes_since_last_tx:.0f} minutes" 
            )

    # 1. Feature Engineering (Pandas / NumPy)
    behavior=extract_behavioral_features(
        current_amount=tx.amount,
        past_amounts=tx.past_amounts,
        is_night=tx_night
    )

    # 2. Supervised Classification (Random Forest Categorizer)
    if is_deposit:
        pred_category="Account Deposit"
        cat_confidence=100.0
    else:
        pred_category,cat_confidence=categorizer.predict_category(
            amount=tx.amount,
            hour=tx_hour,
            is_weekend=tx_weekend
        )

    # 3. Deterministic Hard Rules

    if not is_deposit and tx.amount>=200000:
        rules_triggered.append("Transaction >=200000 requires KYC mandate")

    if behavior["amount_to_mean_ratio"]>10.0:
        rules_triggered.append(f"Transaction is {behavior['amount_to_mean_ratio']}x higher than the customer average transaction amount")

    if tx_night and tx.amount>=50000:
        rules_triggered.append("High-value transaction")


    # 4. Unsupervised ML Anomaly Detection (Isolation Forest)
    if is_deposit:
        is_anomaly=False
        ml_risk=0.0
    else:
        is_anomaly,ml_risk=fraud_model.evaluate_risk(
            amount=tx.amount,
            amount_to_mean_ratio=behavior["amount_to_mean_ratio"],
            is_night=tx_night,
            is_international=tx_international
        )

    has_critical_sacurity_violation=any(
        k in r for r in rules_triggered for k in ["PAN_MISMATCH", "RAPID_HIGH_VALUE_DRAIN", "IMPOSSIBLE_TRAVEL"]
    )

    # 5. Hybrid Decision Logic
    if has_critical_sacurity_violation or ml_risk>=85 or (tx.amount>=200000 and tx.is_international):
        final_decision="BLOCKED"
        recommendation="Immediate account lock. Escalate to AML compliance unit."

    elif tx.amount<=2000 and ml_risk<70 and pred_category in ["TRAVEL_FUEL","FOOD_DINING"]:
        final_decision="APPROVED"
        is_anomaly= False
        ml_risk=min(ml_risk,37.0)
        recommendation="Low-value routine retail transaction authorized under frictionless rails."

    elif is_anomaly and ml_risk>=45 and len(rules_triggered)>0:
        final_decision="MANUAL_REVIEW"
        recommendation="Hold settlement. Trigger 2-factor OTP verification to account holder"

    else:
        final_decision="APPROVED"
        recommendation="Transaction authorized with low risk profile"

    # 6. Generative AI Narrative (passes category and ratio to LLM)
    enriched_tx_data={
        **tx.model_dump(),
        "category":pred_category,
        "ratio_to_avg":behavior["amount_to_mean_ratio"],
        "critical_violations": [r for r in rules_triggered if any(k in r for k in ["PAN_MISMATCH", "RAPID_HIGH_VALUE_DRAIN", "NPCI"])]
    }

    ai_narrative=ai_analyst.generate_narrative(
        tx_data=enriched_tx_data,
        final_decision=final_decision,
        predicted_category=pred_category,
        is_anomaly=bool(is_anomaly),
        ml_risk_score=float(ml_risk),
        rules=rules_triggered
    )

    return AuditResponse(
        account_id=tx.account_id,
        amount=tx.amount,
        predicted_category=pred_category,
        predicted_confidence=cat_confidence,
        amount_to_mean_ratio=behavior["amount_to_mean_ratio"],
        is_night_transaction=tx_night,
        ml_risk_score=float(ml_risk),
        is_anomaly=bool(is_anomaly),
        final_decision=final_decision,
        rules_triggered=rules_triggered,
        recommendation=recommendation,
        ai_compliance_narrative=ai_narrative
    )