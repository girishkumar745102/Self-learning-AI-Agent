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
    user_id: str
agents = {}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        if request.user_id not in agents:
            agents[request.user_id]= SelfLearningAgent(user_id=request.user_id)

        user_agent = agents[request.user_id]
        reply = user_agent.chat(request.message)
    
        return {"reply": reply}

    except Exception as e:
        return {"error": "Something went wrong. Please try again." , "details": str(e)}

