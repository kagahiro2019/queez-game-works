import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel


# --------------------------------------------------
# ログ設定
# --------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AI_Yato")


# --------------------------------------------------
# OpenAI
# OPENAI_API_KEY はWindows環境変数から自動取得
# --------------------------------------------------

client = OpenAI()


# --------------------------------------------------
# FastAPI
# --------------------------------------------------

app = FastAPI(
    title="AI_Yato API",
    version="0.2.0",
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
# Request / Response
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str


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

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=(
            "日本語で短く返答してください。"
            "これはAPI疎通確認なので、人格設定はまだ不要です。"
        ),
        input=request.message,
    )

    ai_message = response.output_text

    logger.info("AI: %s", ai_message)

    return ChatResponse(
        speaker_ID="AI_100_010_010",
        emotion_ID="Normal",
        message=ai_message,
    )