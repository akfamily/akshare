#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2021/11/8 17:48
Desc: 同花顺-板块-行业板块
http://q.10jqka.com.cn/thshy/
"""
import os
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from py_mini_racer import py_mini_racer
from tqdm import tqdm

from akshare.utils import demjson


def _get_js_path_ths(name: str = None, module_file: str = None) -> str:
    """
    获取 JS 文件的路径(从模块所在目录查找)
    :param name: 文件名
    :type name: str
    :param module_file: 模块路径
    :type module_file: str
    :return: 路径
    :rtype: str
    """
    module_folder = os.path.abspath(os.path.dirname(os.path.dirname(module_file)))
    module_json_path = os.path.join(module_folder, "stock_feature", name)
    return module_json_path


def _get_file_content_ths(file_name: str = "ase.min.js") -> str:
    """
    获取 JS 文件的内容
    :param file_name:  JS 文件名
    :type file_name: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_name = file_name
    setting_file_path = _get_js_path_ths(setting_file_name, __file__)
    with open(setting_file_path) as f:
        file_data = f.read()
    return file_data


def stock_board_industry_name_ths() -> pd.DataFrame:
    """
    同花顺-板块-行业板块-行业
    http://q.10jqka.com.cn/thshy/
    :return: 所有行业板块的名称和链接
    :rtype: pandas.DataFrame
    """
    code_name_ths_map = {'881101': '种植业与林业',
                         '881102': '养殖业',
                         '881103': '农产品加工',
                         '881104': '农业服务',
                         '881105': '煤炭开采加工',
                         '881107': '油气开采及服务',
                         '881108': '化学原料',
                         '881109': '化学制品',
                         '881110': '化工合成材料',
                         '881112': '钢铁',
                         '881114': '金属新材料',
                         '881115': '建筑材料',
                         '881116': '建筑装饰',
                         '881117': '通用设备',
                         '881118': '专用设备',
                         '881119': '仪器仪表',
                         '881120': '电力设备',
                         '881121': '半导体及元件',
                         '881122': '光学光电子',
                         '881123': '其他电子',
                         '881124': '消费电子',
                         '881125': '汽车整车',
                         '881126': '汽车零部件',
                         '881127': '非汽车交运',
                         '881128': '汽车服务',
                         '881129': '通信设备',
                         '881130': '计算机设备',
                         '881131': '白色家电',
                         '881132': '黑色家电',
                         '881133': '饮料制造',
                         '881134': '食品加工制造',
                         '881135': '纺织制造',
                         '881136': '服装家纺',
                         '881137': '造纸',
                         '881138': '包装印刷',
                         '881139': '家用轻工',
                         '881140': '化学制药',
                         '881141': '中药',
                         '881142': '生物制品',
                         '881143': '医药商业',
                         '881144': '医疗器械',
                         '881145': '电力',
                         '881146': '燃气',
                         '881148': '港口航运',
                         '881149': '公路铁路运输',
                         '881151': '机场航运',
                         '881152': '物流',
                         '881153': '房地产开发',
                         '881155': '银行',
                         '881156': '保险及其他',
                         '881157': '证券',
                         '881158': '零售',
                         '881159': '贸易',
                         '881160': '景点及旅游',
                         '881161': '酒店及餐饮',
                         '881162': '通信服务',
                         '881163': '计算机应用',
                         '881164': '传媒',
                         '881165': '综合',
                         '881166': '国防军工',
                         '881167': '非金属材料',
                         '881168': '工业金属',
                         '881169': '贵金属',
                         '881170': '小金属',
                         '881171': '自动化设备',
                         '881172': '电子化学品',
                         '881173': '小家电',
                         '881174': '厨卫电器',
                         '881175': '医疗服务',
                         '881176': '房地产服务',
                         '881177': '互联网电商',
                         '881178': '教育',
                         '881179': '其他社会服务',
                         '881180': '石油加工贸易',
                         '881181': '环保',
                         '881182': '美容护理',
                         '884001': '种子生产',
                         '884002': '粮食种植',
                         '884003': '其他种植业',
                         '884004': '林业',
                         '884005': '海洋捕捞',
                         '884006': '水产养殖',
                         '884007': '畜禽养殖',
                         '884008': '饲料',
                         '884009': '果蔬加工',
                         '884010': '粮油加工',
                         '884011': '其他农产品加工',
                         '884012': '农业综合',
                         '884013': '动物保健',
                         '884014': '煤炭开采',
                         '884015': '焦炭加工',
                         '884016': '油气开采',
                         '884018': '油服工程',
                         '884020': '石油加工',
                         '884021': '油品石化贸易',
                         '884022': '纯碱',
                         '884023': '氯碱',
                         '884024': '无机盐',
                         '884025': '其他化学原料',
                         '884026': '氮肥',
                         '884027': '磷肥及磷化工',
                         '884028': '农药',
                         '884030': '涂料油墨',
                         '884031': '钾肥',
                         '884032': '民爆用品',
                         '884033': '纺织化学用品',
                         '884034': '其他化学制品',
                         '884035': '复合肥',
                         '884036': '氟化工',
                         '884039': '聚氨酯',
                         '884041': '涤纶',
                         '884043': '粘胶',
                         '884044': '其他纤维',
                         '884045': '氨纶',
                         '884046': '其他塑料制品',
                         '884048': '改性塑料',
                         '884050': '其他橡胶制品',
                         '884051': '炭黑',
                         '884052': '普钢',
                         '884053': '铝',
                         '884054': '铜',
                         '884055': '铅锌',
                         '884056': '其他金属新材料',
                         '884057': '磁性材料',
                         '884058': '非金属材料Ⅲ',
                         '884059': '玻璃玻纤',
                         '884060': '水泥',
                         '884062': '其他建材',
                         '884063': '耐火材料',
                         '884064': '管材',
                         '884065': '装饰园林',
                         '884066': '房屋建设',
                         '884067': '基础建设',
                         '884068': '专业工程',
                         '884069': '机床工具',
                         '884071': '磨具磨料',
                         '884073': '制冷空调设备',
                         '884074': '其他通用设备',
                         '884075': '金属制品',
                         '884076': '纺织服装设备',
                         '884077': '工程机械',
                         '884078': '农用机械',
                         '884080': '能源及重型设备',
                         '884081': '印刷包装机械',
                         '884082': '其他专用设备',
                         '884083': '楼宇设备',
                         '884084': '环保设备',
                         '884085': '电机',
                         '884086': '电气自控设备',
                         '884088': '输变电设备',
                         '884089': '线缆部件及其他',
                         '884090': '分立器件',
                         '884091': '半导体材料',
                         '884092': '印制电路板',
                         '884093': '被动元件',
                         '884094': '面板',
                         '884095': 'LED',
                         '884096': '光学元件',
                         '884098': '消费电子零部件及组装',
                         '884099': '乘用车',
                         '884100': '商用载货车',
                         '884101': '商用载客车',
                         '884105': '轨交设备',
                         '884106': '其他交运设备',
                         '884107': '汽车服务Ⅲ',
                         '884112': '冰洗',
                         '884113': '空调',
                         '884115': '小家电Ⅲ',
                         '884116': '其他白色家电',
                         '884117': '彩电',
                         '884118': '其他黑色家电',
                         '884119': '其他酒类',
                         '884120': '软饮料',
                         '884123': '肉制品',
                         '884124': '调味发酵品',
                         '884125': '乳品',
                         '884126': '其他食品',
                         '884128': '棉纺',
                         '884130': '印染',
                         '884131': '辅料',
                         '884132': '其他纺织',
                         '884136': '鞋帽及其他',
                         '884137': '家纺',
                         '884139': '家具',
                         '884140': '其他家用轻工',
                         '884141': '饰品',
                         '884142': '文娱用品',
                         '884143': '原料药',
                         '884144': '化学制剂',
                         '884145': '医疗设备',
                         '884146': '火电',
                         '884147': '水电',
                         '884149': '热力',
                         '884150': '新能源发电',
                         '884152': '燃气Ⅲ',
                         '884153': '港口',
                         '884154': '高速公路',
                         '884155': '铁路运输',
                         '884156': '机场',
                         '884157': '航空运输',
                         '884158': '多元金融',
                         '884159': '保险',
                         '884160': '百货零售',
                         '884161': '专业连锁',
                         '884162': '商业物业经营',
                         '884163': '人工景点',
                         '884164': '自然景点',
                         '884165': '旅游综合',
                         '884167': '酒店',
                         '884168': '餐饮',
                         '884172': '有线电视网络',
                         '884173': '通信服务Ⅲ',
                         '884174': '软件开发',
                         '884176': '出版',
                         '884177': '影视院线',
                         '884178': '广告营销',
                         '884179': '其他传媒',
                         '884180': '航天装备',
                         '884181': '航空装备',
                         '884182': '地面兵装',
                         '884183': '航海装备',
                         '884184': '特钢',
                         '884185': '贵金属Ⅲ',
                         '884186': '其他小金属',
                         '884188': '白酒',
                         '884189': '啤酒',
                         '884191': '航运',
                         '884192': '仪器仪表Ⅲ',
                         '884193': '其他电子Ⅲ',
                         '884194': '汽车零部件Ⅲ',
                         '884195': '造纸Ⅲ',
                         '884197': '中药Ⅲ',
                         '884199': '医药商业Ⅲ',
                         '884200': '公交',
                         '884201': '物流Ⅲ',
                         '884202': '住宅开发',
                         '884203': '产业地产',
                         '884205': '证券Ⅲ',
                         '884206': '贸易Ⅲ',
                         '884207': '计算机设备Ⅲ',
                         '884208': '综合Ⅲ',
                         '884209': '钛白粉',
                         '884210': '食品及饲料添加剂',
                         '884211': '有机硅',
                         '884212': '合成树脂',
                         '884213': '膜材料',
                         '884214': '冶钢原料',
                         '884215': '稀土',
                         '884216': '能源金属',
                         '884217': '工程咨询服务',
                         '884218': '机器人',
                         '884219': '工控设备',
                         '884220': '激光设备',
                         '884221': '其他自动化设备',
                         '884222': '光伏设备',
                         '884223': '风电设备',
                         '884224': '电池',
                         '884225': '其他电源设备',
                         '884226': '集成电路设计',
                         '884227': '集成电路制造',
                         '884228': '集成电路封测',
                         '884229': '半导体设备',
                         '884230': '品牌消费电子',
                         '884231': '电子化学品Ⅲ',
                         '884232': '厨卫电器Ⅲ',
                         '884233': '休闲食品',
                         '884234': '服装',
                         '884235': '印刷',
                         '884236': '包装',
                         '884237': '瓷砖地板',
                         '884238': '血液制品',
                         '884239': '疫苗',
                         '884240': '其他生物制品',
                         '884242': '医疗耗材',
                         '884243': '体外诊断',
                         '884244': '医疗研发外包',
                         '884245': '其他医疗服务',
                         '884246': '电能综合服务',
                         '884247': '商业地产',
                         '884248': '房地产服务Ⅲ',
                         '884249': '国有大型银行',
                         '884250': '股份制银行',
                         '884251': '城商行',
                         '884252': '农商行',
                         '884253': '其他银行',
                         '884254': '旅游零售',
                         '884255': '互联网电商Ⅲ',
                         '884256': '教育Ⅲ',
                         '884257': '专业服务',
                         '884258': '体育',
                         '884259': '其他社会服务Ⅲ',
                         '884260': '游戏',
                         '884261': '数字媒体',
                         '884262': '通信网络设备及器件',
                         '884263': '通信线缆及配套',
                         '884264': '通信终端及配件',
                         '884265': '其他通信设备',
                         '884266': '军工电子',
                         '884267': '大气治理',
                         '884268': '水务及水治理',
                         '884269': '固废治理',
                         '884270': '综合环境治理',
                         '884271': '个护用品',
                         '884272': '化妆品',
                         '884273': '医疗美容',
                         '884274': 'IT服务'}
    temp_df = pd.DataFrame.from_dict(code_name_ths_map, orient="index")
    temp_df.reset_index(inplace=True)
    temp_df.columns = ['code', 'name']
    temp_df = temp_df[[
        'name',
        'code',
    ]]
    return temp_df


