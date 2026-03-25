// 每次你更改 sw.js 、index.html 、 manifest.json时，就把这个版本号改一下（比如 v1 改成 v2）

const CACHE_NAME = 'energy-station-v4'; // 以后改 UI 样式需要改这个版本号
const ASSETS_TO_CACHE = [
    './',
    './index.html',
    './manifest.json'
];

// 1. 安装阶段：把网页外壳存入仓库
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('正在缓存外壳资源...');
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting(); // 强制跳过等待，立即接管
});

// 2. 激活阶段：清理旧版本的仓库
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.map(key => {
                    if (key !== CACHE_NAME) {
                        console.log('清理旧缓存:', key);
                        return caches.delete(key);
                    }
                })
            );
        })
    );
    self.clients.claim(); // 立即控制所有页面
});

// 3. 拦截请求：核心逻辑
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);

    // 如果是请求 data.json，我们采取“网络优先，失败则找缓存”的策略
    if (url.pathname.includes('data.json')) {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    // 联网成功，顺便更新一下本地缓存的数据
                    const clnd = response.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(event.request, clnd));
                    return response;
                })
                .catch(() => {
                    // 没网了，从缓存里翻出上一次存的数据
                    return caches.match(event.request);
                })
        );
    } else {
        // 其他资源（HTML/CSS/JS），直接走缓存加速打开
        event.respondWith(
            caches.match(event.request).then(response => {
                return response || fetch(event.request);
            })
        );
    }
});
