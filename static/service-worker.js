const CACHE_NAME = "igem-iv-calculator-v3";

const OFFLINE_ASSETS = [

"/home",

"/calculator",

"/static/main.css",

"/static/calculator.css",

"/static/manifest.json",

"/static/icon-180.png",

"/static/icon-192.png",

"/static/icon-512.png"

];

self.addEventListener(
"install",
event => {

    event.waitUntil(

        caches
            .open(CACHE_NAME)
            .then(cache => {

                return cache.addAll(
                    OFFLINE_ASSETS
                );

            })

    );

    self.skipWaiting();

}

);

self.addEventListener(
"activate",
event => {

    event.waitUntil(

        caches
            .keys()
            .then(keys => {

                return Promise.all(

                    keys
                        .filter(
                            key =>
                                key !== CACHE_NAME
                        )
                        .map(
                            key =>
                                caches.delete(key)
                        )

                );

            })

    );

    self.clients.claim();

}

);

self.addEventListener(
"fetch",
event => {

    if (
        event.request.method !== "GET"
    ) {

        return;

    }


    const url =
        new URL(event.request.url);


    /*
     * Only handle requests to this app.
     */

    if (
        url.origin !==
        self.location.origin
    ) {

        return;

    }


    /*
     * Never intercept the login page.
     */

    if (
        url.pathname === "/login"
    ) {

        return;

    }


    /*
     * Static files:
     *
     * Cache first, then network.
     */

    if (
        url.pathname.startsWith(
            "/static/"
        )
    ) {

        event.respondWith(

            caches
                .match(event.request)
                .then(cached => {

                    if (cached) {

                        return cached;

                    }

                    return fetch(
                        event.request
                    )
                    .then(response => {

                        if (
                            response.ok
                        ) {

                            const copy =
                                response.clone();

                            caches
                                .open(
                                    CACHE_NAME
                                )
                                .then(
                                    cache => {
                                        cache.put(
                                            event.request,
                                            copy
                                        );
                                    }
                                );

                        }

                        return response;

                    });

                })

        );

        return;

    }


    /*
     * App pages:
     *
     * Network first when online.
     * Cached version when offline.
     */

    if (
        url.pathname === "/" ||
        url.pathname === "/home" ||
        url.pathname === "/calculator" ||
        url.pathname === "/Calculator"
    ) {

        event.respondWith(

            fetch(event.request)

                .then(response => {

                    if (
                        response.ok
                    ) {

                        const copy =
                            response.clone();

                        caches
                            .open(
                                CACHE_NAME
                            )
                            .then(
                                cache => {

                                    cache.put(
                                        event.request,
                                        copy
                                    );

                                }
                            );

                    }

                    return response;

                })

                .catch(() => {

                    return caches.match(
                        event.request
                    );

                })

        );

    }

}

);
