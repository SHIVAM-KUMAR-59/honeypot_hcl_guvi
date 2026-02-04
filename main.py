from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Literal

from agent import get_agent_response

app = FastAPI()


# -------- Request Models (STRICTLY MATCH SPEC) -------- #

class Message(BaseModel):
    sender: Literal["scammer", "user"]
    text: str
    timestamp: int  # Epoch ms


class Metadata(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = None
    locale: Optional[str] = None


class IncomingRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Message]] = None
    metadata: Optional[Metadata] = None

    class Config:
        extra = "allow"   # prevents tester crashes


# -------- Honeypot Endpoint -------- #

@app.post("/honeypot")
async def honeypot(request: IncomingRequest):

    # Safe history fallback
    history = request.conversationHistory or []

    # Generate reply (agent only needs text + history)
    reply = get_agent_response(
        message=request.message.text,
        history=[h.dict() for h in history]
    )

    # ⚠️ RESPONSE MUST MATCH SECTION 8 EXACTLY
    return {
        "status": "success",
        "reply": reply
    }
