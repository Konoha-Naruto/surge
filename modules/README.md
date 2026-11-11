# Surge 模块

按用途属性分目录，一个模块一个文件夹。

| 属性 | 目录 | 模块 | 说明 |
|---|---|---|---|
| media | [`media/qqmusic/`](media/qqmusic/) | `QQMusic.sgmodule` + `qqmusic.js` | QQ音乐：绿钻成长值签到、金币中心签到、App 每日任务、金币抽奖、红包雨；参数 `getck` 控制是否抓 Cookie |
| tools | [`tools/maimemo-capture/`](tools/maimemo-capture/) | `maimemo-capture.sgmodule` + `capture.js` | 墨墨背单词请求抓包，只记录不改包 |
| monitor | [`monitor/vps/`](monitor/vps/) | `vps_monitor.sgmodule` + `vps_panel.js` + 服务端 | VPS 面板：CPU / 内存 / 磁盘 / 月流量 / 运行时长 |

## 安装地址

```
# QQ音乐签到
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/media/qqmusic/QQMusic.sgmodule

# 墨墨抓包
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/tools/maimemo-capture/maimemo-capture.sgmodule

# VPS 监控（需先在服务器跑 modules/monitor/vps/install.sh）
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/monitor/vps/vps_monitor.sgmodule
```

## 添加新模块

1. `modules/<属性>/<名字>/` 放 `.sgmodule` 与它依赖的脚本
2. `script-path` 用本仓库完整 raw 地址，不要写相对路径
3. 需要服务端 / 外部依赖的，把部署脚本一并放进来并在该目录 README 说明
4. 更新本 README 与根 README 的表格
