# ==========================
# Stage 1 - Build React App
# ==========================
FROM node:20-alpine AS frontend-builder

WORKDIR /frontend

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ .

RUN npm run build


# ==========================
# Stage 2 - Flask Backend
# ==========================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download EasyOCR models during Docker build
RUN mkdir -p /app/easyocr_models && \
    python -c "import easyocr; easyocr.Reader(['en'], gpu=False, model_storage_directory='/app/easyocr_models', verbose=True)"

# Copy backend code
COPY backend/ .

# Copy React production build
COPY --from=frontend-builder /frontend/dist ./frontend_build

# Railway provides PORT automatically
ENV PORT=8080

EXPOSE 8080

CMD ["python", "app.py"]