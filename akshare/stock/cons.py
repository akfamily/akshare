# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/10/25 15:56
Desc: 股票配置文件
"""
# zh-sina-kcb
zh_sina_kcb_stock_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
zh_sina_kcb_stock_payload = {
    "page": "1",
    "num": "80",
    "sort": "symbol",
    "asc": "1",
    "node": "kcb",
    "symbol": "",
    "_s_r_a": "auto"
}
zh_sina_kcb_stock_count_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=kcb"
zh_sina_kcb_stock_hist_url = "https://quotes.sina.cn/cn/api/jsonp.php/var%20_{}{}=/KC_MarketDataService.getKLineData?symbol={}"
zh_sina_kcb_stock_amount_url = "https://stock.finance.sina.com.cn/stock/api/jsonp.php/var%20KKE_ShareAmount_{}=/StockService.getAmountBySymbol?_=20&symbol={}"
zh_sina_kcb_stock_hfq_url = "https://finance.sina.com.cn/realstock/company/{}/hfq.js"
zh_sina_kcb_stock_qfq_url = "https://finance.sina.com.cn/realstock/company/{}/qfq.js"

# zh-sina-a
zh_sina_a_stock_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
zh_sina_a_stock_payload = {
    "page": "1",
    "num": "80",
    "sort": "symbol",
    "asc": "1",
    "node": "hs_a",
    "symbol": "",
    "_s_r_a": "init"
}
zh_sina_a_stock_count_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=hs_a"
zh_sina_a_stock_hist_url = "https://finance.sina.com.cn/realstock/company/{}/hisdata/klc_kl.js"
zh_sina_a_stock_amount_url = "https://stock.finance.sina.com.cn/stock/api/jsonp.php/var%20KKE_ShareAmount_{}=/StockService.getAmountBySymbol?_=20&symbol={}"
zh_sina_a_stock_hfq_url = "https://finance.sina.com.cn/realstock/company/{}/hfq.js"
zh_sina_a_stock_qfq_url = "https://finance.sina.com.cn/realstock/company/{}/qfq.js"

# us-sina
us_sina_stock_hist_qfq_url = "https://finance.sina.com.cn/us_stock/company/reinstatement/{}_qfq.js"
us_sina_stock_hist_url = "https://finance.sina.com.cn/us_stock/company/hisdata/klc_kl_{}.js"
us_sina_stock_list_url = "http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList[{}]/US_CategoryService.getList"
us_sina_stock_dict_payload = {
    "page": "2",
    "num": "20",
    "sort": "",
    "asc": "0",
    "market": "",
    "id": ""
}
js_hash_text = """
    function d(s){
		var a, i, j, c, c0, c1, c2, r;
		var _s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_$';
		var _r64 = function(s, b)
		{
			return ((s | (s << 6)) >>> (b % 6)) & 63;
		};
		a = [];
		c = [];
		for (i = 0; i < s.length; i++)
		{
			c0 = s.charCodeAt(i);
			if (c0 & ~255)
			{
				c0 = (c0 >> 8) ^ c0;
			}
			c.push(c0);
			if (c.length == 3 || i == s.length - 1)
			{
				while(c.length < 3)
				{
					c.push(0);
				}
				a.push((c[0] >> 2) & 63);
				a.push(((c[1] >> 4) | (c[0] << 6)) & 63);
				a.push(((c[1] << 4) | (c[2] >> 2)) & 63);
				a.push(c[2] & 63);
				c = [];
			}
		}
		while (a.length < 16)
		{
			a.push(0);
		}
		r = 0;
		for (i = 0; i < a.length; i++)
		{
			r ^= (_r64(a[i] ^ (r | i), i) ^ _r64(i, r)) & 63;
		}
		for (i = 0; i < a.length; i++)
		{
			a[i] = (_r64((r | i & a[i]), r) ^ a[i]) & 63;
			r += a[i];
		}
		for (i = 16; i < a.length; i++)
		{
			a[i % 16] ^= (a[i] + (i >>> 4)) & 63;
		}
		for (i = 0; i < 16; i++)
		{
			a[i] = _s.substr(a[i], 1);
		}
		a = a.slice(0, 16).join('');
		return a;
	}
