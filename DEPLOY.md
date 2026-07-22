# Deploying Grab to a free host

You asked me to host it on a free host you haven't used. I've made it fully
deploy-ready (a `Dockerfile` + `Procfile`), but the final sign-in and deploy
clicks are yours — I can't create accounts, accept a host's terms, or enter a
card on your behalf.

**Recommended host: [Koyeb](https://www.koyeb.com)** — free tier, runs Docker,
**no credit card required**, and it's not one of the hosts noted against your
account (you've used Vercel; Vercel's serverless model can't run ffmpeg + long
downloads anyway, so it's the wrong tool here).

---

## Option A — Koyeb (recommended, no card)

1. Push this `mobile/` folder to a **GitHub repo** (public or private).
2. Go to **koyeb.com** → sign up (GitHub login is easiest).
3. **Create Web Service** → **GitHub** → pick your repo.
4. Koyeb auto-detects the `Dockerfile`. Leave the build as **Docker**.
5. Set the **port to `8080`** (matches the Dockerfile).
6. Pick the **Free** instance → **Deploy**.
7. In ~2–3 min you get a public URL like `https://grab-xxxx.koyeb.app`.
8. Open it on your phone → **Add to Home Screen**.

## Option B — Render (also free; skip if you've used it)

1. Push `mobile/` to GitHub.
2. **render.com** → **New → Web Service** → connect the repo.
3. Runtime **Docker**. Free instance. **Create Web Service**.
4. Use the `onrender.com` URL it gives you.

## Option C — Fly.io (free allowance, but asks for a card)

`flyctl launch` from this folder detects the Dockerfile. Only if you're okay
adding a card for verification.

---

## Test the image locally first (optional)
If you have Docker Desktop:
```bash
docker build -t grab .
docker run -p 8080:8080 grab
# open http://localhost:8080
```

---

## Honest caveats for a *hosted* downloader
- **Platform blocks:** YouTube/IG/TikTok often rate-limit or block known cloud
  IPs. A hosted instance may hit "sign in to confirm" or throttling that a
  home/PC run doesn't. If a site blocks it, running on your own PC is the
  reliable fallback.
- **Free tiers sleep:** the app may cold-start (a few seconds) after inactivity.
- **Keep it yours:** it's a public URL anyone with the link could use. Don't
  share it around; if you want, I can add a simple password gate.
- Same rights rule as always: only download content you own or may use.
