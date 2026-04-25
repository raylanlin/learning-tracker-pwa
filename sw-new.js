const CACHE_NAME = 'learning-tracker-v10';
const ASSETS = ['/', '/index.html', '/manifest.json'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  // API calls: network first, then offline fallback.
  // Return a 503 (not 200) so the app's res.ok check correctly routes into
  // its offline branch and flags "同步失败" instead of "已同步".
  if (e.request.url.includes('supabase')) {
    e.respondWith(
      fetch(e.request).catch(() => {
        return new Response(JSON.stringify({ error: 'offline' }), {
          status: 503,
          statusText: 'Service Unavailable',
          headers: { 'Content-Type': 'application/json' }
        });
      })
    );
    return;
  }
  // Static assets: cache first
  e.respondWith(
    caches.match(e.request).then(resp => resp || fetch(e.request).then(r => {
      const clone = r.clone();
      caches.open(CACHE_NAME).then(c => c.put(e.request, clone)).catch(() => {});
      return r;
    }).catch(() => caches.match('/index.html')))
  );
});