"""
# hk-sina
hk_sina_stock_hist_hfq_url = "https://finance.sina.com.cn/stock/hkstock/{}/hfq.js"
hk_sina_stock_hist_qfq_url = "https://finance.sina.com.cn/stock/hkstock/{}/qfq.js"
hk_sina_stock_hist_url = "https://finance.sina.com.cn/stock/hkstock/{}/klc_kl.js"
hk_sina_stock_list_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHKStockData"

hk_sina_stock_dict_payload = {
    "page": "1",
    "num": "3000",
    "sort": "symbol",
    "asc": "1",
    "node": "qbgg_hk",
    "_s_r_a": "page"
}

# hk-tx
hk_url = "http://stock.gtimg.cn/data/hk_rank.php"
hk_headers = {
    "Referer": "http://stockapp.finance.qq.com/mstats/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}
hk_payload = {
    "board": "A_H",
    "metric": "price",
    "pageSize": "20",
    "reqPage": "1",
    "order": "decs",
    "var_name": "list_data"
}

hk_stock_url = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get"
hk_stock_headers = {
    # "Referer": "http://gu.qq.com/hk00168/gp",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}
hk_stock_payload = {
    "_var": "kline_dayhfq{}",
    "param": "hk{},day,{}-01-01,{}-12-31,640,hfq",
    "r": ""
}

# usa
url_usa_daily = "http://webusstock.hermes.hexun.com/usa/kline"
payload_usa_daily = {
    "code": "NASDAQNTES",
    "start": "20191026213000",
    "number": "-1000",
    "type": "5"
}

# usa
url_usa = "http://quote.hexun.com/usastock/data/getdjstock.aspx"

payload_usa = {
    "type": "1",
    "market": "3",
    "sorttype": "4",
    "updown": "up",
    "page": "1",
    'count': "200",
    "time": "203450"
}

headers_usa = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "quote.hexun.com",
    "Pragma": "no-cache",
    "Referer": "http://quote.hexun.com/usastock/xqstock.aspx?market=3",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}

# china
hx_url = "http://stockdata.stock.hexun.com/zrbg/data/zrbList.aspx"

hx_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "ADVC=371c0a2afd9a7b; UM_distinctid=16a24d29c4f142-0f969e46eea4c7-e323069-1fa400-16a24d29c50aa5; HexunTrack=SID=20190416142542146f54a3710276640a88fea687ad6a7bcb0&CITY=51&TOWN=510100; vjuids=11fcc219b5.16a820267e4.0.cc0391a93be56; vjlast=1556959357.1556959357.30; __utma=194262068.1423418741.1558975446.1558975446.1558975446.1; __utmz=194262068.1558975446.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ASL=18179,anzqo,7ca108c3ded485387ca108c27ca108b97ca108ef; cn_1263247791_dplus=%7B%22distinct_id%22%3A%20%2216a24d29c4f142-0f969e46eea4c7-e323069-1fa400-16a24d29c50aa5%22%2C%22userFirstDate%22%3A%20%2220190504%22%2C%22userID%22%3A%20%22%22%2C%22userName%22%3A%20%22%22%2C%22userType%22%3A%20%22nologinuser%22%2C%22userLoginDate%22%3A%20%2220191010%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201570727325%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201570727325%2C%22initial_view_time%22%3A%20%221556958609%22%2C%22initial_referrer%22%3A%20%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DJmHPP1QGABcJs0kzrvZREqHK_nobidR7d7YPCQF75loa5N33Au5q_xFu8y9VPlvl8O6I7b1LmRuhIiccTnFW-_%26wd%3D%26eqid%3Db55837ee0001a310000000025ccd4f55%22%2C%22initial_referrer_domain%22%3A%20%22www.baidu.com%22%2C%22%24recent_outside_referrer%22%3A%20%22www.baidu.com%22%7D; hxck_webdev1_general=bondjlvcookie_list=019124_11%e5%9b%bd%e5%80%ba24_1&npFutjlvcookie_list=czcers1409|WT1009; appToken=pc%2Cother%2Cchrome%2ChxAppSignId96253760252191461570688954189%2CHXGG20190415; __jsluid_h=08f65cba22ad34dc3fd095b5b986c8a4",
    "Host": "stockdata.stock.hexun.com",
    "Pragma": "no-cache",
    "Referer": "http://stockdata.stock.hexun.com/zrbg/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}

hx_params = {
    "date": "2018-12-31",
    "count": "20",
    "pname": "20",
    "titType": "null",
    "page": "8",
    "callback": "hxbase_json11571989979887",
}

hk_js_decode = """
function d(t) {
    var e, i, n, r, a, o, s, l = (arguments,
            864e5), u = 7657, c = [], h = [], d = ~(3 << 30), f = 1 << 30,
        p = [0, 3, 5, 6, 9, 10, 12, 15, 17, 18, 20, 23, 24, 27, 29, 30], m = Math, g = function () {
            var l, u;
            for (l = 0; 64 > l; l++)
                h[l] = m.pow(2, l),
                26 > l && (c[l] = v(l + 65),
                    c[l + 26] = v(l + 97),
                10 > l && (c[l + 52] = v(l + 48)));
            for (c.push("+", "/"),
                     c = c.join(""),
                     i = t.split(""),
                     n = i.length,
                     l = 0; n > l; l++)
                i[l] = c.indexOf(i[l]);
            return r = {},
                e = o = 0,
                a = {},
                u = w([12, 6]),
                s = 63 ^ u[1],
            {
                _1479: T,
                _136: _,
                _200: S,
                _139: k,
                _197: _mi_run
            }["_" + u[0]] || function () {
                return []
            }
        }, v = String.fromCharCode, b = function (t) {
            return t === {}._
        }, N = function () {
            var t, e;
            for (t = y(),
                     e = 1; ;) {
                if (!y())
                    return e * (2 * t - 1);
                e++
            }
        }, y = function () {
            var t;
            return e >= n ? 0 : (t = i[e] & 1 << o,
                o++,
            o >= 6 && (o -= 6,
                e++),
                !!t)
        }, w = function (t, r, a) {
            var s, l, u, c, d;
            for (l = [],
                     u = 0,
                 r || (r = []),
                 a || (a = []),
                     s = 0; s < t.length; s++)
                if (c = t[s],
                    u = 0,
                    c) {
                    if (e >= n)
                        return l;
                    if (t[s] <= 0)
                        u = 0;
                    else if (t[s] <= 30) {
                        for (; d = 6 - o,
                                   d = c > d ? d : c,
                                   u |= (i[e] >> o & (1 << d) - 1) << t[s] - c,
                                   o += d,
                               o >= 6 && (o -= 6,
                                   e++),
                                   c -= d,
                                   !(0 >= c);)
                            ;
                        r[s] && u >= h[t[s] - 1] && (u -= h[t[s]])
                    } else
                        u = w([30, t[s] - 30], [0, r[s]]),
                        a[s] || (u = u[0] + u[1] * h[30]);
                    l[s] = u
                } else
                    l[s] = 0;
            return l
        }, x = function (t) {
            var e, i, n;
            for (t > 1 && (e = 0),
                     e = 0; t > e; e++)
                r.d++,
                    n = r.d % 7,
                (3 == n || 4 == n) && (r.d += 5 - n);
            return i = new Date,
                i.setTime((u + r.d) * l),
                i
        }, S = function () {
            var t, i, a, o, l;
            if (s >= 1)
                return [];
            for (r.d = w([18], [1])[0] - 1,
                     a = w([3, 3, 30, 6]),
                     r.p = a[0],
                     r.ld = a[1],
                     r.cd = a[2],
                     r.c = a[3],
                     r.m = m.pow(10, r.p),
                     r.pc = r.cd / r.m,
                     i = [],
                     t = 0; o = {
                d: 1
            },
                 y() && (a = w([3])[0],
                     0 == a ? o.d = w([6])[0] : 1 == a ? (r.d = w([18])[0],
                         o.d = 0) : o.d = a),
                     l = {
                         day: x(o.d)
                     },
                 y() && (r.ld += N()),
                     a = w([3 * r.ld], [1]),
                     r.cd += a[0],
                     l.close = r.cd / r.m,
                     i.push(l),
                 !(e >= n) && (e != n - 1 || 63 & (r.c ^ t + 1)); t++)
                ;
            return i[0].prevclose = r.pc,
                i
        }, _ = function () {
            var t, i, a, o, l, u, c, h, d, f, p;
            if (s > 2)
                return [];
            for (c = [],
                     d = {
                         v: "volume",
                         p: "price",
                         a: "avg_price"
                     },
                     r.d = w([18], [1])[0] - 1,
                     h = {
                         day: x(1)
                     },
                     a = w(1 > s ? [3, 3, 4, 1, 1, 1, 5] : [4, 4, 4, 1, 1, 1, 3]),
                     t = 0; 7 > t; t++)
                r[["la", "lp", "lv", "tv", "rv", "zv", "pp"][t]] = a[t];
            for (r.m = m.pow(10, r.pp),
                     s >= 1 ? (a = w([3, 3]),
                         r.c = a[0],
                         a = a[1]) : (a = 5,
                         r.c = 2),
                     r.pc = w([6 * a])[0],
                     h.pc = r.pc / r.m,
                     r.cp = r.pc,
                     r.da = 0,
                     r.sa = r.sv = 0,
                     t = 0; !(e >= n) && (e != n - 1 || 7 & (r.c ^ t)); t++) {
                for (l = {},
                         o = {},
                         f = r.tv ? y() : 1,
                         i = 0; 3 > i; i++)
                    if (p = ["v", "p", "a"][i],
                    (f ? y() : 0) && (a = N(),
                        r["l" + p] += a),
                        u = "v" == p && r.rv ? y() : 1,
                        a = w([3 * r["l" + p] + ("v" == p ? 7 * u : 0)], [!!i])[0] * (u ? 1 : 100),
                        o[p] = a,
                    "v" == p) {
                        if (!(l[d[p]] = a) && (s > 1 || 241 > t) && (r.zv ? !y() : 1)) {
                            o.p = 0;
                            break
                        }
                    } else
                        "a" == p && (r.da = (1 > s ? 0 : r.da) + o.a);
                r.sv += o.v,
                    l[d.p] = (r.cp += o.p) / r.m,
                    r.sa += o.v * r.cp,
                    l[d.a] = b(o.a) ? t ? c[t - 1][d.a] : l[d.p] : r.sv ? ((m.floor((r.sa * (2e3 / r.m) + r.sv) / r.sv) >> 1) + r.da) / 1e3 : l[d.p] + r.da / 1e3,
                    c.push(l)
            }
            return c[0].date = h.day,
                c[0].prevclose = h.pc,
                c
        }, T = function () {
            var t, e, i, n, a, o, l;
            if (s >= 1)
                return [];
            for (r.lv = 0,
                     r.ld = 0,
                     r.cd = 0,
                     r.cv = [0, 0],
                     r.p = w([6])[0],
                     r.d = w([18], [1])[0] - 1,
                     r.m = m.pow(10, r.p),
                     a = w([3, 3]),
                     r.md = a[0],
                     r.mv = a[1],
                     t = []; a = w([6]),
                     a.length;) {
                if (i = {
                    c: a[0]
                },
                    n = {},
                    i.d = 1,
                32 & i.c)
                    for (; ;) {
                        if (a = w([6])[0],
                        63 == (16 | a)) {
                            l = 16 & a ? "x" : "u",
                                a = w([3, 3]),
                                i[l + "_d"] = a[0] + r.md,
                                i[l + "_v"] = a[1] + r.mv;
                            break
                        }
                        if (32 & a) {
                            o = 8 & a ? "d" : "v",
                                l = 16 & a ? "x" : "u",
                                i[l + "_" + o] = (7 & a) + r["m" + o];
                            break
                        }
                        if (o = 15 & a,
                            0 == o ? i.d = w([6])[0] : 1 == o ? (r.d = o = w([18])[0],
                                i.d = 0) : i.d = o,
                            !(16 & a))
                            break
                    }
                n.date = x(i.d);
                for (o in {
                    v: 0,
                    d: 0
                })
                    b(i["x_" + o]) || (r["l" + o] = i["x_" + o]),
                    b(i["u_" + o]) && (i["u_" + o] = r["l" + o]);
                for (i.l_l = [i.u_d, i.u_d, i.u_d, i.u_d, i.u_v],
                         l = p[15 & i.c],
                     1 & i.u_v && (l = 31 - l),
                     16 & i.c && (i.l_l[4] += 2),
                         e = 0; 5 > e; e++)
                    l & 1 << 4 - e && i.l_l[e]++,
                        i.l_l[e] *= 3;
                i.d_v = w(i.l_l, [1, 0, 0, 1, 1], [0, 0, 0, 0, 1]),
                    o = r.cd + i.d_v[0],
                    n.open = o / r.m,
                    n.high = (o + i.d_v[1]) / r.m,
                    n.low = (o - i.d_v[2]) / r.m,
                    n.close = (o + i.d_v[3]) / r.m,
                    a = i.d_v[4],
                "number" == typeof a && (a = [a, a >= 0 ? 0 : -1]),
                    r.cd = o + i.d_v[3],
                    l = r.cv[0] + a[0],
                    r.cv = [l & d, r.cv[1] + a[1] + !!((r.cv[0] & d) + (a[0] & d) & f)],
                    n.volume = (r.cv[0] & f - 1) + r.cv[1] * f,
                    t.push(n)
            }
            return t
        }, k = function () {
            var t, e, i, n;
            if (s > 1)
                return [];
            for (r.l = 0,
                     n = -1,
                     r.d = w([18])[0] - 1,
                     i = w([18])[0]; r.d < i;)
                e = x(1),
                    0 >= n ? (y() && (r.l += N()),
                        n = w([3 * r.l], [0])[0] + 1,
                    t || (t = [e],
                        n--)) : t.push(e),
                    n--;
            return t
        };
    return _mi_run = function () {
        var t, i, a, o;
        if (s >= 1)
            return [];
        for (r.f = w([6])[0],
                 r.c = w([6])[0],
                 a = [],
                 r.dv = [],
                 r.dl = [],
                 t = 0; t < r.f; t++)
            r.dv[t] = 0,
                r.dl[t] = 0;
        for (t = 0; !(e >= n) && (e != n - 1 || 7 & (r.c ^ t)); t++) {
            for (o = [],
                     i = 0; i < r.f; i++)
                y() && (r.dl[i] += N()),
                    r.dv[i] += w([3 * r.dl[i]], [1])[0],
                    o[i] = r.dv[i];
            a.push(o)
        }
        return a
    }
        ,
        g()()
}
"""
