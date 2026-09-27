from fastapi import FastAPI
from agent import SelfLearningAgent
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import File, UploadFile
from llm import transcribe_audio
import shutil
import os
from database import SessionLocal, User
from auth import hash_password


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

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

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

@app.post("/signup")
def signup(request: SignupRequest):
    db = SessionLocal()
    try:
        # Check kar username ya email pehle se exist toh nahi karta
        existing_user = db.query(User).filter(
            (User.username == request.username) | (User.email == request.email)
        ).first()

        if existing_user:
            return {"error": "Username or email already registered"}

        # Password hash kar aur naya user bana
        hashed_pw = hash_password(request.password)
        new_user = User(
            username=request.username,
            email=request.email,
            hashed_password=hashed_pw
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "Signup successful", "user_id": new_user.id}

    except Exception as e:
        db.rollback()
        return {"error": "Something went wrong", "details": str(e)}

    finally:
        db.close()