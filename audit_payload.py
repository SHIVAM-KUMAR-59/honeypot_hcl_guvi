from pydantic import BaseModel, Field
from typing import List

# This class replicates the EXACT requirements of Section 12
class ExtractedIntelligenceSchema(BaseModel):
    bankAccounts: List[str]
    upiIds: List[str]
    phishingLinks: List[str]
    phoneNumbers: List[str]
    suspiciousKeywords: List[str]

class FinalCallbackSchema(BaseModel):
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: ExtractedIntelligenceSchema
    agentNotes: str

def audit_my_data(data_to_test):
    try:
        FinalCallbackSchema(**data_to_test)
        print("✅ VALIDATION SUCCESS: Your payload matches GUVI Section 12 exactly.")
    except Exception as e:
        print(f"❌ VALIDATION FAILED: {e}")

# Example of what your code is generating:
test_data = {
    "sessionId": "eval-session-999",
    "scamDetected": True,
    "totalMessagesExchanged": 4,
    "extractedIntelligence": {
        "bankAccounts": [],
        "upiIds": ["verify@okicici"],
        "phishingLinks": ["http://scam.link"],
        "phoneNumbers": [],
        "suspiciousKeywords": ["blocked", "verify"]
    },
    "agentNotes": "Scammer used urgency tactics."
}

audit_my_data(test_data)