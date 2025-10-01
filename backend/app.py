from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fuzzywuzzy import fuzz, process
from transformers import pipeline
import json
import os

app = FastAPI()

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend build (React Vite -> dist/)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/")
    async def serve_frontend():
        return FileResponse("static/index.html")

# -----------------------
# Models & Files
# -----------------------
class Question(BaseModel):
    question: str

KB_FILE = "knowledge_base.json"
HISTORY_FILE = "history.json"

def load_kb():
    with open(KB_FILE) as f:
        return json.load(f)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# Load KB into memory
kb = load_kb()

# Lazy init for LLM
generator = None

# -----------------------
# API Endpoint
# -----------------------
@app.post("/ask")
def ask(q: Question):
    global generator
    question = q.question.strip()

    # Load chat history (last 3 interactions for context)
    history = load_history()
    context = "\n".join([f"Q: {h['question']}\nA: {h['answer']}" for h in history[-3:]])

    # Step 1: Fuzzy match against KB
    best_match, score = process.extractOne(question, kb.keys(), scorer=fuzz.ratio)
    if score >= 70:
        answer = kb[best_match]
    else:
        # Step 2: Fall back to LLM if KB doesn’t match
        if generator is None:
            try:
                generator = pipeline("text-generation", model="distilgpt2")
            except Exception as e:
                return {"answer": "I'm sorry, I don't have information on that. Please consult a professional."}

        try:
            prompt = f"Answer professionally: {question}\n{context}"
            response = generator(
                prompt,
                max_length=150,
                num_return_sequences=1,
                truncation=True,
                do_sample=True,
                temperature=0.7,
            )
            generated = response[0]["generated_text"]
            answer = generated.replace(prompt, "").strip()
            if not answer:
                answer = generated.strip()
        except Exception:
            answer = "I'm sorry, I don't have information on that. Please consult a professional."

    # Save conversation in history
    history.append({"question": question, "answer": answer})
    save_history(history)

    return {"answer": answer}
