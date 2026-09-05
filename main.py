from fastapi import FastAPI
from agent import SelfLearningAgent
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import File, UploadFile
from llm import transcribe_audio
import shutil
import os

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


@app.post("/transcribe")
async def transcribe_endpoint(audio: UploadFile = File(...)):
    temp_path = f"temp_{audio.filename}"
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    
    text = transcribe_audio(temp_path)

    os.remove(temp_path)
    
    return {"text": text}