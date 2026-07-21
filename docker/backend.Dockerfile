FROM python:3.12-slim

WORKDIR /app

# Keep STT_PROVIDER/TTS_PROVIDER at their mock defaults unless the real
# NVIDIA parakeet/chatterbox weights are available on the host running this
# image -- swapping providers is an env var change, not a rebuild.

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY backend/alembic ./alembic
COPY backend/alembic.ini .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
