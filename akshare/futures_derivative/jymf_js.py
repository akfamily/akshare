d = """
        function d(e) {
            var t, n = [];
            for (n[(e.length >> 2) - 1] = void 0,
            t = 0; t < n.length; t += 1)
                n[t] = 0;
            var a = 8 * e.length;
            for (t = 0; t < a; t += 8)
                n[t >> 5] |= (255 & e.charCodeAt(t / 8)) << t % 32;
            return n
        }
"""

c = """
        function u(e, t) {
            var n = (65535 & e) + (65535 & t);
            return (e >> 16) + (t >> 16) + (n >> 16) << 16 | 65535 & n
        }
        function s(e, t, n, a, i, o) {
            return u(function(e, t) {
                return e << t | e >>> 32 - t
            }(u(u(t, e), u(a, o)), i), n)
        }
        function f(e, t, n, a, i, o, r) {
            return s(t & n | ~t & a, e, t, i, o, r)
        }
        function h(e, t, n, a, i, o, r) {
            return s(t & a | n & ~a, e, t, i, o, r)
        }
        function p(e, t, n, a, i, o, r) {
            return s(t ^ n ^ a, e, t, i, o, r)
        }
        function m(e, t, n, a, i, o, r) {
            return s(n ^ (t | ~a), e, t, i, o, r)
        }
        function c(e, t) {
            var n, a, i, o, r;
            e[t >> 5] |= 128 << t % 32,
            e[14 + (t + 64 >>> 9 << 4)] = t;
            var s = 1732584193
              , c = -271733879
              , l = -1732584194
              , d = 271733878;
            for (n = 0; n < e.length; n += 16)
                c = m(c = m(c = m(c = m(c = p(c = p(c = p(c = p(c = h(c = h(c = h(c = h(c = f(c = f(c = f(c = f(i = c, l = f(o = l, d = f(r = d, s = f(a = s, c, l, d, e[n], 7, -680876936), c, l, e[n + 1], 12, -389564586), s, c, e[n + 2], 17, 606105819), d, s, e[n + 3], 22, -1044525330), l = f(l, d = f(d, s = f(s, c, l, d, e[n + 4], 7, -176418897), c, l, e[n + 5], 12, 1200080426), s, c, e[n + 6], 17, -1473231341), d, s, e[n + 7], 22, -45705983), l = f(l, d = f(d, s = f(s, c, l, d, e[n + 8], 7, 1770035416), c, l, e[n + 9], 12, -1958414417), s, c, e[n + 10], 17, -42063), d, s, e[n + 11], 22, -1990404162), l = f(l, d = f(d, s = f(s, c, l, d, e[n + 12], 7, 1804603682), c, l, e[n + 13], 12, -40341101), s, c, e[n + 14], 17, -1502002290), d, s, e[n + 15], 22, 1236535329), l = h(l, d = h(d, s = h(s, c, l, d, e[n + 1], 5, -165796510), c, l, e[n + 6], 9, -1069501632), s, c, e[n + 11], 14, 643717713), d, s, e[n], 20, -373897302), l = h(l, d = h(d, s = h(s, c, l, d, e[n + 5], 5, -701558691), c, l, e[n + 10], 9, 38016083), s, c, e[n + 15], 14, -660478335), d, s, e[n + 4], 20, -405537848), l = h(l, d = h(d, s = h(s, c, l, d, e[n + 9], 5, 568446438), c, l, e[n + 14], 9, -1019803690), s, c, e[n + 3], 14, -187363961), d, s, e[n + 8], 20, 1163531501), l = h(l, d = h(d, s = h(s, c, l, d, e[n + 13], 5, -1444681467), c, l, e[n + 2], 9, -51403784), s, c, e[n + 7], 14, 1735328473), d, s, e[n + 12], 20, -1926607734), l = p(l, d = p(d, s = p(s, c, l, d, e[n + 5], 4, -378558), c, l, e[n + 8], 11, -2022574463), s, c, e[n + 11], 16, 1839030562), d, s, e[n + 14], 23, -35309556), l = p(l, d = p(d, s = p(s, c, l, d, e[n + 1], 4, -1530992060), c, l, e[n + 4], 11, 1272893353), s, c, e[n + 7], 16, -155497632), d, s, e[n + 10], 23, -1094730640), l = p(l, d = p(d, s = p(s, c, l, d, e[n + 13], 4, 681279174), c, l, e[n], 11, -358537222), s, c, e[n + 3], 16, -722521979), d, s, e[n + 6], 23, 76029189), l = p(l, d = p(d, s = p(s, c, l, d, e[n + 9], 4, -640364487), c, l, e[n + 12], 11, -421815835), s, c, e[n + 15], 16, 530742520), d, s, e[n + 2], 23, -995338651), l = m(l, d = m(d, s = m(s, c, l, d, e[n], 6, -198630844), c, l, e[n + 7], 10, 1126891415), s, c, e[n + 14], 15, -1416354905), d, s, e[n + 5], 21, -57434055), l = m(l, d = m(d, s = m(s, c, l, d, e[n + 12], 6, 1700485571), c, l, e[n + 3], 10, -1894986606), s, c, e[n + 10], 15, -1051523), d, s, e[n + 1], 21, -2054922799), l = m(l, d = m(d, s = m(s, c, l, d, e[n + 8], 6, 1873313359), c, l, e[n + 15], 10, -30611744), s, c, e[n + 6], 15, -1560198380), d, s, e[n + 13], 21, 1309151649), l = m(l, d = m(d, s = m(s, c, l, d, e[n + 4], 6, -145523070), c, l, e[n + 11], 10, -1120210379), s, c, e[n + 2], 15, 718787259), d, s, e[n + 9], 21, -343485551),
                s = u(s, a),
                c = u(c, i),
                l = u(l, o),
                d = u(d, r);
            return [s, c, l, d]
        }
        function l(e) {
            var t, n = "", a = 32 * e.length;
            for (t = 0; t < a; t += 8)
                n += String.fromCharCode(e[t >> 5] >>> t % 32 & 255);
            return n
        }
        function d(e) {
            var t, n = [];
            for (n[(e.length >> 2) - 1] = void 0,
            t = 0; t < n.length; t += 1)
                n[t] = 0;
            var a = 8 * e.length;
            for (t = 0; t < a; t += 8)
                n[t >> 5] |= (255 & e.charCodeAt(t / 8)) << t % 32;
            return n
        }
        function a(e) {
            var t, n, a = "0123456789abcdef", i = "";
            for (n = 0; n < e.length; n += 1)
                t = e.charCodeAt(n),
                i += a.charAt(t >>> 4 & 15) + a.charAt(15 & t);
            return i
        }
        function n(e) {
            return unescape(encodeURIComponent(e))
        }
        function i(e) {
            return function(e) {
                return l(c(d(e), 8 * e.length))
            }(n(e))
        }
        function o(e, t) {
            return function(e, t) {
                var n, a, i = d(e), o = [], r = [];
                for (o[15] = r[15] = void 0,
                16 < i.length && (i = c(i, 8 * e.length)),
                n = 0; n < 16; n += 1)
                    o[n] = 909522486 ^ i[n],
                    r[n] = 1549556828 ^ i[n];
                return a = c(o.concat(d(t)), 512 + 8 * t.length),
                l(c(r.concat(a), 640))
            }(n(e), n(t))
        }
        function e(e, t, n) {
            return t ? n ? o(t, e) : function(e, t) {
                return a(o(e, t))
            }(t, e) : n ? i(e) : function(e) {
                return a(i(e))
            }(e)
        }
"""