import os
import requests
import time
import json
from dotenv import load_dotenv

load_dotenv()

GUVI_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_to_guvi_with_retry(session_id: str, intel: dict, total_msgs: int, max_retries: int = 3):
    """
    Sends the final extraction report to GUVI with exponential backoff logic.
    """
    payload = {
        "sessionId": session_id,
        "scamDetected": intel.get("scamDetected", False),
        "totalMessagesExchanged": total_msgs,
        "extractedIntelligence": {
            "bankAccounts": intel.get("bankAccounts", []),
            "upiIds": intel.get("upiIds", []),
            "phishingLinks": intel.get("phishingLinks", []),
            "phoneNumbers": intel.get("phoneNumbers", []),
            "suspiciousKeywords": intel.get("suspiciousKeywords", [])
        },
        "agentNotes": intel.get("agentNotes", "No notes provided.")
    }

    for attempt in range(max_retries):
        try:
            print(f"DEBUG: [Attempt {attempt+1}] Sending report for session {session_id}...")
            response = requests.post(GUVI_URL, json=payload, timeout=10)
            
            if response.status_code == 200:
                print(f"SUCCESS: Report accepted by GUVI for {session_id}")
                return True
            else:
                print(f"WARN: GUVI returned {response.status_code}: {response.text}")
        
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Connection failed: {e}")

        # Exponential Backoff: Wait 2s, 4s, 8s...
        wait_time = 2 ** (attempt + 1)
        time.sleep(wait_time)



    print("--- [FINAL JSON AUDIT] ---")
    print(json.dumps(payload, indent=2))
    print("--------------------------")

    print(f"CRITICAL: Failed to send report after {max_retries} attempts.")
    return False