# QQ音乐签到（Surge）

QQ音乐 **绿钻成长值签到 + 金币中心签到 + App 每日任务 + 金币抽奖 + 红包雨**，一次抓包，之后全自动。
脚本主体来自 [MaYIHEI/paperclip · app/qqmusic](https://github.com/MaYIHEI/paperclip/tree/main/app/qqmusic)。

Egern 版在另一个仓库：[Konoha-Naruto/egern](https://github.com/Konoha-Naruto/egern/tree/main/modules/media/qqmusic)。

## 文件

| 文件 | 说明 |
|---|---|
| `QQMusic.sgmodule` | Surge 模块（4 条脚本 + MITM + 参数表） |
| `qqmusic.js` | 构建产物：上游源码 + `getck` 开关外壳，**不要手改** |
| `src/build.py` | 拉上游最新 `qqmusic.js`，套开关外壳，输出上一级 |

## 安装

```
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/media/qqmusic/QQMusic.sgmodule
```

Surge → 模块 → 从 URL 安装。

## 使用步骤

1. 安装模块，确认 MITM 生效（模块自带 `u6.y.qq.com`）。
2. 打开 QQ音乐 →「我的 → 会员中心」→ 进「金币中心 → 每日签到」页面一次。
3. 收到 `✅ QQ音乐 Cookie 获取成功` 通知即抓取成功。
4. 之后保持代理运行即可，Cookie 由 cron 自动续期，不用再进 App。

## 参数：抓取 Cookie（`getck`）

模块 → 编辑参数 → `getck`，默认 `true`。

| 值 | 行为 |
|---|---|
| `true`（默认 / 留空 / 其它值） | 抓 Cookie |
| `false` | 请求脚本立即 `$done({})` 放行 —— 不拦截、不读 body、不发通知 |

**cron 定时任务不受这个开关影响**，关闭抓包后签到照常执行。

> Surge 的模块参数表只支持「名称:默认值」的文本输入框（官方 `#!arguments` 没有布尔开关类型），
> 所以这里是填 `true` / `false`，不是一个开关控件。

MITM 本身是模块级的，没法随参数关闭；关掉抓包后仍会走 MITM，但脚本秒放行，开销很小。

## 定时任务

| 任务 | cron | 说明 |
|---|---|---|
| QQ音乐每日任务 | `30 7 * * *` | 续期 Cookie、两套签到、每日任务、免费抽奖；当天没跑成功，后续 cron 会补跑 |
| QQ音乐定时金币 | `* 9-10 * * *` | 9–10 点每分钟唤醒，按各任务返回的 `TargetNum / Progress / TaskMaxTimes / State` 决定是否发请求 |
| QQ音乐红包雨 | `5 0,8,12,16,20,22 * * *` | 六个时段各跑一次，每时段只请求一次 |

结果合并成最多一条通知，没新结果不打扰。

## 注意

- **不要给脚本加 `max-size=0`**。上游 README 的 Surge 片段带了这一项，但在 Surge 里 `max-size=0` 表示「响应体上限 0 字节」，请求会被直接拒绝、Cookie 永远抓不到；本模块已去掉。
- **模块参数里含逗号的值必须加引号**（如 `cronexp="5 0,8,12,16,20,22 * * *"`），否则 Surge 会把逗号当参数分隔符，`cronexp` 只剩 `5 0`。
- `* 9-10 * * *` 每分钟唤醒会增加少量耗电，这是作者为抢定时金币设计的，觉得费电可以停用该项。
- Cookie 存在客户端持久化存储里，模块本身不含任何凭证。
- 仅个人自用。接口随 App 版本变动可能失效。

## 重新生成

`qqmusic.js` 是构建产物：

```bash
cd src
python3 build.py        # 输出上一级 qqmusic.js，头部写入上游 SHA256 前 16 位
```

## 校验

```bash
# 模块语法
{ cat ../QQMusic.sgmodule; echo; echo "[Rule]"; echo "FINAL,DIRECT"; } > /tmp/qq-check.conf
surge-cli --check /tmp/qq-check.conf   # OK
```
