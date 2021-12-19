#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/12/19 12:54
Desc: 乐咕乐股-A 股市净率
https://www.legulegu.com/stockdata/market_pb
此网站需要 JS 逆向分析 token 代码，本项目分解 JS 加密部分，提取主要的加密参数后本地执行
"""
from datetime import datetime

import pandas as pd
import requests
from py_mini_racer import py_mini_racer

hash_code = """
function e(n) {
    var e, t, r = "", o = -1, f;
    if (n && n.length) {
        f = n.length;
        while ((o += 1) < f) {
            e = n.charCodeAt(o);
            t = o + 1 < f ? n.charCodeAt(o + 1) : 0;
            if (55296 <= e && e <= 56319 && 56320 <= t && t <= 57343) {
                e = 65536 + ((e & 1023) << 10) + (t & 1023);
                o += 1
            }
            if (e <= 127) {
                r += String.fromCharCode(e)
            } else if (e <= 2047) {
                r += String.fromCharCode(192 | e >>> 6 & 31, 128 | e & 63)
            } else if (e <= 65535) {
                r += String.fromCharCode(224 | e >>> 12 & 15, 128 | e >>> 6 & 63, 128 | e & 63)
            } else if (e <= 2097151) {
                r += String.fromCharCode(240 | e >>> 18 & 7, 128 | e >>> 12 & 63, 128 | e >>> 6 & 63, 128 | e & 63)
            }
        }
    }
    return r
}

function t(n) {
    var e, t, r, o, f, i = [], h;
    e = t = r = o = f = 0;
    if (n && n.length) {
        h = n.length;
        n += "";
        while (e < h) {
            r = n.charCodeAt(e);
            t += 1;
            if (r < 128) {
                i[t] = String.fromCharCode(r);
                e += 1
            } else if (r > 191 && r < 224) {
                o = n.charCodeAt(e + 1);
                i[t] = String.fromCharCode((r & 31) << 6 | o & 63);
                e += 2
            } else {
                o = n.charCodeAt(e + 1);
                f = n.charCodeAt(e + 2);
                i[t] = String.fromCharCode((r & 15) << 12 | (o & 63) << 6 | f & 63);
                e += 3
            }
        }
    }
    return i.join("")
}

function r(n, e) {
    var t = (n & 65535) + (e & 65535)
        , r = (n >> 16) + (e >> 16) + (t >> 16);
    return r << 16 | t & 65535
}

function o(n, e) {
    return n << e | n >>> 32 - e
}

function f(n, e) {
    var t = e ? "0123456789ABCDEF" : "0123456789abcdef", r = "", o, f = 0, i = n.length;
    for (; f < i; f += 1) {
        o = n.charCodeAt(f);
        r += t.charAt(o >>> 4 & 15) + t.charAt(o & 15)
    }
    return r
}

function i(n) {
    var e, t = n.length, r = "";
    for (e = 0; e < t; e += 1) {
        r += String.fromCharCode(n.charCodeAt(e) & 255, n.charCodeAt(e) >>> 8 & 255)
    }
    return r
}

function h(n) {
    var e, t = n.length, r = "";
    for (e = 0; e < t; e += 1) {
        r += String.fromCharCode(n.charCodeAt(e) >>> 8 & 255, n.charCodeAt(e) & 255)
    }
    return r
}

function u(n) {
    var e, t = n.length * 32, r = "";
    for (e = 0; e < t; e += 8) {
        r += String.fromCharCode(n[e >> 5] >>> 24 - e % 32 & 255)
    }
    return r
}

function a(n) {
    var e, t = n.length * 32, r = "";
    for (e = 0; e < t; e += 8) {
        r += String.fromCharCode(n[e >> 5] >>> e % 32 & 255)
    }
    return r
}

function c(n) {
    var e, t = n.length * 8, r = Array(n.length >> 2), o = r.length;
    for (e = 0; e < o; e += 1) {
        r[e] = 0
    }
    for (e = 0; e < t; e += 8) {
        r[e >> 5] |= (n.charCodeAt(e / 8) & 255) << e % 32
    }
    return r
}

