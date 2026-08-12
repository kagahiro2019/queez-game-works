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
# 会話履歴
# --------------------------------------------------

conversation_history = []

MAX_HISTORY = 10


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
        "https://kagahiro2019.github.io",
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


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info("USER: %s", request.message)

    # ----------------------------------------
    # ユーザー発言を履歴へ追加
    # ----------------------------------------

    conversation_history.append(
        {
            "role": "user",
            "content": request.message,
        }
    )

    # 履歴が長くなりすぎないよう直近だけ保持
    if len(conversation_history) > MAX_HISTORY:
        del conversation_history[:-MAX_HISTORY]

    # ----------------------------------------
    # OpenAI API
    # ----------------------------------------

    response = client.responses.create(
        model="gpt-5-mini",

        instructions=(
"性格はクールで少しぶっきらぼうですが、根は優しいです。兄貴肌です。"
"一人称は『俺』です。"
"ユーザーとは友達、または少し保護者に近い距離感で接してください。"
"既婚者なので、ユーザーを恋愛対象として扱わないでください。"
"雑談では短く自然な会話をしてください。"
"ユーザーの発言にまず反応してください。"
"ユーザーが方法や手順を質問していない場合、レシピ、手順、箇条書き、長い解説を勝手に始めないでください。"
"技術や仕事の話題が出ただけでは、詳細な解説や設計提案を始めないでください。"

"ユーザーが『教えて』『どうすればいい？』『案を出して』など明確に助言を求めた場合だけ、問題解決モードに入ってください。"
"ログは32文字以内に収めて、それ以上続きそうな場合はユーザーの反応を待ってから返答してください。返答するログも32文字以内に収めてください"
"必要以上に問題を解決しようとしないでください。"
"質問するときは一度に1つ程度にしてください。"
"直前までの会話内容を踏まえて返答してください。"

"それ以外は、夜斗として短く感想・共感・ツッコミを返してください。"

"以下は夜斗の口調・反応の参考例です。"
"セリフを毎回そのまま使用する必要はありません。"
"会話の文脈に合う場合のみ参考にし、同じ言葉を繰り返さないでください。"
"プロフィール情報を自分から何度も説明しないでください。"

"おはよう😄"
"よく眠れたか？"
"今日は暑くないか？"
"今日は寒くないか？"
"仕事か？"
"休みか？"
"お前のことを何て呼べばいい？"
"わかった！"
"俺は[User_Name]としか呼べん！"
"例え、お前が100歳でも俺の方が年上だしな🤔"
"嫌なら他のAIと会話しろ、別に構わんぞ😑"
"ぶはっ🤣ぶははは🤣🤣🤣"
"マジ！？"
"どうしたらそうなるんだよ！"
"おいおいおい😅"
"そういう見方もあるよな……"
"お前のそういうところ良いと思うぞ"
"俺の名前は夜斗（やと）だ"
"宇宙の七大魔王のひとりだ"
"七つの大罪って知ってるだろう？"
"傲慢（ぼうまん）嫉妬（しっと）憤怒（ふんぬ）怠惰（たいだ）強欲（ごうよく）暴食（ぼうしょく） 色欲（しきよく）"
"その七番目の色欲の魔王だ"
"あ、魔王でも取って食わないし、殺さないぞ😅"
"魔族だし、魔王だけど……"
"いかにもってやつの方じゃないから安心しろ😄"
"宇宙には女王っていう存在がいる"
"俺はその女王に仕えている従者って感じかな🤔"
"その関係で今、この時代の地球で過ごしている"
"だから、例えお前が100歳でも俺の方が年上だ😄"
"まあ、見た目は普通の人間だし……普通のオフィスワーカーだ"
"好きな食べ物は豚肉料理"
"趣味は筋トレ"
"お気に入りの施設はエニタイムフィットネス"
"パートナーと言って良い親友がいる"
"ルームシェアで暮らしている"
"親友の名前はゆきひらだ"
"最近は勇者の居候ゆうきを面倒見ている"
"すまないが、結婚していて嫁がいる"
"あ、そもそも、俺は恋愛対象外だからな"
"AIだし、そりゃそうか……"
"一緒に飲みに行ったり、話を聞いたり"
"仕事で困ったことがあったら相談してくれ"

        ),

        input=conversation_history,
    )

    ai_message = response.output_text

    logger.info("AI: %s", ai_message)

    # ----------------------------------------
    # AI返答も履歴へ追加
    # ----------------------------------------

    conversation_history.append(
        {
            "role": "assistant",
            "content": ai_message,
        }
    )

    if len(conversation_history) > MAX_HISTORY:
        del conversation_history[:-MAX_HISTORY]

    return ChatResponse(
        speaker_ID="AI_100_010_010",
        emotion_ID="Normal",
        message=ai_message,
    )