# 墨墨签到抓包（Surge）

只记录墨墨背单词 App 的请求，**不改包、不阻断**，用来提取每日签到的真实接口与参数。

| 文件 | 说明 |
|---|---|
| `maimemo-capture.sgmodule` | 模块：一条 `http-request` 记录脚本 + MITM |
| `capture.js` | 记录脚本，输出到 Surge 日志 |

## 安装

```
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/tools/maimemo-capture/maimemo-capture.sgmodule
```

## 用法

1. 装模块，确认 MITM 生效（模块追加 `*.maimemo.com`）。
2. 打开一次墨墨 →「我的 → 签到」。
3. 到 Surge → 日志 里看请求体与参数，即签到接口。
4. 抓完**关闭本模块** —— 它不带任何定时任务，长期挂着只会多记日志。

## 说明

- 只做 `http-request` 记录，`requires-body=true` 读取请求体；从不改写响应。
- `capture.js` 里没有凭证，日志只写到本地 Surge 日志。
