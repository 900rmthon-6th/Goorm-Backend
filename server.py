from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging
from modules.logger import setup_logger
import openai

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

@app.post("/chat")
async def chat(chat_input: ChatInput):
    user_message = "제주도에서 " + chat_input.message
    logger.info(f"Received a chat message: {user_message}")

    # Send user message to ChatGPT and get the model's response
    response = openai.Completion.create(
        engine=model_name,
        prompt=user_message,
    )

    model_response = response.choices[0].text.strip()

    return ChatOutput(message=model_response)