function l(n) {
    var e, t = n.length * 8, r = Array(n.length >> 2), o = r.length;
    for (e = 0; e < o; e += 1) {
        r[e] = 0
    }
    for (e = 0; e < t; e += 8) {
        r[e >> 5] |= (n.charCodeAt(e / 8) & 255) << 24 - e % 32
    }
    return r
}

function D(n, e) {
    var t = e.length, r = Array(), o, f, i, h, u, a, c, l;
    a = Array(Math.ceil(n.length / 2));
    h = a.length;
    for (o = 0; o < h; o += 1) {
        a[o] = n.charCodeAt(o * 2) << 8 | n.charCodeAt(o * 2 + 1)
    }
    while (a.length > 0) {
        u = Array();
        i = 0;
        for (o = 0; o < a.length; o += 1) {
            i = (i << 16) + a[o];
            f = Math.floor(i / t);
            i -= f * t;
            if (u.length > 0 || f > 0) {
                u[u.length] = f
            }
        }
        r[r.length] = i;
        a = u
    }
    c = "";
    for (o = r.length - 1; o >= 0; o--) {
        c += e.charAt(r[o])
    }
    l = Math.ceil(n.length * 8 / (Math.log(e.length) / Math.log(2)));
    for (o = c.length; o < l; o += 1) {
        c = e[0] + c
    }
    return c
}

function B(n, e) {
    var t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", r = "", o = n.length, f, i, h;
    e = e || "=";
    for (f = 0; f < o; f += 3) {
        h = n.charCodeAt(f) << 16 | (f + 1 < o ? n.charCodeAt(f + 1) << 8 : 0) | (f + 2 < o ? n.charCodeAt(f + 2) : 0);
        for (i = 0; i < 4; i += 1) {
            if (f * 8 + i * 6 > n.length * 8) {
                r += e
            } else {
                r += t.charAt(h >>> 6 * (3 - i) & 63)
            }
        }
    }
    return r
}

function hex(n) {
    return f(u(n, h), t)
}

function u(n) {
    n = h ? e(n) : n;
    return a(C(c(n), n.length * 8))
}

function l(n, t) {
    var r, o, f, i, u;
    n = h ? e(n) : n;
    t = h ? e(t) : t;
    r = c(n);
    if (r.length > 16) {
        r = C(r, n.length * 8)
    }
    o = Array(16),
        f = Array(16);
    for (u = 0; u < 16; u += 1) {
        o[u] = r[u] ^ 909522486;
        f[u] = r[u] ^ 1549556828
    }
    i = C(o.concat(c(t)), 512 + t.length * 8);
    return a(C(f.concat(i), 512 + 128))
}

