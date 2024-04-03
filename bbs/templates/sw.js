const CACHE_NAME = 'caches-pwa';
const urlsToCache = [
	'/media/bg_parallax.webp',
	'/media/1.webp',
	'/media/2.webp',
	'/media/logo.svg',
	'/media/author.webp',
	'/static/css/index.css',
	'/static/fonts/icomoon.ttf',
	'/static/fonts/MontserratSubrayada-Bold.ttf',
	'/static/js/main.js'
];
self.addEventListener('install', (event) => {
	event.waitUntil(
		caches
		.open(CACHE_NAME)
		.then((cache) => {
			return cache.addAll(urlsToCache);
		})
	);
});
self.addEventListener('fetch', (event) => {
	event.respondWith(
		caches
		.match(event.request)
		.then((response) => {
			return response ? response : fetch(event.request);
		})
	);
});