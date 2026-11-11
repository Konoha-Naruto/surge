#!/usr/bin/env python3
"""生成 Apple「下载」与「基础服务」两份分开的 Surge 规则集。

下载类（AppleDownload.list）：App Store 商店/App 本体、系统更新、固件、商店图片 CDN
基础服务（AppleServices.list）：APNs、账号/激活、iCloud、其余 Apple 服务

数据来源（blackmatrix7/ios_rule_script，Surge 分支）+ 少量手工补齐。
两份是「先下载后服务」的配对关系：服务那份带了 apple 系的兜底关键词，
所以规则顺序必须是 Download 在前。
"""
import pathlib
import urllib.request

BASE = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge"
APNS = "https://raw.githubusercontent.com/HotKids/Rules/master/Surge/RULE-SET/Apple/APNS.list"
OUT = pathlib.Path(__file__).resolve().parent

# 上游文件 -> 本地缓存名
SRC = {
    "AppStore": f"{BASE}/AppStore/AppStore.list",
    "SystemOTA": f"{BASE}/SystemOTA/SystemOTA.list",
    "iCloud": f"{BASE}/iCloud/iCloud.list",
    "AppleID": f"{BASE}/AppleID/AppleID.list",
    "Apple": f"{BASE}/Apple/Apple.list",
    "APNS": APNS,
}

# 手工补齐：App Store 商店与 App 本体、图片/预览 CDN、更新分发
EXTRA_DOWNLOAD = [
    "DOMAIN-SUFFIX,iosapps.itunes.apple.com",
    "DOMAIN-SUFFIX,iosapps.apple.com",
    "DOMAIN-SUFFIX,appsto.re",
    "DOMAIN-SUFFIX,appstore.com",
    "DOMAIN-SUFFIX,mzstatic.com",
    "DOMAIN-SUFFIX,swcdn.apple.com",
    "DOMAIN-SUFFIX,swdist.apple.com",
    "DOMAIN-SUFFIX,oscdn.apple.com",
    "DOMAIN-SUFFIX,appldnld.apple.com",
]

# 兜底：下载类已被 AppleDownload 精确命中，这里收「其余所有 Apple 流量」
# 必须在 Download 之后生效（同一条 rule-set 顺序）
GENERIC_SERVICES = [
    "DOMAIN-SUFFIX,apple.com",
    "DOMAIN-SUFFIX,aaplimg.com",
    "DOMAIN-SUFFIX,apple-dns.net",
]

# Apple 里混了 USER-AGENT / PROCESS-NAME，规则集里不带这些（设备相关，容易误伤）
DROP_TYPES = {"USER-AGENT", "PROCESS-NAME"}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def rules_of(text: str):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.split(",", 1)[0].strip().upper() in DROP_TYPES:
            continue
        if line.startswith(("DOMAIN", "IP-CIDR", "IP-CIDR6", "PROCESS-NAME", "USER-AGENT")):
            out.append(line)
    return out


def key(line: str) -> str:
    parts = [p.strip() for p in line.split(",")]
    return ",".join(parts[:2]).lower()


def dedupe(lines):
    seen, out = set(), []
    for l in lines:
        k = key(l)
        if k not in seen:
            seen.add(k)
            out.append(l)
    return out


ORDER = {"DOMAIN": 0, "DOMAIN-SUFFIX": 1, "DOMAIN-KEYWORD": 2, "IP-CIDR": 3, "IP-CIDR6": 4}


def sort_key(line: str):
    parts = line.split(",")
    return (ORDER.get(parts[0].strip().upper(), 9), parts[1].strip().lower())


def write(name: str, title: str, desc: str, lines, sources: str):
    lines = sorted(dedupe(lines), key=sort_key)
    counts = {}
    for l in lines:
        t = l.split(",", 1)[0].strip().upper()
        counts[t] = counts.get(t, 0) + 1
    head = [
        f"# NAME: {title}",
        "# AUTHOR: blackmatrix7 / HotKids (surge ruleset)",
        f"# SOURCE: {sources}",
        f"# DESC: {desc}",
    ]
    for t, c in counts.items():
        head.append(f"# {t}: {c}")
    head.append(f"# TOTAL: {len(lines)}")
    p = OUT / name
    p.write_text("\n".join(head + [""] + lines) + "\n", encoding="utf-8")
    print(f"{name:22s} {len(lines):4d} 条  {counts}")
    return set(key(l) for l in lines)


def main():
    texts = {k: fetch(u) for k, u in SRC.items()}

    # ---------- 下载 ----------
    download = []
    download += rules_of(texts["AppStore"])          # apps.apple.com / itunes.apple.com
    download += rules_of(texts["SystemOTA"])         # OTA 全链路（含 updates*.cdn-apple.com）
    download += EXTRA_DOWNLOAD
    dl_keys = write(
        "AppleDownload.list",
        "AppleDownload",
        "App Store 商店与 App 下载、iOS/macOS 系统更新与固件 CDN",
        download,
        "blackmatrix7 AppStore + SystemOTA，另补 iosapps/mzstatic/swcdn 等",
    )

    # ---------- 基础服务 ----------
    services = []
    services += rules_of(texts["APNS"])              # APNs（含 IP 集合）
    services += rules_of(texts["AppleID"])           # 账号
    services += rules_of(texts["iCloud"])            # iCloud
    services += rules_of(texts["Apple"])             # 激活/推送/地图等关键词 + IP 集合
    services += GENERIC_SERVICES                     # 其余 Apple 流量兜底

    # 下载里已经精确列过的，服务里去掉（避免同一域名两边都有、靠顺序决定）
    services = [l for l in services if key(l) not in dl_keys]
    write(
        "AppleServices.list",
        "AppleServices",
        "APNs、账号/激活、iCloud 等 Apple 基础服务（不含下载类）",
        services,
        "blackmatrix7 AppleID + iCloud + Apple，APNs 取 HotKids Apple/APNS",
    )


if __name__ == "__main__":
    main()