function C(n, e) {
    var t, o, f, i, h, u = 1732584193, a = -271733879, c = -1732584194, l = 271733878;
    n[e >> 5] |= 128 << e % 32;
    n[(e + 64 >>> 9 << 4) + 14] = e;
    for (t = 0; t < n.length; t += 16) {
        o = u;
        f = a;
        i = c;
        h = l;
        u = s(u, a, c, l, n[t + 0], 7, -680876936);
        l = s(l, u, a, c, n[t + 1], 12, -389564586);
        c = s(c, l, u, a, n[t + 2], 17, 606105819);
        a = s(a, c, l, u, n[t + 3], 22, -1044525330);
        u = s(u, a, c, l, n[t + 4], 7, -176418897);
        l = s(l, u, a, c, n[t + 5], 12, 1200080426);
        c = s(c, l, u, a, n[t + 6], 17, -1473231341);
        a = s(a, c, l, u, n[t + 7], 22, -45705983);
        u = s(u, a, c, l, n[t + 8], 7, 1770035416);
        l = s(l, u, a, c, n[t + 9], 12, -1958414417);
        c = s(c, l, u, a, n[t + 10], 17, -42063);
        a = s(a, c, l, u, n[t + 11], 22, -1990404162);
        u = s(u, a, c, l, n[t + 12], 7, 1804603682);
        l = s(l, u, a, c, n[t + 13], 12, -40341101);
        c = s(c, l, u, a, n[t + 14], 17, -1502002290);
        a = s(a, c, l, u, n[t + 15], 22, 1236535329);
        u = w(u, a, c, l, n[t + 1], 5, -165796510);
        l = w(l, u, a, c, n[t + 6], 9, -1069501632);
        c = w(c, l, u, a, n[t + 11], 14, 643717713);
        a = w(a, c, l, u, n[t + 0], 20, -373897302);
        u = w(u, a, c, l, n[t + 5], 5, -701558691);
        l = w(l, u, a, c, n[t + 10], 9, 38016083);
        c = w(c, l, u, a, n[t + 15], 14, -660478335);
        a = w(a, c, l, u, n[t + 4], 20, -405537848);
        u = w(u, a, c, l, n[t + 9], 5, 568446438);
        l = w(l, u, a, c, n[t + 14], 9, -1019803690);
        c = w(c, l, u, a, n[t + 3], 14, -187363961);
        a = w(a, c, l, u, n[t + 8], 20, 1163531501);
        u = w(u, a, c, l, n[t + 13], 5, -1444681467);
        l = w(l, u, a, c, n[t + 2], 9, -51403784);
        c = w(c, l, u, a, n[t + 7], 14, 1735328473);
        a = w(a, c, l, u, n[t + 12], 20, -1926607734);
        u = F(u, a, c, l, n[t + 5], 4, -378558);
        l = F(l, u, a, c, n[t + 8], 11, -2022574463);
        c = F(c, l, u, a, n[t + 11], 16, 1839030562);
        a = F(a, c, l, u, n[t + 14], 23, -35309556);
        u = F(u, a, c, l, n[t + 1], 4, -1530992060);
        l = F(l, u, a, c, n[t + 4], 11, 1272893353);
        c = F(c, l, u, a, n[t + 7], 16, -155497632);
        a = F(a, c, l, u, n[t + 10], 23, -1094730640);
        u = F(u, a, c, l, n[t + 13], 4, 681279174);
        l = F(l, u, a, c, n[t + 0], 11, -358537222);
        c = F(c, l, u, a, n[t + 3], 16, -722521979);
        a = F(a, c, l, u, n[t + 6], 23, 76029189);
        u = F(u, a, c, l, n[t + 9], 4, -640364487);
        l = F(l, u, a, c, n[t + 12], 11, -421815835);
        c = F(c, l, u, a, n[t + 15], 16, 530742520);
        a = F(a, c, l, u, n[t + 2], 23, -995338651);
        u = E(u, a, c, l, n[t + 0], 6, -198630844);
        l = E(l, u, a, c, n[t + 7], 10, 1126891415);
        c = E(c, l, u, a, n[t + 14], 15, -1416354905);
        a = E(a, c, l, u, n[t + 5], 21, -57434055);
        u = E(u, a, c, l, n[t + 12], 6, 1700485571);
        l = E(l, u, a, c, n[t + 3], 10, -1894986606);
        c = E(c, l, u, a, n[t + 10], 15, -1051523);
        a = E(a, c, l, u, n[t + 1], 21, -2054922799);
        u = E(u, a, c, l, n[t + 8], 6, 1873313359);
        l = E(l, u, a, c, n[t + 15], 10, -30611744);
        c = E(c, l, u, a, n[t + 6], 15, -1560198380);
        a = E(a, c, l, u, n[t + 13], 21, 1309151649);
        u = E(u, a, c, l, n[t + 4], 6, -145523070);
        l = E(l, u, a, c, n[t + 11], 10, -1120210379);
        c = E(c, l, u, a, n[t + 2], 15, 718787259);
        a = E(a, c, l, u, n[t + 9], 21, -343485551);
        u = r(u, o);
        a = r(a, f);
        c = r(c, i);
        l = r(l, h)
    }
    return Array(u, a, c, l)
}

