# 大众评球 去广告

拦截大众评球 App 的广告位配置下发与广告素材竞价，所有请求统一回**空对象**（`{}`），App 侧判定为「无填充」，广告位保持空白。装后清缓存或重装 App 生效。

## 文件

| 文件 | 说明 |
|---|---|
| `DazhongPingqiu.sgmodule` | 精简版，命中 3 个端点 |
| `DazhongPingqiu-Enhanced.sgmodule` | 增强版 = 精简版 + dsocial 全量 `ad_` 系列通配，抗改名 |

安装：

```
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/ads/dazhong-pingqiu/DazhongPingqiu.sgmodule
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/ads/dazhong-pingqiu/DazhongPingqiu-Enhanced.sgmodule
```

## 拦截的端点

| 端点 | 作用 | 处理 |
|---|---|---|
| `https://api.wxcjgg.cn/ad/map` | 广告位映射表，App 启动时拉一次，决定哪些位置放广告 | → `{}` |
| `http://api-tx.dsocial.xyz/api/v2/ad_config` | dsocial 广告配置（开屏 / 插屏参数） | → `{}` |
| `http?://api-tx.dsocial.xyz/api/*/ad_` | 增强版专有：dsocial 全部 `ad_` 系接口 | → `" "` |
| `http(s)://fg.xiawan8.com/rtb` | 夏玩（xiawan8）RTB 实时竞价入口 | → `{}` |

### 关于 `fg.xiawan8.com/rtb`

OpenRTB 竞价接口，参数 `v`（接口版本）、`mid`（媒体 ID）、`slot`（广告位 ID）、`fan`（返回格式开关）。实测行为：

- `POST` 标准竞价包会回填 `id` → `{"nbr":1002,"bidid":"<id>","id":"<id>"}`，`nbr=1002` 即自定义「无合适广告」
- `v=206/208` 分别回 `seat_bid` / `ad` 结构，`v=227` 回 AES 密文
- 无参数访问回 `502 unkown request`

模块用 `{}` 代替服务端真实的 `{"nbr":1002,...}`：App 的其它广告接口本来就被本模块喂 `{}` 并正常工作，兼容路径已被现网验证；相比 `REJECT` 的 TCP RST，这种方式吃一次正常 200，SDK 直接走 no-bid 分支，网络层零报错、零重试。

## 依赖

- `[Map Local]` 对 `https` 端点需开启 MITM，模块已把三个域名加进 `hostname`
- 首次导入后到 Surge → 模块确认开关为开启状态

## 验证

```sh
curl -sS -m 6 -w '\n%{http_code}\n' "http://fg.xiawan8.com/rtb?v=227&mid=426&slot=36297872&fan=1"
```

生效后返回 `{}` + `200`；原样是一行 44 字符 base64。

Surge 侧确认：

```sh
surge-cli rule match fg.xiawan8.com
surge-cli module show "大众评球去广告"
```

`module show` 的 section 计数里应出现 `Map Local 4`（增强版）/ `Map Local 4`（精简版 4 条中的 3 条业务 + 1 条 rtb）。

## 来源

基础规则来自 `QingRex/LoonKissSurge`（sliverkiss 版）与 `gys619` 开屏广告集；`fg.xiawan8.com` 由本项目补入。
