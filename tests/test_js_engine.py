"""JS 引擎（mini-racer）的离线回归测试，不访问网络。

覆盖 akshare 调用 MiniRacer 的三类用法：新浪 hk_js_decode 解码、同花顺 ths.js 与
巨潮 cninfo.js 生成请求 token。CI 在 Linux、macOS、Windows 上都会运行，替换或升级
JS 引擎依赖时由它把关。
"""

import hashlib
import json

import py_mini_racer

from akshare.datasets import get_ths_js
from akshare.stock.cons import hk_js_decode

# 2026-11-03 抓取的 https://finance.sina.com.cn/realstock/company/klc_td_sh.txt
SINA_TRADE_DATE_PAYLOAD = (
    "LC/AAApNDXCw6mHbaPgkryxXv10eAJP1LW0SD39aT7+NV44Xba3PxCgTdrp5BkYVAc11hWvg0c/1"
    "9UAc7jNtHQyWBAu2xmGuZI1NVAc3FepphjnTBw1X4hmGu+ypVAcvFenpBXPqCc6F4ZmGueLFwbIN"
    "8QTDXPsCc1FepphjvOoCc8FepphjvcgFO3CP00wxXXWhrkUdZrIJpw9X3ThrlEp6hlGc88Kcem0V"
    "eFpZM46VV4MrTC2KScKc811U4aLXUdlzINc9lTrwFW3T52KPj0mDueVFuUR1RtiEoCXfdgFOOSGR"
    "XnUhrXWhb0kt6Rk2pU44JV4SrTyU9wSDHPwCnXdP1FuiUM44r7qwdKqcYrIZpw1DqgrlU5IrHRaw"
    "xjrwBaqcbrIt9gr3UhDtOpyVNjEnCHPnC3royNWvi0gjHXBXYdRlLbFpdJFueSFcqkK30sSDO+68"
    "K46IVOwVkaBX/"
)


def test_hk_js_decode_trade_dates():
    ctx = py_mini_racer.MiniRacer()
    ctx.eval(hk_js_decode)
    dates = ctx.call("d", SINA_TRADE_DATE_PAYLOAD)
    assert len(dates) == 8796
    assert dates[0] == "1990-12-19T00:00:00.000Z"
    assert dates[-1] == "2026-12-31T00:00:00.000Z"
    blob = json.dumps(dates, ensure_ascii=False, sort_keys=True)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    assert digest == "1e4d0930cbbebededb659539549734a4da3a18785f5f3a1f91df57081439003d"


def test_bundled_js_tokens():
    for js_file, func in (("ths.js", "v"), ("cninfo.js", "getResCode1")):
        ctx = py_mini_racer.MiniRacer()
        ctx.eval(get_ths_js(js_file).read_text(encoding="utf-8"))
        token = ctx.call(func)
        assert isinstance(token, str) and len(token) > 10, (js_file, token)
