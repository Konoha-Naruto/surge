# 波点音乐（Surge）

波点音乐 **会员标识解锁 + 无损/付费专辑下载 + 付费专辑解锁 + 去广告**。纯响应体改写，不抓 Cookie、不签到，装完开代理即生效。

上游脚本：[WeiGiegie/666 · bdyy.js](https://github.com/WeiGiegie/666/blob/main/bdyy.js)（176 KB，javascript-obfuscator 混淆，Surge/QuanX/Loon 三平台自动适配）。

Egern 版在另一个仓库：[Konoha-Naruto/egern](https://github.com/Konoha-Naruto/egern/tree/main/modules/media/bodian-music)。

## 文件

| 文件 | 说明 |
|---|---|
| `BodianMusic.sgmodule` | Surge 模块：1 条 `http-response` 脚本 + 1 条 `reject-200` 重写 + 20 个 MITM 主机名 |
| `bdyy.js` | 上游脚本的**原样镜像**（176,784 B，SHA256 前 16 位 `9f1ed2a7f54bff17`），未做任何改动 |

## 安装

```
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/media/bodian-music/BodianMusic.sgmodule
```

Surge → 首页 → 模块 → 安装新模块 → 粘贴 URL；装完确认 MITM 已开、证书已信任。

## 生效范围

| 功能 | 命中接口（前缀） |
|---|---|
| 会员标识 / VIP 状态 | `bd-api.kuwo.cn/api/ucenter/users/(pub\|login)`、`pay/vip/*`、`sp/actVip` |
| 音质 / 播放权限 | `play/music/v2/(audioUrl\|checkRight)` |
| 下载 / 付费专辑 | `service/music/(info\|download/info\|download/config)`、`pay/audition/url` |
| 开屏 / 弹窗 / 悬浮广告 | `popup/start/info`、`advert/*`、`pay/vip/invitation/assist/popup` |
| 横幅 / 商城 Tab / 首页模块 | `service/banner/*`、`service/home/module`、`global/config/(scene\|vipEnter)` |
| 搜索热词 | `search/topic/word/list` |
| 开屏联盟广告（第三方） | `us.l.qq.com/exapp`、`xs.gdt.qq.com/style_factory/template_list` |
| 腾讯音乐联盟广告域名 | `tmeadcomm.y.qq.com` → `reject-200`（200 空响应） |

推荐流、ABTest、收听上报这类接口也会过一遍脚本（`rec/feed`、`abtest/ui/info`），只做字段裁剪。

## 参数

无。模块没有 `#!arguments`，装上就跑。

## 注意

- **建议先卸载重装波点音乐**再启用：广告位 / 会员状态会缓存在 App 本地，旧缓存会让效果看起来没生效。
- 脚本只在 `2 MB` 以内响应体上执行（`max-size=2097152`）。上游示例里的 `max-size=0` 在 Surge 语义下是「上限 0 字节」，会直接跳过脚本，别抄。
- 混淆脚本的单次执行约 1.2–1.4 s（字符串解码 + 反调试开销），这是上游本身的成本。
- MITM 列表里 `public-ip-*`、`39.156.12*.*`、`*.kuwo.*` 这类条目来自上游，是波点音乐的多域名 / IP 直连兜底，照抄保留。

## 更新脚本

上游更新后重新镜像即可（模块通过 `script-path` 指向本仓库，所以只要推一次）：

```bash
cd modules/media/bodian-music
curl -sL https://raw.githubusercontent.com/WeiGiegie/666/main/bdyy.js -o bdyy.js
sha256sum bdyy.js | cut -c1-16     # 记到本 README 的表里
```

## 校验记录（2026-11-18）

- `bdyy.js` 与上游逐字节一致：176,784 B / SHA256 `9f1ed2a7f54bff17…`
- 模块正则与上游 `[rewrite_local]` 完全一致（571 字符），`new RegExp()` 可编译
- MITM 20 条 = 上游 24 条去重去端口

## 来源

脚本作者 WeiGiegie，模块封装 Konoha-Naruto。仅供个人学习交流。
