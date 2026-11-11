# Apple：下载 / 基础服务 分开

把 Apple 流量拆成两份，便于「下载走一条线路、其余走另一条」：

| 文件 | 管什么 | 条数 |
|---|---|---|
| `AppleDownload.list` | App Store 商店与 App 本体下载、iOS/macOS 系统更新、固件与更新 CDN | 88 |
| `AppleServices.list` | APNs、账号/激活、iCloud、地图/推送等其余 Apple 服务 | 99 |

## ⚠️ 顺序要求

`AppleServices.list` 里带了兜底规则 `DOMAIN-SUFFIX,apple.com`（收「其余所有 Apple 流量」），
所以 **`AppleDownload` 必须排在前面**：

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Konoha-Naruto/surge/main/rules/apple/AppleDownload.list,下载
RULE-SET,https://raw.githubusercontent.com/Konoha-Naruto/surge/main/rules/apple/AppleServices.list,Apple服务
```

顺序反了，App Store 和系统更新会被 Services 的兜底吃掉。

## 覆盖范围

**AppleDownload（88 条）**

| 类别 | 代表域名 |
|---|---|
| 商店页 / App 接口 | `apps.apple.com`、`itunes.apple.com`、`iosapps.apple.com` |
| App 本体下载 | `iosapps.itunes.apple.com` |
| 商店图片 / 预览 CDN | `mzstatic.com` |
| 短链 | `appsto.re`、`appstore.com` |
| OTA / 系统更新 | `mesu.apple.com`、`updates.cdn-apple.com`、`updates-http.cdn-apple.com`、`swcdn.apple.com`、`swdist.apple.com`、`oscdn.apple.com`、`gdmf*.apple.com` |
| 固件分发 | `appldnld.apple.com`、`appldnld-cdn.apple.com.akadns.net` |

**AppleServices（99 条）**

| 类别 | 代表域名 / 规则 |
|---|---|
| APNs 推送 | `identity.apple.com`、`push.apple.com`、`push-apple.com.akadns.net`、APNs 的 IP 段 |
| 账号 / 激活 | `appleid.apple.com`、`gsa.apple.com`、`idmsa.apple.com`、`gs.apple.com` |
| iCloud | `icloud.com`、`icloud-content.com`、`apple-cloudkit.com`、`cdn-apple.com`（含各国 `icloud.*`） |
| 兜底 | `DOMAIN-SUFFIX,apple.com`、`aaplimg.com`、`apple-dns.net` |
| 关键词 | `apple.com.akadns.net`、`apple.com.edgekey.net`、`apple-support.akadns.net`、`buy.itunes.apple.com`、`testflight`、`smp-device` |

`USER-AGENT` / `PROCESS-NAME` 类规则（设备相关，跨设备容易误伤）已剔除，上游只保留域名与 IP 段。

## 典型用法

```ini
# 下载走大带宽节点
RULE-SET,...,AppleDownload.list,🇸🇬 高速
# 其余 Apple 直连，省代理流量
RULE-SET,...,AppleServices.list,DIRECT
```

## 重新生成

```bash
python3 build.py
```

上游取 `blackmatrix7/ios_rule_script`（AppStore / SystemOTA / AppleID / iCloud / Apple）与
`HotKids/Rules` 的 `APNS.list`，改 `build.py` 里的 `EXTRA_DOWNLOAD` / `GENERIC_SERVICES` 即可增删。

## 和 Repcz AppleServers 的区别

`Repcz/Tool` 那份 `AppleServers.yaml` 是「Apple 全家桶一锅端」：`apple.com` + `itunes.com` 整域后缀，
下载、iCloud、APNs 全在一份里，没法分开走。本目录这两份是**互斥配对**，能单独给下载分流。
