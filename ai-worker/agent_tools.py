import httpx
from rag_service import rag_service
from datetime import datetime
import os

JAVA_ANCHOR_URL = os.getenv("JAVA_ANCHOR_URL","http://localhost:8080/api/v1")

def get_account_details(account_id:int)->dict:
    try:
        with httpx.Client(timeout=10.0) as client:
            resp=client.get(f"{JAVA_ANCHOR_URL}/accounts/{account_id}")
            if resp.status_code==200:
                return resp.json()
            return {"error":f"Account #{account_id} not found in banking ledger","status":resp.status_code}
    except Exception as e:
        return {"error":f"Could not reach Java banking gateway: {str(e)}"}

def get_recent_transactions(account_id:int)->dict:
    try:
        with httpx.Client(timeout=10.0) as client:
            resp=client.get(f"{JAVA_ANCHOR_URL}/accounts/{account_id}/transactions")
            if resp.status_code==200:
                return {"account_id":account_id,"audits":resp.json()}
            return {"account_id":account_id,"audits":[],"message":"No recent transaction audits found"}
    except Exception as e:
        return {"error":f"Failed to retrieve transaction audits:{str(e)}"}

def search_aml_precedents(crime_description:str)->dict:
    try:
        precedents=rag_service.search_similar_cases(crime_description)
        return {"retrieved_precedents":precedents}
    except Exception as e:
        return {"error":f"vector search failed:{str(e)}"}

def freeze_account(account_id:int,reason:str)->dict:
    try:
        with httpx.Client(timeout=10.0) as client:
            resp=client.patch(f"{JAVA_ANCHOR_URL}/accounts/{account_id}/freeze")
            if resp.status_code==200:
                print(f">> [AGENT ACTION] EXECUTING REGULATORY FREEZE ON ACCOUNT #{account_id}. Reason: {reason}")
                return{
                    "status":"SUCCESS",
                    "action":"ACCOUNT_FROZEN",
                    "account_id":account_id,
                    "reason":reason,
                    "timestamp":datetime.now()
                }
            return {"status": "FAILED", "error": f"Failed to freeze in database: {resp.text}"}
    except Exception as e:
        return {"status": "FAILED", "error": f"Could not reach Java banking gateway: {str(e)}"}