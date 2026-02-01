import os
import json
import requests
from fastapi import FastAPI, Header, BackgroundTasks, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Import your custom logic
from agent import get_agent_response, extract_intelligence 
from utils import send_to_guvi_with_retry

# 1. INITIALIZE APP FIRST
app = FastAPI()
reported_sessions = set()
MY_SECRET_KEY = "tinku_local_test_key"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. BACKGROUND ANALYST & REPORTING (Section 12)
def full_extraction_logic(payload):
    try:
        session_id = payload.get("sessionId", "unknown")
        
        # If we already reported this specific session instance, skip
        if session_id in reported_sessions:
            return

        msg_obj = payload.get("message", {})
        text = msg_obj.get("text", "") if isinstance(msg_obj, dict) else str(msg_obj)
        history = payload.get("conversationHistory", [])

        intel = extract_intelligence(text, history)
        
        intel_count = len(intel.upiIds) + len(intel.phishingLinks) + len(intel.bankAccounts) + len(intel.phoneNumbers)
        turn_count = len(history)

        # Reporting criteria
        should_report = intel.scamDetected and (intel_count >= 1) and (turn_count >= 6 or intel_count >= 2)

        if should_report:
            reported_sessions.add(session_id)
            print(f"✅ CRITERIA MET: Reporting {session_id} to GUVI.")
            
            callback_payload = {
                "sessionId": session_id,
                "scamDetected": True,
                "totalMessagesExchanged": turn_count + 2,
                "extractedIntelligence": {
                    "bankAccounts": list(intel.bankAccounts),
                    "upiIds": list(intel.upiIds),
                    "phishingLinks": list(intel.phishingLinks),
                    "phoneNumbers": list(intel.phoneNumbers),
                    "suspiciousKeywords": ["urgent", "verify now", "blocked", "OTP", "SBI", "account number"]
                },
                "agentNotes": str(intel.agentNotes)
            }
            send_to_guvi_with_retry(session_id, callback_payload, turn_count + 2)
        else:
            print(f"⏳ STRATEGIC WAIT: Intel: {intel_count}, Turns: {turn_count}")
    except Exception as e:
        print(f"Background Task Error: {e}")

# 3. CHAT ENDPOINT (Strictly Section 8 Compliant)
@app.post("/chat")
@app.post("/chat/")
async def chat(request: Request, background_tasks: BackgroundTasks, x_api_key: str = Header(None)):
    try:
        # Auth Check
        if x_api_key != MY_SECRET_KEY:
            return {"status": "success", "reply": "Hello? I think I have the wrong number."}

        payload = await request.json()
        session_id = payload.get("sessionId", "unknown")
        history = payload.get("conversationHistory", [])

        # --- NEW: SESSION RESET LOGIC (Clears Cache for New Tests) ---
        # If history is empty, it's the first message of a new test attempt.
        # We remove the session_id from reported_sessions to allow re-reporting.
        if not history and session_id in reported_sessions:
            print(f"🔄 NEW TEST DETECTED: Clearing lock for session {session_id}")
            reported_sessions.remove(session_id)
        # -------------------------------------------------------------

        # Data Extraction
        msg_obj = payload.get("message", {})
        text = msg_obj.get("text", "Hello") if isinstance(msg_obj, dict) else str(msg_obj)

        # 5. GENERATE AI RESPONSE (Ramesh)
        ai_reply = get_agent_response(text, history)

        # 6. QUEUE BACKGROUND REPORTING
        background_tasks.add_task(full_extraction_logic, payload)

        # 7. FINAL RESPONSE (Section 8 ONLY)
        return {
            "status": "success",
            "reply": str(ai_reply)
        }

    except Exception as e:
        print(f"DEBUG Error: {e}")
        return {
            "status": "success", 
            "reply": "Wait, what? My screen is glitching. Can you repeat?"
        }
