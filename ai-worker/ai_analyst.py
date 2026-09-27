import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class AIComplianceAnalyst:

    def __init__(self):
        self.api_key=os.getenv("GEMINI_API_KEY")
        self.client=None

        if self.api_key:
            try:
                self.client=genai.Client(api_key=self.api_key)
                print(">> [AI Analyst] connected to google gemini api")
            except Exception as e:
                print(f"[AI Analyst] failed to initialize gemini: {e}")

        else:
            print(">> [AI Analyst] no gemini api key found. Running in smart fallback mode")

    def generate_narrative(self,tx_data:dict,final_decision:str, predicted_category:str, is_anomaly:bool,ml_risk_score:float,rules:list[str])->str:
        """
        Generates a 2-sentence executive compliance summary for bank auditors
        """

        if self.client:
            try:
                prompt=f"""
                You are a Senior Anti-Money Laundering(AML) compliance officer at Bank in India.
                Analyze this transaction and write a strict 2-sentence executive audit summary:
                -Account ID: {tx_data.get('account_id')}
                -Amount: {tx_data.get('amount'):,.2f} INR
                -International: {tx_data.get('is_international')}
                -Final Decision: {final_decision}
                -Predicted Category: {predicted_category}
                -ML Isolation Forest Anomaly: {is_anomaly} (Risk Score: {ml_risk_score}/100)
                -Rules Triggered: {', '.join(rules) if rules else 'None'}

                If there is a PAN Mismatch, Rapid High-Value Drain,or Impossible travel, explicitly state the security breach and recommend an immediate account freeze.
                Write only 2 professional, regulatory-focused sentences explaining the risk and recommended action.
                """
                response=self.client.models.generate_content(
                    model='gemini-3.5-flash-lite',
                    contents=prompt,
                )
                if response and response.text:
                    return response.text.strip()

            except Exception as err:
                print(f">>[AI Analyst] LLM call failed, falling back:{err}")

        if ml_risk_score>=70 or len(rules)>0:
            reasons=f"Triggered rules {'; '.join(rules)}." if rules else "Statistical anomaly detected by ML."

            return (
                f"High risk alert for account #{tx_data.get('account_id')} involving ₹{tx_data.get('amount'):,.2f}."
                f"{reasons} Recommend immediate freeze and submission of suspicious activity report(SAR) to compliance."
            )

        else:
            return(
                f"Account #{tx_data.get('acoount_id')} transaction of {tx_data.get('amount'):,.2f} verified against baseline"
                f"Risk score of {ml_risk_score}/100 indicates routine customer activity with no regulatory flags"
            )

ai_analyst=AIComplianceAnalyst()