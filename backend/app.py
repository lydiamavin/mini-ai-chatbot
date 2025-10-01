from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from fuzzywuzzy import fuzz, process
from transformers import pipeline
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


app = FastAPI()

# Serve frontend build
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

kb = load_kb()
generator = None

@app.post("/ask")
def ask(q: Question):
    question = q.question
    history = load_history()
    context = "\n".join([f"Q: {h['question']}\nA: {h['answer']}" for h in history[-3:]])

    best_match, score = process.extractOne(question, kb.keys(), scorer=fuzz.ratio)
    if score > 70:
        answer = kb[best_match]
    else:
        global generator
        if generator is None:
            try:
                generator = pipeline('text-generation', model='distilgpt2')
            except Exception:
                generator = None
                answer = "I'm sorry, I don't have information on that. Please consult a professional."
                return
        prompt = f"Answer professionally: {question}"
        try:
            response = generator(prompt, max_length=150, num_return_sequences=1, truncation=True, do_sample=True, temperature=0.7)
            generated = response[0]['generated_text']
            answer = generated.replace(prompt, "").strip()
            if not answer:
                answer = generated
        except Exception:
            answer = "I'm sorry, I don't have information on that. Please consult a professional."
    
    # Save to history
    history.append({"question": q.question, "answer": answer})
    save_history(history)
    
    return {"answer": answer}