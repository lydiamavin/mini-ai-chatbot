---
title: Mini AI Chatbot
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: python
sdk_version: "0.0.1"
app_file: app.py
pinned: false
---

# Mini AI Chatbot

A web-based AI chatbot answering professional questions using a knowledge base, with fuzzy matching and LLM fallback.

## Features
- **Frontend (React + Vite)**: Conversational chat UI with history and clear option.
- **Backend (FastAPI)**: REST API with `/ask` endpoint.
- **Knowledge Base**: 20 professional Q&A pairs in JSON.
- **Matching**: Fuzzy string matching using `fuzzywuzzy` (70% threshold).
- **History**: Persists chat history in `history.json`.
- **Fallback**: Open-source LLM (DistilGPT-2) for unmatched questions.
- **Deployment**: Docker support for easy containerization.

## Quick Start

### Prerequisites
- Docker (for containerized run) or Python 3.8+ & Node.js 14+

### Option 1: Docker (Recommended)
```bash
cd backend
docker build -t mini-ai-backend .
docker run -d -p 8000:8000 --name mini-ai-backend mini-ai-backend
cd ../frontend
npm install
npm run dev
```
Frontend: `http://localhost:5173`, Backend: `http://localhost:8000`.

### Option 2: Local Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## API Usage
- **Endpoint**: `POST /ask`
- **Request**: `{"question": "Your question"}`
- **Response**: `{"answer": "Answer text"}`

Example:
```bash
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"question": "How to manage time effectively?"}'
```

## Libraries Used
- **Backend**: FastAPI, Uvicorn, Pydantic, fuzzywuzzy, transformers, torch
- **Frontend**: React, Axios, Vite

## Project Structure
```
mini-ai-chatbot/
├── backend/
│   ├── app.py                
│   ├── knowledge_base.json   
│   ├── history.json           
│   ├── requirements.txt   
│   └── Dockerfile             # Container config
├── frontend/
│   ├── src/
│   │   ├── App.jsx          
│   │   ├── App.css           
│   │   └── main.jsx           # App entry
│   ├── package.json          
│   └── vite.config.js         
├── .gitignore                 
└── README.md
```
