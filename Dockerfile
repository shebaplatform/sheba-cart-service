# -------- Stage 1: Build dependencies --------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential libffi-dev

# Install poetry or use pip + requirements.txt
COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# -------- Stage 2: Final minimal image --------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install only runtime dependencies
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Copy only essential code (assuming mounted or included at build)
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start using uvicorn without reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
