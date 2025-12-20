FROM python:3.12-slim

# Install system dependencies and Tesseract OCR
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        libtesseract-dev \
        libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TESSERACT_CMD=/usr/bin/tesseract
ENV PORT=${PORT:-5000}

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:${PORT}", "--timeout", "120"]
