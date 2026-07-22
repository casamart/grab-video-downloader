# Grab — Mobile Video Downloader (PWA)

A phone-friendly web app for downloading videos **you have the right to save**.
You run a tiny server (on your PC or a host), open it on your phone's browser,
and **Add to Home Screen** — it then opens fullscreen like a native app.

Why a web app and not a store app?
- **iOS App Store** and **Google Play** both **ban** video-downloader apps.
- A PWA installs straight from the browser, works on **Android + iPhone**, and
  needs no Android Studio, no signing, no Apple developer account.

---

## How it works
Your phone sends the link → the server downloads it with `yt-dlp` → the file is
streamed back to your phone and saved to **Downloads**.

| Platform | Link support |
|---|---|
| YouTube, TikTok, Instagram, X | ✅ paste the link |
| Snapchat | ⚠️ public **Spotlight** links only |
| WhatsApp status | ❌ no link — copy from your phone's `.Statuses` folder* |

\* `Internal storage/Android/media/com.whatsapp/WhatsApp/Media/.Statuses`
(enable "show hidden files"). View the status first so it caches, then copy it.

---

## Setup (once, on your PC)

```bash
pip install -r requirements.txt
winget install Gyan.FFmpeg
```
(ffmpeg is needed for "Best" quality merging and MP3.)

## Run it

```bash
python app.py
```
You'll see it serving on port **5000**.

## Open it on your phone
1. Make sure your **phone and PC are on the same Wi-Fi**.
2. Find your PC's IP: run `ipconfig` and read the **IPv4 Address** (e.g. `192.168.1.24`).
3. On your phone's browser go to:  `http://YOUR_PC_IP:5000`  (e.g. `http://192.168.1.24:5000`)
4. Browser menu → **Add to Home Screen**. Now it's an app icon.

---

## Use it anywhere (optional hosting)
To use it off your home Wi-Fi, deploy `app.py` to a host (Render, Railway, a
VPS, etc.). Note: cloud IPs are sometimes rate-limited or blocked by the video
platforms, so a home/PC run is usually the most reliable.

---

## Please use it responsibly
For content you **own, licensed, or have permission** to save — your own posts,
royalty-free/CC0 clips, or videos a creator allows you to reuse. Downloading and
re-posting other people's videos can infringe copyright and break platform
Terms of Service.
