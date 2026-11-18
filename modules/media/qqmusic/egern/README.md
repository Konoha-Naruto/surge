# QQ音乐签到 · Egern 原生版

- `QQMusic.yaml`：Egern 原生模块，含一条请求脚本、三个定时任务和单域名 MITM。
- `qqmusic-egern.js`：原生 JavaScript 脚本，使用 `ctx.request`、`ctx.storage`、`ctx.http` 和 `ctx.notify`。

## 安装

1. 停用旧 Surge 模块，避免重复任务。打开 [Egern 一键安装](egern:/modules/new?url=https%3A%2F%2Fraw.githubusercontent.com%2FKonoha-Naruto%2Fsurge%2Fegern-qqmusic%2Fmodules%2Fmedia%2Fqqmusic%2Fegern%2FQQMusic.yaml)，或将 [YAML 原始链接](https://raw.githubusercontent.com/Konoha-Naruto/surge/egern-qqmusic/modules/media/qqmusic/egern/QQMusic.yaml) 粘贴到 Egern 的模块添加页。
2. 仅在自己的设备和账号上使用。启用 Egern MITM 并确认其证书已受信任；模块只包含 `u6.y.qq.com`。
3. 保持 `getck=true`，打开已登录的 QQ 音乐「会员中心 → 每日签到」或「金币中心 → 每日签到」。收到保存成功通知后可设 `getck=false`；这不会关闭定时任务，也不会从模块移除 MITM 域名。
4. 从 Surge 保存的登录状态不会随模块自动迁移。不要把 Cookie 或 `refresh_key` 贴到模块配置、日志或聊天里。

## 调度

沿用原模块时段：07:30 每日任务，09:00–10:59 每分钟检查定时金币，00/08/12/16/20/22 点的第 5 分钟检查红包雨。计划脚本超时改为 Egern 支持的 600 秒。保留原脚本的任务去重与时段判断。

本地通过 YAML/JS 语法校验，以及登录状态缺失、抓取关闭、读取模拟登录态、模拟每日调度及去重测试。未在 Egern 真机导入，也未使用真实 QQ 账号提交请求。任务能否成功仍取决于 Egern 版本和 QQ 音乐接口。

原作：[MaYIHEI](https://github.com/MaYIHEI/paperclip/tree/main/app/qqmusic)；参照 [Konoha-Naruto 的 Surge 封装](https://github.com/Konoha-Naruto/surge/tree/main/modules/media/qqmusic)。