function A(n, e, t, f, i, h) {
    return r(o(r(r(e, n), r(f, h)), i), t)
}

function s(n, e, t, r, o, f, i) {
    return A(e & t | ~e & r, n, e, o, f, i)
}

function w(n, e, t, r, o, f, i) {
    return A(e & r | t & ~r, n, e, o, f, i)
}

function F(n, e, t, r, o, f, i) {
    return A(e ^ t ^ r, n, e, o, f, i)
}

function E(n, e, t, r, o, f, i) {
    return A(t ^ (e | ~r), n, e, o, f, i)
}
"""
ctx = py_mini_racer.MiniRacer()
ctx.eval(hash_code)
token = ctx.call("hex", datetime.now().date().isoformat()).lower()


def stock_a_pb(symbol: str = "sh") -> pd.DataFrame:
    """
    乐咕乐股-A 股市净率
    https://www.legulegu.com/stockdata/market_pb
    :param symbol: choice of {"sh", "sz", "cy", "zx", "000016.XSHG" ...}
    :type symbol: str
    :return: 指定市场的 A 股平均市盈率
    :rtype: pandas.DataFrame
    """
    if symbol in ["000300.XSHG",
                  "000016.XSHG",
                  "000010.XSHG",
                  "000009.XSHG",
                  "000902.XSHG",
                  "000903.XSHG",
                  "000905.XSHG",
                  "000906.XSHG",
                  "000852.XSHG"]:
        url = "https://www.legulegu.com/api/stockdata/market-index-pb/get-data"
        params = {
            "token": token,
            "marketId": symbol
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json)
        temp_df.index = pd.to_datetime(
            temp_df["date"], unit="ms", utc=True).dt.tz_convert("Asia/Shanghai").dt.date
        index_df = temp_df[["equalWeightAveragePB",
                            "middlePB", "weightingAveragePB", "close"]]
        index_df.reset_index(inplace=True)
        return index_df

    url = "https://www.legulegu.com/stockdata/market_pb/getmarket_pb"
    params = {
        "token": token  # token should be get from js decode
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["cySharesPBList"])
    temp_df.index = pd.to_datetime(
        temp_df["date"], unit="ms", utc=True).dt.tz_convert("Asia/Shanghai").dt.date
    cy_df = temp_df[["close", "pb"]]
    cy_df.reset_index(inplace=True)

    temp_df = pd.DataFrame(data_json["shSharesPBList"])
    temp_df.index = pd.to_datetime(
        temp_df["date"], unit="ms", utc=True).dt.tz_convert("Asia/Shanghai").dt.date
    sh_df = temp_df[["close", "pb"]]
    sh_df.reset_index(inplace=True)

    temp_df = pd.DataFrame(data_json["szSharesPBList"])
    temp_df.index = pd.to_datetime(
        temp_df["date"], unit="ms", utc=True).dt.tz_convert("Asia/Shanghai").dt.date
    sz_df = temp_df[["close", "pb"]]
    sz_df.reset_index(inplace=True)

    temp_df = pd.DataFrame(data_json["zxSharesPBList"])
    temp_df.index = pd.to_datetime(
        temp_df["date"], unit="ms", utc=True).dt.tz_convert("Asia/Shanghai").dt.date
    zx_df = temp_df[["close", "pb"]]
    zx_df.reset_index(inplace=True)

    if symbol == "sh":
        return sh_df
    elif symbol == "sz":
        return sz_df
    elif symbol == "cy":
        return cy_df
    elif symbol == "zx":
        return zx_df


if __name__ == '__main__':
    stock_a_pb_df = stock_a_pb(symbol="sh")
    print(stock_a_pb_df)

    stock_a_pb_df = stock_a_pb(symbol="000902.XSHG")
    print(stock_a_pb_df)
