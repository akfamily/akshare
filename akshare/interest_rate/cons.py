#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2020/4/29 19:51
Desc: 东方财富网-经济数据-银行间拆借利率-配置文件
上海银行同业拆借市场
上海银行同业拆借市场-Shibor人民币
隔夜: http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99221&cu=cny&type=009016&p=2
1周: http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99222&cu=cny&type=009017&p=2
2周: http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99223&cu=cny&type=009018&p=2
1月: http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99224&cu=cny&type=009019&p=2
3月: http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99225&cu=cny&type=009020&p=2
6月: http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99226&cu=cny&type=009021&p=2
9月: http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99227&cu=cny&type=009022&p=2
1年: http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99228&cu=cny&type=009023&p=2

中国银行同业拆借市场
中国银行同业拆借市场-Chibor人民币
隔夜: http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99231&cu=cny&type=009086
1周: http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99232&cu=cny&type=009087
2周: http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99233&cu=cny&type=009088
3周: http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99234&cu=cny&type=009089
1月: http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99235&cu=cny&type=009090
2月: http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99236&cu=cny&type=009091
3月: http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99237&cu=cny&type=009092
4月: http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99238&cu=cny&type=009093
6月: http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99239&cu=cny&type=009094
9月: http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=992310&cu=cny&type=009095
1年: http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=992311&cu=cny&type=009096

伦敦银行同业拆借市场
伦敦银行同业拆借市场-Libor英镑
隔夜: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=97&d=99241&cu=gbp&type=009001
1周: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=97&d=99242&cu=gbp&type=009002
1月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=97&d=99243&cu=gbp&type=009004
2月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=97&d=99244&cu=gbp&type=009005
3月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=97&d=99245&cu=gbp&type=009006
8月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=97&d=99246&cu=gbp&type=009011
伦敦银行同业拆借市场-Libor美元
隔夜: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=96&d=99251&cu=usd&type=009001
1周: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=96&d=99252&cu=usd&type=009002
1月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=96&d=99253&cu=usd&type=009004
2月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=96&d=99254&cu=usd&type=009005
3月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=96&d=99255&cu=usd&type=009006
8月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=96&d=99256&cu=usd&type=009011
伦敦银行同业拆借市场-Libor欧元
隔夜: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=95&d=99261&cu=eur&type=009001
1周: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=95&d=99262&cu=eur&type=009002
1月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=95&d=99263&cu=eur&type=009004
2月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=95&d=99264&cu=eur&type=009005
3月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=95&d=99265&cu=eur&type=009006
8月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=95&d=99266&cu=eur&type=009011
伦敦银行同业拆借市场-Libor日元
隔夜: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=94&d=99271&cu=jpy&type=009001
1周: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=94&d=99272&cu=jpy&type=009002
1月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=94&d=99273&cu=jpy&type=009004
2月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=94&d=99274&cu=jpy&type=009005
3月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=94&d=99275&cu=jpy&type=009006
8月: http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=94&d=99276&cu=jpy&type=009011

欧洲银行同业拆借市场
欧洲银行同业拆借市场-Euribor欧元
1周: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99281&cu=eur&type=009070
2周: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99282&cu=eur&type=009071
3周: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99283&cu=eur&type=009072
1月: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99284&cu=eur&type=009073
2月: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99285&cu=eur&type=009074
3月: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99286&cu=eur&type=009075
4月: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99287&cu=eur&type=009076
5月: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99288&cu=eur&type=009077
6月: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99289&cu=eur&type=009078
7月: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=992810&cu=eur&type=009079
8月: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=992811&cu=eur&type=009080
9月: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=992812&cu=eur&type=009081
10月: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=992813&cu=eur&type=009082
11月: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=992814&cu=eur&type=009083
1年: http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=992815&cu=eur&type=009084

