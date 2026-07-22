# Grab — video downloader web app.
# Container image that works on any Docker host (Koyeb, Render, Fly, Railway…).
FROM python:3.12-slim

# ffmpeg is needed for "Best" quality merging and MP3 extraction.
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Hosts inject $PORT; default to 8080 for local `docker run`.
ENV PORT=8080
EXPOSE 8080

# 1 worker (jobs live in memory), multiple threads, generous timeout for downloads.
CMD ["sh", "-c", "gunicorn -w 1 --threads 8 -t 300 -b 0.0.0.0:${PORT} app:app"]
