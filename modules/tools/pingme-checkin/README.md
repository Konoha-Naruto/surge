# PingMe自动签到（Surge 模块）

PingMe App 每日签到 + 视频奖励签到。签到脚本每次运行会随机一个设备 ID，并自动给请求签名。

- 原作者：@ZenMoFiShi / 怎么肥事 / 奶思
- Egern 版：mickeu
- 本仓库：Surge 移植版（Egern v2 `ctx.*` API → Surge 原生 `$httpClient` / `$persistentStore` / `$notification`）

## 安装

```
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/tools/pingme-checkin/PingMe.sgmodule
```

## 使用

1. 装好模块，确认 Surge 的 **MITM** 已开、证书已信任（模块会自动把 `api.pingmeapp.net` 追加进 hostname）。
2. 模块参数 `PINGME_CAPTURE` 保持默认 `true`，打开 PingMe App 随便刷新一下（触发 `queryBalanceAndBonus` 请求），会收到「✅ PingMe 获取成功」通知，签到参数已写入本地存储。
3. 抓完后把 `PINGME_CAPTURE` 设为 `false` 省电，之后每天按 `CRON` 自动签到。

## 模块参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `PROXY` | `DIRECT` | `api.pingmeapp.net` 走哪条策略。Surge 对模块内规则策略有限制，报错就保持 `DIRECT` |
| `CRON` | `30 8 * * *` | 签到定时表达式。想恢复原作者的一天两次填 `30 8,20 * * *` |
| `PINGME_CAPTURE` | `true` | 抓参开关，抓完设为 `false` |

## 文件

| 文件 | 作用 |
|---|---|
| `PingMe.sgmodule` | 模块本体（规则 / MITM / 两条脚本） |
| `checkin.js` | 定时签到：签到 + 视频奖励（最多 5 次，间隔 10s） |
| `capture.js` | 抓参：拦截余额/奖励查询请求，保存 URL 与请求头到 `pingme_capture_v3` |

## 备注

- 抓到的参数存在 Surge 本地持久化存储（key `pingme_capture_v3`），不含模块内代码里的签名密钥以外的额外凭证。
- 通知图标取自 [axhani/icon](https://github.com/axhani/icon)。
- 原始版本脚本托管在 paste.rs（链接会过期），本仓库改为自托管，模块内 `script-path` 已指向本仓库 raw 地址。
