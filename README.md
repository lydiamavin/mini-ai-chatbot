# Mini AI Chatbot

A simple web-based AI chatbot that answers professional questions using a small knowledge base.

## Features
- **Frontend (React)**: Clean UI with input box, submit button, answer display, and chat history (last 10 Q&As).
- **Backend (FastAPI)**: REST API with `/ask` endpoint accepting JSON `{"question": "..."}` and returning `{"answer": "..."}`.
- **Knowledge Base**: 10 professional Q&A pairs stored in JSON.
- **Matching**: Fuzzy string matching using Python's `difflib`.
- **History**: Saves Q&A history to `history.json`.
- **Fallback**: Returns a default message for unmatched questions (placeholder for LLM API).

## Quick Start

### Prerequisites
- Python 3.8+ (with pip)
- Node.js 14+ (with npm)

### 1. Clone or Download the Project
Ensure you're in the project root directory.

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
Backend will run on `http://localhost:8000`.

### 3. Frontend Setup (in a new terminal)
```bash
cd frontend
npm install
npm run dev  # or npm start if using react-scripts
```
Frontend will run on `http://localhost:5173` (Vite) or `http://localhost:3000` (react-scripts).

### 4. Test the Chatbot
- Open the frontend URL in your browser.
- Ask questions like "How can I improve my productivity?" or "What is work-life balance?"
- Check chat history and backend logs for saved history.

## API Usage
- **Endpoint**: `POST /ask`
- **Request**: `{"question": "Your question here"}`
- **Response**: `{"answer": "Matched or fallback answer"}`

Example with curl:
```bash
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"question": "How to manage time effectively?"}'
```

## Libraries Used
- **Backend**: FastAPI (API framework), Uvicorn (server), Pydantic (data validation)
- **Frontend**: React (UI), Axios (HTTP client), Vite or react-scripts (build tool)

## Assumptions & Notes
- Knowledge base is static; edit `backend/knowledge_base.json` to add more Q&As.
- History persists in `backend/history.json` (appends on each ask).
- No authentication or rate limiting.
- CORS enabled for local dev.
- Fallback is mock; integrate OpenAI API by adding `openai` to requirements and updating `app.py`.
- Tested on macOS; adjust paths if needed.

## Project Structure
```
mini-ai-chatbot/
├── backend/
│   ├── app.py                 # FastAPI app
│   ├── knowledge_base.json    # Q&A data
│   ├── history.json           # Chat history
│   └── requirements.txt       # Python deps
├── frontend/
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── App.css            # Styles
│   │   └── index.js           # App entry
│   ├── public/index.html      # HTML template
│   └── package.json           # Node deps
├── .gitignore                 # Ignore venv, node_modules, etc.
└── README.md                  # This file
```

## Troubleshooting
- **Backend errors**: Ensure Python venv is activated and deps installed.
- **Frontend errors**: Clear npm cache (`npm cache clean --force`) and reinstall.
- **Connection issues**: Check ports (8000 for backend, 5173/3000 for frontend) and firewall.
- **No matches**: Questions must closely match knowledge base keys (case-insensitive fuzzy match).

For issues, check console logs or open an issue on GitHub.