def stock_board_industry_cons_ths(symbol: str = "半导体及元件") -> pd.DataFrame:
    """
    同花顺-板块-行业板块-成份股
    http://q.10jqka.com.cn/thshy/detail/code/881121/
    :param symbol: 板块名称
    :type symbol: str
    :return: 成份股
    :rtype: pandas.DataFrame
    """
    stock_board_ths_map_df = stock_board_industry_name_ths()
    symbol = stock_board_ths_map_df[stock_board_ths_map_df['name'] == symbol]['code'].values[0]
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call('v')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Cookie': f'v={v_code}'
    }
    url = f'http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/1/ajax/1/code/{symbol}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    try:
        page_num = int(soup.find_all('a', attrs={'class': 'changePage'})[-1]['page'])
    except IndexError as e:
        page_num = 1
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num+1), leave=False):
        v_code = js_code.call('v')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Cookie': f'v={v_code}'
        }
        url = f'http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/{page}/ajax/1/code/{symbol}'
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.rename({"涨跌幅(%)": "涨跌幅",
                   "涨速(%)": "涨速",
                   "换手(%)": "换手",
                   "振幅(%)": "振幅",
                   }, inplace=True, axis=1)
    del big_df['加自选']
    big_df['代码'] = big_df['代码'].astype(str).str.zfill(6)
    return big_df


