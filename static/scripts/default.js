function fetchHtml(url, options) {
    return fetch(url, options)
        .then(r => r.text());
}

function requestHtml(element, url, options) {
    return fetchHtml(url, options)
        .then(html => element.innerHTML = html);
}

function onRequestHtml(element, url, options) {
    return requestHtml(element, url || element.getAttribute('url'), options)
}

const config = { attributes: true, childList: true, subtree: true };

function createMutationObserver(element, callback) {
    const observer = new MutationObserver(callback);
    observer.observe(element, config);

    return observer;
}

function Debounce(defaultTimeout) {
	let sync = 0;
	this.run = (func, timeout = defaultTimeout) => {
		const stamp = ++sync;
		setTimeout(() => {
			(sync === stamp) && func(() => stamp === sync, stamp);
		}, timeout);
	};
}