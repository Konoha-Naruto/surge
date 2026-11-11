#!/usr/bin/env python3
"""把 MetaCubeX/meta-rules-dat 的 geosite YAML 转成 Surge RULE-SET .list

用法: python3 build.py
产物: 同目录下 DouYin.list / BiliBili.list 等，可直接 RULE-SET 订阅。
"""
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

BASE = "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/"
OUT = os.path.dirname(os.path.abspath(__file__))

# 输出文件名 -> (显示名, [源 yaml 标签...], 说明)
JOBS = {
    "DouYin.list": ("DouYin", ["douyin"], "抖音（MetaCubeX geosite:douyin）"),
    "BiliBili.list": ("BiliBili", ["bilibili", "bilibili-cdn", "bilibili-game"],
                      "哔哩哔哩（bilibili + cdn + game 合并去重）"),
    "BiliBiliIntl.list": ("BiliBiliIntl", ["biliintl"], "哔哩哔哩国际版"),
    "ByteDance.list": ("ByteDance", ["bytedance"], "字节跳动全系（含抖音/头条/西瓜，961 条）"),
}


def fetch(tag):
    url = BASE + tag + ".yaml"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8")
        except Exception as e:  # noqa: BLE001
            err = e
    raise SystemExit(f"下载失败 {tag}: {err}")


def convert(text):
    """Clash/mihomo geosite payload -> [(surge_type, value)]"""
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("- "):
            continue
        v = line[2:].strip().strip("'\"")
        if not v:
            continue
        low = v.lower()
        if low.startswith("+."):                 # +.example.com -> 后缀匹配
            out.append(("DOMAIN-SUFFIX", v[2:]))
        elif low.startswith("*."):               # *.example.com -> 后缀匹配
            out.append(("DOMAIN-SUFFIX", v[2:]))
        elif low.startswith("domain:"):
            out.append(("DOMAIN", v[len("domain:"):]))
        elif low.startswith("keyword:"):
            out.append(("DOMAIN-KEYWORD", v[len("keyword:"):]))
        elif low.startswith("regexp:"):
            # Surge 无 DOMAIN-REGEX，退化为 DOMAIN-SUFFIX 不可接受，直接跳过并计数
            out.append(("__SKIP__", v[len("regexp:"):]))
        elif low.startswith("full:"):
            out.append(("DOMAIN", v[5:]))
        else:
            out.append(("DOMAIN", v))
    # 去重保序
    seen, uniq = set(), []
    for item in out:
        if item not in seen:
            seen.add(item)
            uniq.append(item)
    return uniq


def write_list(name, display, tags, note):
    rules, skipped = [], 0
    for tag in tags:
        for t, v in convert(fetch(tag)):
            if t == "__SKIP__":
                skipped += 1
                continue
            rules.append((t, v))
    # 全局去重
    seen, uniq = set(), []
    for item in rules:
        if item not in seen:
            seen.add(item)
            uniq.append(item)
    # 排序：先 DOMAIN，再 DOMAIN-SUFFIX，再其他，各自字典序
    order = {"DOMAIN": 0, "DOMAIN-SUFFIX": 1, "DOMAIN-KEYWORD": 2}
    uniq.sort(key=lambda x: (order.get(x[0], 9), x[1]))

    counts = {}
    for t, _ in uniq:
        counts[t] = counts.get(t, 0) + 1

    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# NAME: {display}",
        "# AUTHOR: MetaCubeX (surge-converted)",
        "# REPO: https://github.com/MetaCubeX/meta-rules-dat",
        f"# SOURCE: {', '.join('geo/geosite/' + t + '.yaml' for t in tags)}",
        f"# DESC: {note}",
        f"# UPDATED: {now}",
    ]
    for t, c in counts.items():
        lines.append(f"# {t}: {c}")
    lines.append(f"# TOTAL: {len(uniq)}")
    if skipped:
        lines.append(f"# SKIPPED(regexp): {skipped}")
    lines.append("")
    lines += [f"{t},{v}" for t, v in uniq]

    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path, len(uniq), counts


if __name__ == "__main__":
    for fname, (display, tags, note) in JOBS.items():
        p, n, counts = write_list(fname, display, tags, note)
        print(f"{os.path.basename(p):20s} {n:4d} 条  {counts}")
