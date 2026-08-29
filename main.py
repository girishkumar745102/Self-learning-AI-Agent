from fastapi import FastAPI
from agent import SelfLearningAgent
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
agent = SelfLearningAgent(user_id="web_user")

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    reply = agent.chat(request.message)
    return {"reply": reply}

