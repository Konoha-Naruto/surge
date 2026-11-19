# Google 去广告（规则版）

原地址 `https://loon.103516.xyz/Plugin/Google.lpx` **已下线**：整个站点的 `/Plugin`、`/Script` 路径现在都 302 到 `https://t.me/BoStudioHub`，下载回来的是 Telegram 频道页 HTML（11000 B），不是插件。

本模块取自同源镜像 [`fmz200/wool_scripts`](https://raw.githubusercontent.com/fmz200/wool_scripts/main/Loon/plugin/split/partG/Google.lpx)（2026-11-11 21:17 版，作者 奶思），转成 Surge 语法。

安装：

```
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/ads/google/Google.sgmodule
```

## 内容

- 50 条纯域名规则，`REJECT`：Google 广告/统计体系（doubleclick、googlesyndication、googleadservices、admob、firebase `app-measurement`、`crashlytics`、`google-analytics`、`googletagmanager|services`、2mdn），外加原插件附带的腾讯系 CDN 统计域名（`gtimg.com`、`qlogo.cn`）。
- 无脚本、无 MITM，最轻量。

## 与原插件的差异

1. 原 `.lpx` 的 52 条规则里有 2 条无效：`pagead2.googlesyndication.com`（Loon 变量，不是域名）和 `pagespeed-mod`（无点号的非法域名），已剔除，剩 50 条。
2. 原插件 4 条 `reject_img(200)` 改写指向 `*.googleapis.com` 的 `ad_break` / `log_event` / `adsmeasurement` 与 `pagead2.googlesyndication.com/pagead/`，但它的 `[MITM] hostname` 只写了 `pagead2.googlesyndication.com`，没有实际域名 → 在 Loon 里这四条等于从未生效。Surge 版不带 MITM，保持同样效果；要启用见模块内注释。
3. Loon 的 `reject_img(200)` 在 Surge 没有同名词，需要用 Map Local 回 200 空体（`data-type=text data="" status-code=200`）。

## 提醒

- `crashlytics.com` / `app-measurement.com` 被拦后，App 崩溃上报与埋点会一起失效，这是原插件的设计。
- `safebrowsing.googleapis.com` 被拦，Safari/Chrome 的钓鱼站点提示会少一层，介意就把这行删掉。
- 拦截生效需要清 App 缓存或重装，尤其 Chrome / YouTube 这类缓存狠的。

## 校验

- `surge-cli --check`（拼最小 profile + `FINAL,DIRECT`）：`OK`
- 规则数：50（原 52，剔除 2 条非法）
