/*
@Name: PingMe 获取签到参数（Surge 移植版）
@Description: 拦截 PingMe 余额查询请求，自动捕获请求 URL 与全部请求头
@Author: fmz200 → mickeu（Egern 版）→ Surge 移植
@Date: 2026-10-22
@Note: 由 Egern v2 API 改写为 Surge 原生 API
*/

var ckKey = 'pingme_capture_v3';
var NOTIFY_ICON = 'https://raw.githubusercontent.com/axhani/icon/refs/heads/main/pingme&wetalk.png';

function parseRawQuery(url) {
  var idx = url.indexOf('?');
  if (idx === -1) return {};
  var qs = url.substring(idx + 1);
  var params = {};
  qs.split('&').forEach(function (pair) {
    var kv = pair.split('=');
    var k = decodeURIComponent(kv[0] || '');
    var v = decodeURIComponent(kv[1] || '');
    if (k) params[k] = v;
  });
  return params;
}

function normalizeHeaderNameMap(headers) {
  var normalized = {};
  Object.keys(headers || {}).forEach(function (k) {
    normalized[k.toLowerCase()] = headers[k];
  });
  return normalized;
}

(function () {
  try {
    // 开关：模块参数 PINGME_CAPTURE，默认 true
    var arg = '';
    try { arg = (typeof $argument !== 'undefined' && $argument) ? String($argument) : ''; } catch (e) { arg = ''; }
    var cap = arg.trim().toLowerCase();
    if (cap.indexOf('PINGME_CAPTURE=') === 0) cap = cap.split('=')[1];
    if (cap === 'false' || cap === '0' || cap === 'off' || cap === 'no') {
      console.log('⏸ PingMe 已关闭，跳过抓参');
      return $done({});
    }

    var url = ($request && $request.url) || '';
    var headers = ($request && $request.headers) || {};
    console.log('PingMe 开始抓参: ' + url);

    if (url.indexOf('/app/queryBalanceAndBonus') >= 0) {
      var capture = {
        url: url,
        paramsRaw: parseRawQuery(url),
        headers: normalizeHeaderNameMap(headers)
      };
      $persistentStore.write(JSON.stringify(capture), ckKey);
      $notification.post('✅ PingMe 获取成功', '', '参数已保存，可在模块参数里关闭抓参了', {
        'media-url': NOTIFY_ICON,
        sound: true
      });
      console.log('PingMe 获取到的内容为：' + url);
    }
  } catch (e) {
    console.log('PingMe 抓参异常: ' + (e && e.message ? e.message : String(e)));
  }
  $done({});
})();
