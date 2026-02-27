FROM python:3.11-slim

WORKDIR /app

# Copy the whole repo first so `app/` exists
COPY . /app

# Install dependencies (from pyproject.toml) + project
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]