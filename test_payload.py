import json
from pydantic import BaseModel

# This structure MUST match Section 12 exactly
class GUVIRequirement(BaseModel):
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: dict  # This will contain our sub-fields
    agentNotes: str

def verify_structure():
    # Example data from your Agent
    test_intel = {
        "bankAccounts": ["123456789"],
        "upiIds": ["scam@upi"],
        "phishingLinks": ["http://fake.link"],
        "phoneNumbers": ["+9100000000"],
        "suspiciousKeywords": ["blocked", "urgent"]
    }

    # Construct the final payload
    payload = {
        "sessionId": "abc-123",
        "scamDetected": True,
        "totalMessagesExchanged": 5,
        "extractedIntelligence": test_intel,
        "agentNotes": "Scammer used fear tactics."
    }

    try:
        # Validate against the requirement model
        GUVIRequirement(**payload)
        print("✅ SUCCESS: Payload structure meets requirements.")
        print(json.dumps(payload, indent=2))
    except Exception as e:
        print(f"❌ ERROR: Payload structure is invalid: {e}")

if __name__ == "__main__":
    verify_structure()