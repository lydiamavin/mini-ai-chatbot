FROM python:3.11-slim

# Install Node.js for building frontend
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy backend and frontend
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Install Python dependencies
WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt

# Build frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# Move built frontend to backend/static
RUN mv dist ../backend/static

# Back to backend
WORKDIR /app/backend

# Expose port
EXPOSE 7860

# Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]