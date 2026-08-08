import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# --------------------------------------------------
# ログ設定
# --------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AI_Yato")


# --------------------------------------------------
# FastAPI
# --------------------------------------------------

app = FastAPI(
    title="AI_Yato API",
    version="0.1.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str


# --------------------------------------------------
# Response
# --------------------------------------------------

class ChatResponse(BaseModel):
    speaker_ID: str
    emotion_ID: str
    message: str


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "AI_Yato backend OK"
    }


# --------------------------------------------------
# Chat
# --------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info("USER: %s", request.message)

    return ChatResponse(
        speaker_ID="AI_100_010_010",
        emotion_ID="Normal",
        message="お、来たな。Pythonまでちゃんと届いてるぞ。",
    )