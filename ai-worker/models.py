import re
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime

# Request DTO (with validation rules)
class TransactionData(BaseModel):
    account_id: int=Field(...,description="Unique account identifier")
    amount: float=Field(...,gt=0,description="Amount must be positive")
    transaction_type:str=Field(description="DEPOSIT or WITHDRAW")
    timestamp:datetime=Field(default_factory=datetime.now, description="ISO-8601 transaction timestamp")
    pan_number:str | None=Field(default=None,description="PAN required for amount >=50000")
    registered_pan:str | None=Field(default=None)
    location:str= Field(default="Mumbai, India", description="City / Country of transaction")
    ip_address:str | None = Field(default=None, description="Client IP address")
    last_known_location: str | None = Field(default="Mumbai, India", description="Location of previous transaction")
    minutes_since_last_tx: float | None = Field(default=None, description="Minutes elapsed since previous transaction")
    past_amounts:list[float]=Field(default=[],description="Recent transaction amounts from database to establish baseline")
    has_recent_high_value_tx:bool= Field(default=False, description="True if a >₹1,00,000 tx occurred in last 30 mins")

    # Property helpers: Python extracts hour and weekend automatically!
    @property
    def hour(self)->int:
        return self.timestamp.hour

    @property
    def is_weekend(self)->bool:
        return self.timestamp.weekday()>=5

    @property
    def is_night(self)->bool:
        return self.timestamp.hour>=0 and self.timestamp.hour<=5

    @property
    def is_international(self)->bool:
        # Auto-detects if location is outside India
        indian_keywords=["INDIA", "IN", "MUMBAI", "DELHI", "BANGALORE", "BENGALURU", "PUNE", "HYDERABAD", "CHENNAI", "KOLKATA"]
        loc_upper=self.location.upper()
        return not any(keyword in loc_upper for keyword in indian_keywords)

    @field_validator("pan_number")
    @classmethod
    def validate_pan(cls, v: str | None) -> str | None:
        if not v:  # Handles None or empty string ""
            return None
        
        cleaned_pan = v.strip().upper()
        pan_regex = r"^[A-Z]{5}[0-9]{4}[A-Z]$"
        
        # Notice the 'not' here!
        if not re.match(pan_regex, cleaned_pan):
            raise ValueError("Invalid PAN format! Must match pattern ABCDE1234F (5 letters, 4 digits, 1 letter).")
        
        return cleaned_pan

    # @model_validator(mode="after")
    # def pan_required(self)-> "TransactionData":
    #     if self.amount>=50000 and not self.pan_number:
    #         raise ValueError(f"Transaction of ₹{self.amount:,.2f} is >=₹50000. PAN is Mandatory")
    #     return self


# Response DTO (clean contract for Spring Boot)
class AuditResponse(BaseModel):
    account_id:int
    amount:float

    # From Supervised Random Forest (Categorizer)
    predicted_category:str=Field(...,description="FOOD_DINING, UTILITIES_BILLS, INVESTMENT_WEALTH, TRAVEL_FUEL, ENTERTAINMENT")
    predicted_confidence:float=Field(...,description="Confidence score from 0.0% to 100.0%")

    # From Feature Engineering (Pandas / NumPy)
    amount_to_mean_ratio:float=Field(...,description="Ratio of current amount to customer's historical average")
    is_night_transaction:bool  

    # From Unsupervised Isolation Forest (ML Anomaly)
    ml_risk_score: float=Field(...,description="ML risk score form 0.0 to 100.0")
    is_anomaly:bool=Field(...,description="Statistical outlier flag from isolation forest")
    final_decision:str=Field(...,description="APPROVED,MANUAL REVIEW or BLOCKED")
    rules_triggered:list[str]=Field(default=[],description="List of rule violation detected")
    recommendation:str

    # From Generative AI (Gemini LLM)
    ai_compliance_narrative: str=Field(...,description="Executive AI generated SAR narrative for auditors")