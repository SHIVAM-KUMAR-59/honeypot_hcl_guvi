from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Literal

from agent import get_agent_response

app = FastAPI()


# -------- Models -------- #

class Message(BaseModel):
    sender: Literal["scammer", "user"]
    text: str
    timestamp: int


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
        extra = "allow"


# -------- Endpoint -------- #

@app.post("/honeypot")
async def honeypot(request: IncomingRequest):

    # Safe fallback
    history = request.conversationHistory or []

    # Pydantic v2 SAFE conversion
    history_dict = [msg.model_dump() for msg in history]

    reply = get_agent_response(
        message=request.message.text,
        history=history_dict
    )

    return {
        "status": "success",
        "reply": str(reply)
    }
