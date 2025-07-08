from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
import random

app = FastAPI(
    title="Emotion Reflection API",
    description="Analyzes short text input and returns a mock emotional response.",
    version="1.0.0"
)

# === Allow Frontend Access ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⛔ Replace with your frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Schemas ===
class TextInput(BaseModel):
    text: str = Field(..., min_length=3, max_length=300, example="I feel nervous about my job interview")

class EmotionResult(BaseModel):
    emotion: Literal["Happy", "Sad", "Anxious", "Excited", "Calm"]
    confidence: float

# === GET / Root Route ===
@app.get("/")
def read_root():
    return {"message": "Emotion Reflection API is running 🚀"}

# === POST /analyze Route ===
@app.post("/analyze", response_model=EmotionResult)
def analyze_text(input: TextInput):
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    emotions = ["Happy", "Sad", "Anxious", "Excited", "Calm"]
    emotion = random.choice(emotions)
    confidence = round(random.uniform(0.7, 0.99), 2)

    return EmotionResult(emotion=emotion, confidence=confidence)

