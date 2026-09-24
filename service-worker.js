const CACHE_NAME = "igem-iv-calculator-v1";

const APP_FILES = [
    "/",
    "/home",
    "/Calculator",
    "/calculator",

    "/static/main.css",
    "/static/calculator.css",
    "/static/manifest.json",

    "/static/icon-180.png",
    "/static/icon-192.png",
    "/static/icon-512.png"
];


self.addEventListener("install", event => {

    event.waitUntil(

        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(APP_FILES))

    );

    self.skipWaiting();

});


self.addEventListener("activate", event => {

    event.waitUntil(

        caches.keys().then(keys => {

            return Promise.all(

                keys
                    .filter(key => key !== CACHE_NAME)
                    .map(key => caches.delete(key))

            );

        })

    );

    self.clients.claim();

});


self.addEventListener("fetch", event => {

    /*
     * Only handle GET requests.
     */

    if (event.request.method !== "GET") {
        return;
    }


    event.respondWith(

        caches.match(event.request)
            .then(cachedResponse => {

                if (cachedResponse) {
                    return cachedResponse;
                }

                return fetch(event.request);

            })

    );

});