香港银行同业拆借市场
香港银行同业拆借市场-Hibor港元
隔夜: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99301&cu=hkd&type=009048
1周: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99302&cu=hkd&type=009049
2周: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99303&cu=hkd&type=009050
1月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99304&cu=hkd&type=009051
2月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99305&cu=hkd&type=009052
3月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99306&cu=hkd&type=009053
4月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99307&cu=hkd&type=009054
5月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99308&cu=hkd&type=009055
6月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99309&cu=hkd&type=009056
7月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=993010&cu=hkd&type=009057
8月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=993011&cu=hkd&type=009058
9月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=993012&cu=hkd&type=009059
10月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=993013&cu=hkd&type=009060
11月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=993014&cu=hkd&type=009061
1年: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=993015&cu=hkd&type=009062
香港银行同业拆借市场-Hibor美元
隔夜: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99311&cu=usd&type=009048
1周: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99312&cu=usd&type=009049
2周: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99313&cu=usd&type=009050
1月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99314&cu=usd&type=009051
2月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99315&cu=usd&type=009052
3月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99316&cu=usd&type=009053
4月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99317&cu=usd&type=009054
5月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99318&cu=usd&type=009055
6月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99319&cu=usd&type=009056
7月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=993110&cu=usd&type=009057
8月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=993111&cu=usd&type=009058
9月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=993112&cu=usd&type=009059
10月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=993113&cu=usd&type=009060
11月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=993114&cu=usd&type=009061
1年: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=993115&cu=usd&type=009062
香港银行同业拆借市场-Hibor人民币
隔夜: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99321&cu=cny&type=009048
1周: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99322&cu=cny&type=009049
2周: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99323&cu=cny&type=009050
1月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99324&cu=cny&type=009051
2月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99325&cu=cny&type=009052
3月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99326&cu=cny&type=009053
6月: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99327&cu=cny&type=009056
1年: http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99328&cu=cny&type=009062