def stock_board_industry_info_ths(symbol: str = "半导体及元件") -> pd.DataFrame:
    """
    同花顺-板块-行业板块-板块简介
    http://q.10jqka.com.cn/gn/detail/code/301558/
    :param symbol: 板块简介
    :type symbol: str
    :return: 板块简介
    :rtype: pandas.DataFrame
    """
    stock_board_ths_map_df = stock_board_industry_name_ths()
    symbol_code = stock_board_ths_map_df[stock_board_ths_map_df['name'] == symbol]['code'].values[0]
    url = f'http://q.10jqka.com.cn/thshy/detail/code/{symbol_code}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    name_list = [item.text.strip() for item in soup.find('div', attrs={'class': 'board-infos'}).find_all('dt')]
    value_list = [item.text.strip().replace('\n', '/') for item in soup.find('div', attrs={'class': 'board-infos'}).find_all('dd')]
    temp_df = pd.DataFrame([name_list, value_list]).T
    temp_df.columns = ['项目', "值"]
    return temp_df


def stock_board_industry_index_ths(symbol: str = "半导体及元件", start_date: str = "20200101", end_date: str = "20211027") -> pd.DataFrame:
    """
    同花顺-板块-行业板块-指数数据
    http://q.10jqka.com.cn/gn/detail/code/301558/
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :param symbol: 指数数据
    :type symbol: str
    :return: 指数数据
    :rtype: pandas.DataFrame
    """
    code_map = stock_board_industry_name_ths()
    code_map = dict(zip(code_map['name'].values, code_map['code'].values))
    symbol_code = code_map[symbol]
    big_df = pd.DataFrame()
    current_year = datetime.now().year
    for year in tqdm(range(2000, current_year+1), leave=False):
        url = f'http://d.10jqka.com.cn/v4/line/bk_{symbol_code}/01/{year}.js'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Referer': 'http://q.10jqka.com.cn',
            'Host': 'd.10jqka.com.cn'
        }
        r = requests.get(url, headers=headers)
        data_text = r.text
        try:
            demjson.decode(data_text[data_text.find('{'):-1])
        except:
            continue
        temp_df = demjson.decode(data_text[data_text.find('{'):-1])
        temp_df = pd.DataFrame(temp_df['data'].split(';'))
        temp_df = temp_df.iloc[:, 0].str.split(',', expand=True)
        big_df = big_df.append(temp_df, ignore_index=True)
    if len(big_df.columns) == 11:
        big_df.columns = [
            '日期',
            '开盘价',
            '最高价',
            '最低价',
            '收盘价',
            '成交量',
            '成交额',
            '_',
            '_',
            '_',
            '_',
        ]
    else:
        big_df.columns = [
            '日期',
            '开盘价',
            '最高价',
            '最低价',
            '收盘价',
            '成交量',
            '成交额',
            '_',
            '_',
            '_',
            '_',
            '_',
        ]
    big_df = big_df[[
        '日期',
        '开盘价',
        '最高价',
        '最低价',
        '收盘价',
        '成交量',
        '成交额',
    ]]
    big_df['日期'] = pd.to_datetime(big_df['日期']).dt.date
    condition_one = pd.to_datetime(start_date) < big_df['日期']
    condition_two = pd.to_datetime(end_date) > big_df['日期']
    big_df = big_df[condition_one & condition_two]
    big_df['开盘价'] = pd.to_numeric(big_df['开盘价'])
    big_df['最高价'] = pd.to_numeric(big_df['最高价'])
    big_df['最低价'] = pd.to_numeric(big_df['最低价'])
    big_df['收盘价'] = pd.to_numeric(big_df['收盘价'])
    big_df['成交量'] = pd.to_numeric(big_df['成交量'])
    big_df['成交额'] = pd.to_numeric(big_df['成交额'])
    return big_df


