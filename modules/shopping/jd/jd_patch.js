/**
 * 京东去广告 · Surge 补丁脚本
 * 由 Loon 插件「京东去广告.Ipx」(jadkg/egern) 里的声明式改写转写：
 *   widget404   → 原 request ... reject(404)
 *   basicconfig → 原 response.json.replace([...], [0,0,0])
 *   cart        → 原 response.json.delete([...])
 * 模式通过模块里的 argument= 传入，一个脚本吃三种活。
 */

const mode = String(typeof $argument === "string" ? $argument : "").trim();

function zero(obj, path) {
  const keys = path.split(".");
  let cur = obj;
  for (let i = 0; i < keys.length - 1; i++) {
    const k = keys[i];
    if (typeof cur[k] !== "object" || cur[k] === null) cur[k] = {};
    cur = cur[k];
  }
  cur[keys[keys.length - 1]] = 0;
}

function del(obj, path) {
  const keys = path.split(".");
  let cur = obj;
  for (let i = 0; i < keys.length - 1; i++) {
    const k = keys[i];
    if (typeof cur[k] !== "object" || cur[k] === null) return;
    cur = cur[k];
  }
  delete cur[keys[keys.length - 1]];
}

if (mode === "widget404") {
  $done({
    response: {
      status: 404,
      headers: { "Content-Type": "application/json" },
      body: "",
    },
  });
} else {
  let obj = null;
  try {
    obj = JSON.parse($response.body);
  } catch (e) {
    obj = null;
  }
  if (!obj || typeof obj !== "object") {
    $done({});
  } else {
    if (mode === "basicconfig") {
      [
        "data.JDMessage.socketmonitor.isSocketEstablishedAhead",
        "data.JDMessage.socketmonitor.isSocketReport",
        "data.JDHttpToolKit.httpdns.httpdns",
      ].forEach((p) => zero(obj, p));
    } else if (mode === "cart") {
      ["cartLocationMap.loc_emptyCartFloor2", "emptyCartRecommendFloor"].forEach(
        (p) => del(obj, p)
      );
    }
    $done({ body: JSON.stringify(obj) });
  }
}
