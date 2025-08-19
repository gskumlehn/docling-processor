FROM python:3.11-slim

ARG ENABLE_OCR=true

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists \
    bash -lc 'set -eux; \
      apt-get update; \
      apt-get install -y --no-install-recommends libglib2.0-0 libgl1 ca-certificates; \
      if [ "$ENABLE_OCR" = "true" ]; then \
        apt-get install -y --no-install-recommends tesseract-ocr tesseract-ocr-por tesseract-ocr-eng; \
      fi; \
      rm -rf /var/lib/apt/lists/*'

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade --prefer-binary -r requirements.txt

COPY . /app/

EXPOSE 8080
CMD ["python", "server.py"]
