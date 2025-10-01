# =========================
# 1. Backend (FastAPI)
# =========================
FROM python:3.10-slim AS backend

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app

# =========================
# 2. Frontend (React)
# =========================
FROM node:18 AS frontend

WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend .
RUN npm run build

# =========================
# 3. Final Image
# =========================
FROM python:3.10-slim

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend /app

# Copy frontend build into /app/static
COPY --from=frontend /frontend/dist /app/static

# Expose port
EXPOSE 7860

# Start FastAPI backend (serving frontend as static files)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
