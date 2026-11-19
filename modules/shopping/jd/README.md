# 京东（去广告 + 历史比价）· Surge 版

从 Loon 插件 [`京东去广告.Ipx`](https://raw.githubusercontent.com/jadkg/egern/refs/heads/main/京东去广告.Ipx)（`jadkg/egern`，2026-10-02）移植。

安装：

```
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/shopping/jd/JD.sgmodule
```

## 功能

| 块 | 作用 | 实现 |
|---|---|---|
| 开屏/启动图 | `m.360buyimg.com/mobilecms/s1125x2436_jfs` 回空 200 | Map Local |
| 特殊登录入口 | `api.m.jd.com/?loginType=11` 回 `{}` | Map Local |
| 推荐位 | 购物车优惠券推荐 / 智能推荐 / 搜索框热词 / 首页推荐等 7 个 functionId 回 `{}` | Map Local |
| 京东极速版广告 | `lite_advertising` 响应体 `jdLiteAdvertisingVO` → `sooyaaabo` | Body Rewrite |
| 主 App 广告 | 首页 / 我的 / 订单 / 物流 / 启动 / 欢迎页楼层清理 | `jingdong.js`（jadkg） |
| 工具箱 404 | `getWidgetV1052` 返回 404，避免客户端反复拉取 | `jd_patch.js` |
| 基础配置静默 | 关掉 socket 预连接与 httpdns 上报 | `jd_patch.js` |
| 购物车空楼层 | 删 `loc_emptyCartFloor2` / `emptyCartRecommendFloor` | `jd_patch.js` |
| 慢慢买 Cookie | 打开【慢慢买 App → 我的】自动抓 ck | `mw418/Loon` 的 `jd_price.js` |
| 详情页比价 | 商品页嵌入历史价格表（表格图） | `wf021325/qx` 的 `jd_price.js` |

## 与 Loon 原插件的差异（转换时踩到的）

1. **`reject-200` / `reject-dict` 在 Surge 不存在**。`surge-cli --check` 报 `Unknown URL rewrite type: reject-200. Use header, 302, 307 or reject.` → 全部改 `[Map Local]`：`reject(200)` 变 `data="" status-code=200`，`reject_dict(200)` 变 `data="{}" status-code=200`。比 `URL Rewrite` 的 `reject`（403 + RST）更贴近原语义，App 不会重试。
2. **`response.body.replace`** → `[Body Rewrite]`（`http-response <url> <regex> <replacement>`）。
3. **`response.json.replace/delete`** 没有声明式等价物 → `jd_patch.js` 用 `$argument` 分模式（`basicconfig` / `cart`）处理，路径逐级创建，父级缺失也不会抛错。
4. **`with enable=${开关}` 在 Surge 模块里没有等价语法**（`[Script]` 不支持条件启用）。所以互斥的三种比价展示方式用「注释」切换：默认只启用详情嵌入（表格图），与 Loon 默认一致。
5. 原插件 `[Rule]` 里那条 `AND,((DOMAIN,api.m.jd.com),(PROTOCOL,TCP)),REJECT-NO-DROP` **本身是注释掉的**，照抄会整条阻断京东 API，这里没有带过来。
6. 「详情嵌入（折线图）」指向 `https://loon.103516.xyz/Script/JingDong/JingDong.price.js`，该地址现在 302 到 `https://t.me/BoStudioHub`，脚本已下线，模块里留了说明不再提供。

## 使用

1. 装模块 → 开 MITM（`api.m.jd.com`、`in.m.jd.com`、`apapia-sqk-weblogic.manmanbuy.com`、`m.360buyimg.com` 由模块用 `%APPEND%` 追加）；
2. 首次比价前打开【慢慢买 App → 我的】，看到「获取ck成功🎉」；
3. 京东 App 冷启动一次（后台划掉再开），旧的楼层缓存才会消失；
4. 想换比价样式：编辑模块文件，给想要的那行去掉 `#`、给默认那行加上 `#`，再重新安装。

## 验证

- `surge-cli --check`（拼最小 profile + `FINAL,DIRECT`）：`OK`
- `jd_patch.js` node 模拟：`basicconfig` 三条路径置 0、`cart` 两条删除、非法 JSON 原样放行、`widget404` 返回 404 空体
- 上游脚本可用性：`jingdong.js` 200 / 10476 B，`mw418 jd_price.js` 200 / 28692 B，`wf021325 jd_price.js` 200 / 32686 B
