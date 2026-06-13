FROM python:3.11-slim

WORKDIR /app

LABEL org.opencontainers.image.title="CodeSage AI" \
      org.opencontainers.image.description="CodeSage AI – Autonomous Code Intelligence Agent" \
      org.opencontainers.image.source="https://github.com/your-org/codesage-ai"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY codesage_ai ./codesage_ai
RUN pip install --no-cache-dir .

EXPOSE 8000
CMD ["uvicorn", "codesage_ai.main:app", "--host", "0.0.0.0", "--port", "8000"]
