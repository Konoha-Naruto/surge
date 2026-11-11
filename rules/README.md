# 规则集（Surge RULE-SET）

分两类：**media** 由 MetaCubeX 的 geosite YAML 转换而来；**apple** 由 blackmatrix7 / HotKids 的 Surge 规则重组（下载与基础服务分开）。都可直接被 Surge 的 `RULE-SET` 订阅。

## 属性分类

| 类目 | 文件 | 条数 | 上游 tag |
|---|---|---|---|
| media | `media/DouYin.list` | 71 | `geosite/douyin.yaml` |
| media | `media/BiliBili.list` | 53 | `geosite/bilibili` + `bilibili-cdn` + `bilibili-game`（合并去重） |
| media | `media/BiliBiliIntl.list` | 11 | `geosite/biliintl.yaml`（国际版，`bilibili.tv` / `bstar` CDN） |
| media | `media/ByteDance.list` | 961 | `geosite/bytedance.yaml`（字节全系，含抖音 / 头条 / 西瓜 / 剪映） |
| apple | `apple/AppleDownload.list` | 88 | App Store / OTA / 固件下载（blackmatrix7 AppStore + SystemOTA） |
| apple | `apple/AppleServices.list` | 99 | APNs / iCloud / 账号激活等基础服务，含 `apple.com` 兜底 |

**apple 那两份有顺序要求：Download 必须在 Services 之前**，详见 [apple/README.md](apple/README.md)。

## 用法

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Konoha-Naruto/surge/main/rules/media/DouYin.list,抖音
RULE-SET,https://raw.githubusercontent.com/Konoha-Naruto/surge/main/rules/media/BiliBili.list,哔哩哔哩
```

策略名换成自己 profile 里已有的策略组 / 策略，否则会报 `unknown policy`。

## 转换规则

| 上游写法（Clash payload） | Surge 输出 |
|---|---|
| `+.example.com` / `*.example.com` | `DOMAIN-SUFFIX,example.com` |
| `example.com`（裸域） | `DOMAIN,example.com` |
| `keyword:xxx` | `DOMAIN-KEYWORD,xxx` |
| `regexp:xxx` | 跳过（Surge 无对应类型） |

已去重、按类型排序，文件头写入来源 tag、条数统计与转换时间。

## 重新生成 / 加新 tag

```bash
python3 build.py        # 覆盖本目录四个 .list
```

改 `build.py` 里的 `JOBS` 表即可增加规则集：

```python
JOBS = {
    "DouYin.list": ("DouYin", ["douyin"], "抖音"),
    ...
}
```

上游 tag 名在 `MetaCubeX/meta-rules-dat` 的 **`meta` 分支** → `geo/geosite/<tag>.yaml`
（`master` 分支已不含规则文件）。例如 `tiktok`、`kuaishou`、`bytedance@ads`、`bilibili2`。

## 校验

```bash
{ echo '[General]'; echo 'loglevel = notify'; echo '[Proxy]'; echo 'DIRECT = direct';
  echo '[Proxy Group]'; echo 'PROXY = select, DIRECT'; echo '[Rule]';
  sed -n '/^[A-Z]/p' media/DouYin.list | sed 's/$/,PROXY/'; echo 'FINAL,DIRECT'; } > /tmp/check.conf
surge-cli --check /tmp/check.conf
```
