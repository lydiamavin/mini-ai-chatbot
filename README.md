---
title: Mini AI Chatbot
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: latest
app_file: Dockerfile
pinned: false
---

# Mini AI Chatbot

A web-based AI chatbot that answers professional questions using a knowledge base with fuzzy string matching. Built with React frontend and FastAPI backend.

## Features
- **Frontend (React + Vite)**: Clean conversational UI with input field, send button, answer display, and chat history (last 9 interactions).
- **Backend (FastAPI)**: REST API with `/ask` endpoint for question processing.
- **Knowledge Base**: 56 professional Q&A pairs covering productivity, leadership, finance, marketing, HR, and more.
- **Matching**: Fuzzy string matching using `fuzzywuzzy` library with 50% similarity threshold.
- **History**: Persists chat history in `history.json` for context in responses.
- **Fallback**: Provides a professional fallback message for unmatched questions.

## Quick Start

### Prerequisites
- Python 3.8+ (for backend)
- Node.js 14+ (for frontend)

### Local Setup
1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend** (in a new terminal):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Open `http://localhost:5173` in your browser to access the chatbot UI.

## API Usage
- **Endpoint**: `POST /ask`
- **Request Body**: `{"question": "Your question here"}`
- **Response**: `{"answer": "Answer text"}`

### Example API Call
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How to manage time effectively?"}'
```
Response: `{"answer": "Set SMART goals, use calendars, and avoid multitasking."}`

## Libraries Used
- **Backend**: FastAPI, Uvicorn, Pydantic, fuzzywuzzy
- **Frontend**: React, Axios, Vite

## Project Structure
```
mini-ai-chatbot/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── knowledge_base.json    # 56 Q&A pairs
│   ├── history.json           # Chat history
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── App.css            # Styles
│   │   └── main.jsx           # App entry point
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
├── .gitignore
└── README.md
```

## Assumptions
- Knowledge base covers common professional topics; unmatched questions receive a fallback response.
- Chat history uses the last 3 interactions for context.
- Fuzzy matching threshold of 50% balances accuracy and coverage.
