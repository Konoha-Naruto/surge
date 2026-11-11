#!/usr/bin/env python3
"""把 MaYIHEI/paperclip 的 qqmusic.js 包成 Surge 模块脚本（带「抓取 Cookie」开关）。

上游本身已是 Surge 原生脚本（$request/$persistentStore/$httpClient/...），
这里只在外层加一层「开关」：模块参数 getck=false 时，http-request 脚本直接
$done({}) 放行 —— 不拦截、不读 body、不发通知；cron 任务照常执行。

输出：../qqmusic.js（模块 script-path 指向它）
"""
import hashlib
import pathlib
import urllib.request

UPSTREAM = "https://raw.githubusercontent.com/MaYIHEI/paperclip/refs/heads/main/app/qqmusic/qqmusic.js"
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "qqmusic.js"

HEADER = """// ─────────────────────────────────────────────────────────────
// QQ音乐签到 · Surge 封装版（带「抓取 Cookie」开关）
//
// 原作: MaYIHEI  https://github.com/MaYIHEI/paperclip/tree/main/app/qqmusic
// 上游: {upstream}
// SHA256(上游): {sha}
//
// 开关: 模块参数 getck（默认 true）
//   getck=false → http-request 脚本立即 $done({{ }}) 原样放行，不拦截不通知
//   cron 任务不受开关影响，永远执行
//
// 本文件由 src/build.py 生成，不要手改。
// ─────────────────────────────────────────────────────────────
(function () {{
  var __arg = (typeof $argument !== "undefined" && $argument) || "";
  var __m = /(?:^|[&,\\s])getck\\s*=\\s*([^&,\\s]+)/i.exec(__arg);
  var __v = (__m ? __m[1] : "true").trim().toLowerCase();
  var __off = __v === "false" || __v === "0" || __v === "off" || __v === "no";
  if (typeof $request !== "undefined" && __off) {{
    // 抓包已关闭：请求原样通过
    $done({{}});
    return;
  }}

  // ============ 上游原样执行 ============
"""

FOOTER = """
  // ============ 上游结束 ============
})();
"""


def main() -> None:
    src_bytes = urllib.request.urlopen(UPSTREAM, timeout=30).read()
    sha = hashlib.sha256(src_bytes).hexdigest()
    src = src_bytes.decode("utf-8")
    OUT.write_text(HEADER.format(upstream=UPSTREAM, sha=sha[:16]) + src + FOOTER, encoding="utf-8")
    print(f"wrote {OUT}  {OUT.stat().st_size} bytes  upstream_sha={sha[:16]}")


if __name__ == "__main__":
    main()
