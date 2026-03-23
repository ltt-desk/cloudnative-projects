# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy source
COPY . .

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy installed packages and source
COPY --from=builder /root/.local /home/appuser/.local
COPY --from=builder /app .

# Set environment
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8002

CMD ["python", "main.py"]
