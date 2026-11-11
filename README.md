# Surge

自己用的 Surge 资源：**规则集**（`rules/`）和 **模块**（`modules/`），模块按用途属性分目录。

```
.
├── rules/
│   └── media/            流媒体 / 内容平台分流规则（RULE-SET 订阅的 .list）
└── modules/
    ├── media/            媒体：会员签到、任务
    ├── tools/            工具：抓包、调试
    └── monitor/          监控：面板（含服务端采集脚本）
```

## 规则集

| 属性 | 文件 | 条数 |
|---|---|---|
| media | `rules/media/DouYin.list` | 71 |
| media | `rules/media/BiliBili.list` | 53 |
| media | `rules/media/BiliBiliIntl.list` | 11 |
| media | `rules/media/ByteDance.list` | 961 |

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Konoha-Naruto/surge/main/rules/media/DouYin.list,抖音
RULE-SET,https://raw.githubusercontent.com/Konoha-Naruto/surge/main/rules/media/BiliBili.list,哔哩哔哩
```

来源 MetaCubeX geosite，转换脚本与说明见 [rules/README.md](rules/README.md)。

## 模块

| 属性 | 模块 | 说明 |
|---|---|---|
| media | [qqmusic](modules/media/qqmusic/) | QQ音乐绿钻 / 金币 / 每日任务 / 红包雨签到，参数 `getck` 控制是否抓 Cookie |
| tools | [maimemo-capture](modules/tools/maimemo-capture/) | 墨墨签到请求抓包（只记录不改包） |
| monitor | [vps](modules/monitor/vps/) | VPS CPU / 内存 / 磁盘 / 流量面板（附采集端与部署脚本） |

安装地址规律：

```
https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/<属性>/<模块>/<文件>.sgmodule
```

| 模块 | 安装地址 |
|---|---|
| QQ音乐签到 | https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/media/qqmusic/QQMusic.sgmodule |
| 墨墨抓包 | https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/tools/maimemo-capture/maimemo-capture.sgmodule |
| VPS 监控 | https://raw.githubusercontent.com/Konoha-Naruto/surge/main/modules/monitor/vps/vps_monitor.sgmodule |

## 约定

- 一个模块一个文件夹，模块文件、它引用的脚本、服务端代码、文档都放一起。
- 模块内 `script-path` 写本仓库完整 raw 地址，方便统一更新。
- 全部为个人自用配置，脚本多来自社区作者（文件头已标注来源）。
