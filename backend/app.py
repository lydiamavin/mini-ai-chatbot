from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fuzzywuzzy import fuzz, process
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

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

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

# -----------------------
# API Endpoint
# -----------------------
@app.post("/ask")
def ask(q: Question):
    question = q.question.strip()

    # Load chat history (last 3 interactions for context)
    history = load_history()
    context = "\n".join([f"Q: {h['question']}\nA: {h['answer']}" for h in history[-3:]])

    # Step 1: Fuzzy match against KB
    match = process.extractOne(question, kb.keys(), scorer=fuzz.ratio)
    if match and len(match) >= 2:
        best_match, score = match[0], match[1]
        if score >= 50:
            answer = kb.get(best_match)
        else:
            answer = None  # Fallback
    else:
        answer = None  # Fallback

    if answer is None:
        # Fallback message
        answer = "I'm sorry, I don't have information on that. Please consult a professional."

    # Save conversation in history
    history.append({"question": question, "answer": answer})
    save_history(history)

    return {"answer": answer}

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.get("/{path:path}")
async def serve_spa(path: str):
    return FileResponse('static/index.html')
