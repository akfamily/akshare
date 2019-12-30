# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/30 21:02
contact: jindaxiang@163.com
desc: 
"""
stock_em_sy_js = """
    function getCode(num) {
            var str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
            var codes = str.split('');
            num = num || 6;
            var code = "";
            for (var i = 0; i < num; i++) {
                code += codes[Math.floor(Math.random() * 52)]
            }
            return code
        }
    """
