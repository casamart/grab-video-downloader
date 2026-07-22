#!/usr/bin/env python3
"""
Link Video Downloader — mobile web app (PWA)
============================================
A phone-friendly web front-end over yt-dlp. Run on your PC or a host, open it in
your phone's browser, and "Add to Home Screen" to use it like an app.

Job model: the browser starts a download job, polls progress, then fetches the
finished file. This gives a real progress bar and avoids long-request timeouts
on cloud hosts.

Use only for content you own or have permission to save. Respect platform ToS
and copyright.
"""

import glob
import os
import shutil
import tempfile
import threading
import time
import uuid

from flask import Flask, jsonify, render_template, request, send_file

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

app = Flask(__name__)

# quality key -> yt-dlp format ("audio" handled specially)
FORMATS = {
    "best": "bestvideo*+bestaudio/best",
    "1080": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "audio": "audio",
}

JOBS = {}          # job_id -> dict(status, percent, title, error, path, tmp, ts)
JOB_TTL = 1800     # seconds to keep a finished/failed job before sweeping


def _sweep():
    now = time.time()
    for jid, job in list(JOBS.items()):
        if now - job["ts"] > JOB_TTL:
            shutil.rmtree(job.get("tmp", ""), ignore_errors=True)
            JOBS.pop(jid, None)


def _run_job(job_id, url, quality):
    job = JOBS[job_id]
    tmp = job["tmp"]
    fmt = FORMATS.get(quality, FORMATS["best"])

    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            got = d.get("downloaded_bytes") or 0
            job["percent"] = int(got * 100 / total) if total else job["percent"]
            job["status"] = "downloading"
        elif d["status"] == "finished":
            job["percent"] = 100
            job["status"] = "processing"

    opts = {
        "outtmpl": os.path.join(tmp, "%(title).80s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
        "progress_hooks": [hook],
    }
    if fmt == "audio":
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        opts["format"] = fmt

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            job["title"] = (info or {}).get("title") or "video"
        files = sorted(glob.glob(os.path.join(tmp, "*")), key=os.path.getsize, reverse=True)
        if not files:
            raise RuntimeError("Nothing downloaded — unsupported, private, or invalid link.")
        job["path"] = files[0]
        job["percent"] = 100
        job["status"] = "done"
    except Exception as e:  # noqa: BLE001 - surface any yt-dlp error to the client
        job["status"] = "error"
        job["error"] = str(e)
        shutil.rmtree(tmp, ignore_errors=True)


@app.get("/")
def index():
    return render_template("index.html", ready=yt_dlp is not None)


@app.post("/api/start")
def start():
    if yt_dlp is None:
        return jsonify(error="yt-dlp is not installed on the server."), 500
    _sweep()
    url = (request.form.get("url") or "").strip()
    quality = request.form.get("quality", "best")
    if not url:
        return jsonify(error="Please paste a link first."), 400
    job_id = uuid.uuid4().hex[:12]
    JOBS[job_id] = {
        "status": "queued", "percent": 0, "title": "", "error": "",
        "path": None, "tmp": tempfile.mkdtemp(prefix="vdl_"), "ts": time.time(),
    }
    threading.Thread(target=_run_job, args=(job_id, url, quality), daemon=True).start()
    return jsonify(job_id=job_id)


@app.get("/api/progress/<job_id>")
def progress(job_id):
    job = JOBS.get(job_id)
    if not job:
        return jsonify(error="Unknown job."), 404
    return jsonify(status=job["status"], percent=job["percent"],
                   title=job["title"], error=job["error"])


@app.get("/api/file/<job_id>")
def file(job_id):
    job = JOBS.get(job_id)
    if not job or job["status"] != "done" or not job["path"]:
        return jsonify(error="File not ready."), 400
    tmp = job["tmp"]
    resp = send_file(job["path"], as_attachment=True,
                     download_name=os.path.basename(job["path"]))

    @resp.call_on_close
    def _cleanup():
        shutil.rmtree(tmp, ignore_errors=True)
        JOBS.pop(job_id, None)

    return resp


if __name__ == "__main__":
    # dev server; production uses gunicorn (see Procfile / Dockerfile)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
