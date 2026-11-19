# Surge 模块

按用途属性分目录，一个模块一个文件夹。

| 属性 | 目录 | 模块 | 说明 |
|---|---|---|---|
| media | [`media/qqmusic/`](media/qqmusic/) | `QQMusic.sgmodule` + `qqmusic.js` | QQ音乐：绿钻成长值签到、金币中心签到、App 每日任务、金币抽奖、红包雨；参数 `getck` 控制是否抓 Cookie |
| media | [`media/bodian-music/`](media/bodian-music/) | `BodianMusic.sgmodule` + `bdyy.js` | 波点音乐：会员标识、无损/付费专辑下载、付费专辑解锁、开屏/横幅/悬浮广告与商城 Tab 移除（纯 body 改写，无参数） |
| tools | [`tools/maimemo-capture/`](tools/maimemo-capture/) | `maimemo-capture.sgmodule` + `capture.js` | 墨墨背单词请求抓包，只记录不改包 |
| tools | [`tools/pingme-checkin/`](tools/pingme-checkin/) | `PingMe.sgmodule` + `checkin.js` + `capture.js` | PingMe 每日签到 + 视频奖励，自动抓取签到参数（每次随机设备 ID）；参数 `PROXY` / `CRON` / `PINGME_CAPTURE` |
| monitor | [`monitor/vps/`](monitor/vps/) | `vps_monitor.sgmodule` + `vps_panel.js` + 服务端 | VPS 面板：CPU / 内存 / 磁盘 / 月流量 / 运行时长 |
| ads | [`ads/google/`](ads/google/) | `Google.sgmodule` | Google 广告/统计域名 REJECT 50 条（doubleclick、googlesyndication、admob、analytics、firebase 等），纯规则无 MITM |
| ads | [`ads/dazhong-pingqiu/`](ads/dazhong-pingqiu/) | `DazhongPingqiu.sgmodule` + 增强版 | 大众评球广告位/开屏/夏玩 RTB 竞价清零，广告接口统一回 `{}` |
| shopping | [`shopping/jd/`](shopping/jd/) | `JD.sgmodule` + `jd_patch.js` | 京东：首页/订单/物流/购物车/推荐位/工具箱去广告 + 慢慢买历史比价（Loon `京东去广告.Ipx` 移植） |

## 安装地址

```
# QQ音乐签到
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/media/qqmusic/QQMusic.sgmodule

# 波点音乐
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/media/bodian-music/BodianMusic.sgmodule

# 墨墨抓包
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/tools/maimemo-capture/maimemo-capture.sgmodule

# PingMe 自动签到
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/tools/pingme-checkin/PingMe.sgmodule

# VPS 监控（需先在服务器跑 modules/monitor/vps/install.sh）
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/monitor/vps/vps_monitor.sgmodule

# 京东去广告 + 历史比价
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/shopping/jd/JD.sgmodule

# Google 去广告（规则版）
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/ads/google/Google.sgmodule
```

## 添加新模块

1. `modules/<属性>/<名字>/` 放 `.sgmodule` 与它依赖的脚本
2. `script-path` 用本仓库完整 raw 地址，不要写相对路径
3. 需要服务端 / 外部依赖的，把部署脚本一并放进来并在该目录 README 说明
4. 更新本 README 与根 README 的表格
