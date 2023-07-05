from fastapi import FastAPI
from pydantic import BaseModel
import logging
from modules.logger import setup_logger
import openai
import json

# Setup logger
logger = logging.getLogger(__name__)
setup_logger(logger)

# Initialize the OpenAI ChatGPT model
openai.api_key = "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"
model_name = "gpt-3.5-turbo"

app = FastAPI()


class ChatInput(BaseModel):
    message: str


class ChatOutput(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat/test/spot")
async def chat(chat_input: ChatInput):
    user_message = "제주도 안에 지역을 추천 받고 싶어, " + chat_input.message + "라는 지역은 어때? 한글로 답해줘"
    print(f"Received a chat message: {user_message}")

    # Send user message to ChatGPT and get the model's response
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": user_message,
            }
            # },
            # {"role": "assistant", "content": "제주도는 한국의 아름다운 섬이야"},
        ],
    )

    print(completion)
    completion_json = json.loads(str(completion))
    content_msg = completion_json["choices"][0]["message"]["content"]
    print(content_msg)
    return ChatOutput(message=content_msg)


@app.post("/chat/test/mbti")
async def chat(chat_input: ChatInput):
    user_message = (
        "나의 성향을 알고 싶어, 나는 " + chat_input.message + "인데, MBTI 16가지 중에 뭘까? 한글로 답해줘"
    )
    print(f"Received a chat message: {user_message}")

    # Send user message to ChatGPT and get the model's response
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": user_message,
            }
            # },
            # {"role": "assistant", "content": "제주도는 한국의 아름다운 섬이야"},
        ],
    )

    print(completion)
    completion_json = json.loads(str(completion))
    content_msg = completion_json["choices"][0]["message"]["content"]
    print(content_msg)
    return ChatOutput(message=content_msg)
