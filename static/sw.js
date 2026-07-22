// Minimal service worker — makes the app installable ("Add to Home Screen").
// Network-first passthrough; we intentionally don't cache download responses.
const CACHE = "grab-v1";
const SHELL = ["/", "/static/manifest.webmanifest", "/static/icon.svg"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).catch(() => {}));
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  // Never intercept downloads or non-GET requests.
  if (req.method !== "GET" || new URL(req.url).pathname.startsWith("/api/")) return;
  e.respondWith(fetch(req).catch(() => caches.match(req)));
});