def stock_ipo_benefit_ths() -> pd.DataFrame:
    """
    同花顺-数据中心-新股数据-IPO受益股
    http://data.10jqka.com.cn/ipo/syg/
    :return: IPO受益股
    :rtype: pandas.DataFrame
    """
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call('v')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Cookie': f'v={v_code}'
    }
    url = f'http://data.10jqka.com.cn/ipo/syg/field/invest/order/desc/page/2/ajax/1/free/1/'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    page_num = soup.find('span', attrs={'class': 'page_info'}).text.split('/')[1]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(page_num)+1), leave=False):
        url = f'http://data.10jqka.com.cn/ipo/syg/field/invest/order/desc/page/{page}/ajax/1/free/1/'
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [
        '序号',
        '股票代码',
        '股票简称',
        '收盘价',
        '涨跌幅',
        '市值',
        '参股家数',
        '投资总额',
        '投资占市值比',
        '参股对象',
    ]
    big_df['股票代码'] = big_df['股票代码'].astype(str).str.zfill(6)
    big_df['序号'] = pd.to_numeric(big_df['序号'], errors='coerce')
    big_df['收盘价'] = pd.to_numeric(big_df['收盘价'], errors='coerce')
    big_df['涨跌幅'] = pd.to_numeric(big_df['涨跌幅'], errors='coerce')
    big_df['参股家数'] = pd.to_numeric(big_df['参股家数'], errors='coerce')
    big_df['投资占市值比'] = pd.to_numeric(big_df['投资占市值比'], errors='coerce')
    return big_df


if __name__ == '__main__':
    stock_board_industry_name_ths_df = stock_board_industry_name_ths()
    print(stock_board_industry_name_ths_df)

    stock_board_industry_cons_ths_df = stock_board_industry_cons_ths(symbol="涂料油墨")
    print(stock_board_industry_cons_ths_df)

    stock_board_industry_info_ths_df = stock_board_industry_info_ths(symbol="涂料油墨")
    print(stock_board_industry_info_ths_df)

    stock_board_industry_index_ths_df = stock_board_industry_index_ths(symbol="半导体及元件", start_date="20200101", end_date="20211027")
    print(stock_board_industry_index_ths_df)

    stock_ipo_benefit_ths_df = stock_ipo_benefit_ths()
    print(stock_ipo_benefit_ths_df)

    for stock in stock_board_industry_name_ths_df['name']:
        print(stock)
        stock_board_industry_index_ths_df = stock_board_industry_index_ths(symbol=stock)
        print(stock_board_industry_index_ths_df)
