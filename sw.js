/**
 * English Learning Website - Service Worker
 * 
 * Strategy: Stale-While-Revalidate + Auto-Refresh on Update
 *   - Instantly serves cached content (fast offline-first).
 *   - In background, fetches latest version from network and updates cache.
 *   - When new content is successfully fetched, notifies all pages to refresh.
 *   - On next page load, the fresh content is served from cache.
 * 
 * Update flow:
 *   1. User visits page → sees cached (possibly stale) content instantly
 *   2. SW fetches new files in background → stores in cache
 *   3. SW sends "NEW_CONTENT" message to all pages
 *   4. Page receives message → shows a prompt or auto-refreshes
 *   5. After refresh → new content served from cache (the update propagated)
 */

const CACHE_NAME = 'english-learning-v3';

// All static assets to precache. Updated 2026-06-21.
const PRECACHE_URLS = [
  '/', '/index.html', '/core-vocabulary.html',
  '/verbs-a-l.html', '/verbs-m-z.html',
  '/adjectives-adverbs.html', '/nouns-life-scene.html',
  '/nouns-society-function.html',
  '/css/common.css', '/css/grammar.css',
  '/js/common.js',
  '/grammar/tenses.html', '/grammar/passive-voice.html',
  '/grammar/clauses.html', '/grammar/non-finite-verbs.html',
  '/grammar/modal-verbs.html', '/grammar/sentence-patterns.html',
  '/grammar/prepositions.html', '/grammar/confusable-words.html',
  '/grammar/subject-verb-agreement.html',
  '/grammar/direct-indirect-speech.html',
  '/grammar/verb-collocations.html', '/grammar/writing-connectors.html'
];

// ======================== Install ========================

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.addAll(PRECACHE_URLS);
    }).then(function () {
      return self.skipWaiting();
    })
  );
});

// ======================== Activate ========================

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (cacheNames) {
      return Promise.all(
        cacheNames.map(function (name) {
          if (name !== CACHE_NAME) {
            return caches.delete(name);
          }
        })
      );
    }).then(function () {
      return self.clients.claim();
    })
  );
});

// ======================== Fetch (Stale-While-Revalidate + Notify) ========================

self.addEventListener('fetch', function (event) {
  if (event.request.method !== 'GET') return;
  if (!event.request.url.startsWith('http')) return;
  
  // Directly bypass Google TTS so it doesn't pass through the Service Worker
  if (event.request.url.includes('translate.google.com')) return;

  event.respondWith(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.match(event.request).then(function (cachedResponse) {
        
        // Define the network fetch operation
        var networkFetch = fetch(event.request).then(function (networkResponse) {
          // If the network response is valid, manage cache insertion and updates
          if (networkResponse && networkResponse.status === 200) {
            if (networkResponse.type === 'basic') {
              
              var oldCachedPromise = cache.match(event.request);
              var responseToCache = networkResponse.clone();
              cache.put(event.request, responseToCache);

              oldCachedPromise.then(function (oldCached) {
                if (oldCached) {
                  // Compare old and new content to notify clients of updates
                  Promise.all([
                    oldCached.clone().text(),
                    networkResponse.clone().text()
                  ]).then(function (texts) {
                    if (texts[0] !== texts[1]) {
                      self.clients.matchAll().then(function (clients) {
                        clients.forEach(function (client) {
                          client.postMessage({
                            type: 'CONTENT_UPDATED',
                            url: event.request.url
                          });
                        });
                      });
                    }
                  }).catch(function (err) {
                    console.warn('Content comparison skipped:', err);
                  });
                }
              });
            }
          }
          // ALWAYS return the actual network response to the browser
          return networkResponse;
        }).catch(function (err) {
          // If network fails and we have no cached copy, throw error naturally
          if (!cachedResponse) {
            throw err;
          }
        });

        // Return the cached response instantly if available; otherwise, serve from the network
        return cachedResponse || networkFetch;
      });
    })
  );
});

// ======================== Message: skipWaiting from page ========================

self.addEventListener('message', function (event) {
  if (event.data && event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
});