新加坡银行同业拆借市场
新加坡银行同业拆借市场-Sibor星元
1月: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99331&cu=sgd&type=009063
2月: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99332&cu=sgd&type=009064
3月: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99333&cu=sgd&type=009065
6月: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99334&cu=sgd&type=009066
9月: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99335&cu=sgd&type=009067
1年: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99336&cu=sgd&type=009068
新加坡银行同业拆借市场-Sibor美元
1月: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=87&d=99341&cu=usd&type=009063
2月: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=87&d=99342&cu=usd&type=009064
3月: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=87&d=99343&cu=usd&type=009065
6月: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=87&d=99344&cu=usd&type=009066
9月: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=87&d=99345&cu=usd&type=009067
1年: http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=87&d=99346&cu=usd&type=009068
"""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}

market_symbol_indicator_dict = {
    "上海银行同业拆借市场": {"Shibor人民币": {
        "隔夜": "http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99221&cu=cny&type=009016",
        "1周": "http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99222&cu=cny&type=009017",
        "2周": "http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99223&cu=cny&type=009018",
        "1月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99224&cu=cny&type=009019",
        "3月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99225&cu=cny&type=009020",
        "6月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99226&cu=cny&type=009021",
        "9月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99227&cu=cny&type=009022",
        "1年": "http://data.eastmoney.com/shibor/shibor.aspx?m=sh&t=99&d=99228&cu=cny&type=009023",
    }},

    "中国银行同业拆借市场": {"Chibor人民币": {
        "隔夜": "http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99231&cu=cny&type=009086",
        "1周": "http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99232&cu=cny&type=009087",
        "2周": "http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99233&cu=cny&type=009088",
        "3周": "http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99234&cu=cny&type=009089",
        "1月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99235&cu=cny&type=009090",
        "2月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99236&cu=cny&type=009091",
        "3月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99237&cu=cny&type=009092",
        "4月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99238&cu=cny&type=009093",
        "6月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=99239&cu=cny&type=009094",
        "9月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=992310&cu=cny&type=009095",
        "1年": "http://data.eastmoney.com/shibor/shibor.aspx?m=ch&t=98&d=992311&cu=cny&type=009096",
    }},

    "伦敦银行同业拆借市场": {"Libor英镑": {
        "隔夜": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=97&d=99241&cu=gbp&type=009001",
        "1周": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=97&d=99242&cu=gbp&type=009002",
        "1月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=97&d=99243&cu=gbp&type=009004",
        "2月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=97&d=99244&cu=gbp&type=009005",
        "3月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=97&d=99245&cu=gbp&type=009006",
        "8月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=97&d=99246&cu=gbp&type=009011",
    },
        "Libor美元": {
            "隔夜": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=96&d=99251&cu=usd&type=009001",
            "1周": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=96&d=99252&cu=usd&type=009002",
            "1月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=96&d=99253&cu=usd&type=009004",
            "2月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=96&d=99254&cu=usd&type=009005",
            "3月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=96&d=99255&cu=usd&type=009006",
            "8月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=96&d=99256&cu=usd&type=009011",
        },
        "Libor欧元": {
            "隔夜": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=95&d=99261&cu=eur&type=009001",
            "1周": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=95&d=99262&cu=eur&type=009002",
            "1月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=95&d=99263&cu=eur&type=009004",
            "2月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=95&d=99264&cu=eur&type=009005",
            "3月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=95&d=99265&cu=eur&type=009006",
            "8月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=95&d=99266&cu=eur&type=009011",
        },
        "Libor日元": {
            "隔夜": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=94&d=99271&cu=jpy&type=009001",
            "1周": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=94&d=99272&cu=jpy&type=009002",
            "1月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=94&d=99273&cu=jpy&type=009004",
            "2月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=94&d=99274&cu=jpy&type=009005",
            "3月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=94&d=99275&cu=jpy&type=009006",
            "8月": "http://data.eastmoney.com/shibor/shibor.aspx?m=ld&t=94&d=99276&cu=jpy&type=009011",
        }},
    "欧洲银行同业拆借市场": {"Euribor欧元": {
        "1周": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99281&cu=eur&type=009070",
        "2周": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99282&cu=eur&type=009071",
        "3周": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99283&cu=eur&type=009072",
        "1月": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99284&cu=eur&type=009073",
        "2月": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99285&cu=eur&type=009074",
        "3月": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99286&cu=eur&type=009075",
        "4月": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99287&cu=eur&type=009076",
        "5月": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99288&cu=eur&type=009077",
        "6月": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=99289&cu=eur&type=009078",
        "7月": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=992810&cu=eur&type=009079",
        "8月": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=992811&cu=eur&type=009080",
        "9月": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=992812&cu=eur&type=009081",
        "10月": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=992813&cu=eur&type=009082",
        "11月": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=992814&cu=eur&type=009083",
        "1年": "http://data.eastmoney.com/shibor/shibor.aspx?m=eu&t=93&d=992815&cu=eur&type=009084",
    }},
    "香港银行同业拆借市场": {"Hibor港元": {
        "隔夜": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99301&cu=hkd&type=009048",
        "1周": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99302&cu=hkd&type=009049",
        "2周": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99303&cu=hkd&type=009050",
        "1月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99304&cu=hkd&type=009051",
        "2月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99305&cu=hkd&type=009052",
        "3月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99306&cu=hkd&type=009053",
        "4月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99307&cu=hkd&type=009054",
        "5月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99308&cu=hkd&type=009055",
        "6月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=99309&cu=hkd&type=009056",
        "7月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=993010&cu=hkd&type=009057",
        "8月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=993011&cu=hkd&type=009058",
        "9月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=993012&cu=hkd&type=009059",
        "10月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=993013&cu=hkd&type=009060",
        "11月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=993014&cu=hkd&type=009061",
        "1年": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=91&d=993015&cu=hkd&type=009062",
    },
        "Hibor美元": {
            "隔夜": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99311&cu=usd&type=009048",
            "1周": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99312&cu=usd&type=009049",
            "2周": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99313&cu=usd&type=009050",
            "1月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99314&cu=usd&type=009051",
            "2月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99315&cu=usd&type=009052",
            "3月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99316&cu=usd&type=009053",
            "4月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99317&cu=usd&type=009054",
            "5月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99318&cu=usd&type=009055",
            "6月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=99319&cu=usd&type=009056",
            "7月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=993110&cu=usd&type=009057",
            "8月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=993111&cu=usd&type=009058",
            "9月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=993112&cu=usd&type=009059",
            "10月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=993113&cu=usd&type=009060",
            "11月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=993114&cu=usd&type=009061",
            "1年": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=90&d=993115&cu=usd&type=009062",
        },
        "Hibor人民币": {
            "隔夜": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99321&cu=cny&type=009048",
            "1周": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99322&cu=cny&type=009049",
            "2周": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99323&cu=cny&type=009050",
            "1月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99324&cu=cny&type=009051",
            "2月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99325&cu=cny&type=009052",
            "3月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99326&cu=cny&type=009053",
            "6月": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99327&cu=cny&type=009056",
            "1年": "http://data.eastmoney.com/shibor/shibor.aspx?m=hk&t=89&d=99328&cu=cny&type=009062",
        }},
    "新加坡银行同业拆借市场": {"Sibor星元": {
        "1月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99331&cu=sgd&type=009063",
        "2月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99332&cu=sgd&type=009064",
        "3月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99333&cu=sgd&type=009065",
        "6月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99334&cu=sgd&type=009066",
        "9月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99335&cu=sgd&type=009067",
        "1年": "http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=88&d=99336&cu=sgd&type=009068",
    },
        "Sibor美元": {
            "1月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=87&d=99341&cu=usd&type=009063",
            "2月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=87&d=99342&cu=usd&type=009064",
            "3月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=87&d=99343&cu=usd&type=009065",
            "6月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=87&d=99344&cu=usd&type=009066",
            "9月": "http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=87&d=99345&cu=usd&type=009067",
            "1年": "http://data.eastmoney.com/shibor/shibor.aspx?m=sg&t=87&d=99346&cu=usd&type=009068",
        }}}
