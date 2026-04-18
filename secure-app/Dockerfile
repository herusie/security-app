# syntax=docker/dockerfile:1

FROM python:3.12.4-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies without cache to keep image small.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create and use an unprivileged user.
RUN useradd --create-home --shell /usr/sbin/nologin appuser

COPY app ./app

USER appuser
EXPOSE 8080

CMD ["python", "app/main.py"]
