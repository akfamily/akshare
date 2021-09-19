# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2019/9/30 13:58
Desc:
获取中国银行间市场交易商协会(http://www.nafmii.org.cn/)中孔雀开屏(http://zhuce.nafmii.org.cn/fans/publicQuery/manager)
的债券基本信息数据
"""
import pandas as pd
import requests

from akshare.futures.cons import BOND_BANK_URL, bond_bank_headers


# pd.set_option("display.max_columns", None)


def get_bond_bank(page_num=1):
    """
    获取中国银行间市场交易商协会(http://www.nafmii.org.cn/)中孔雀开屏(http://zhuce.nafmii.org.cn/fans/publicQuery/manager)
    的债券基本信息数据
    :param page_num: 输入数字页码
    :return: pandas.DataFrame
       firstIssueAmount          instNo  ... projPhase          releaseTime
       5  50000001337193  ...        60  2019-09-17 00:00:00
      20  50000001424511  ...        60  2019-09-17 00:00:00
       4  50000000900081  ...        60  2019-09-17 00:00:00
       3  60000001628024  ...        20  2019-09-17 00:00:00
       5  60000001611820  ...        20  2019-09-17 00:00:00
       5  50000001494880  ...        20  2019-09-17 00:00:00
      10  60000001175908  ...        60  2019-09-17 00:00:00
       5  50000001216207  ...        60  2019-09-17 00:00:00
       6  50000001138819  ...        60  2019-09-17 00:00:00
     2.5  60000001592028  ...        20  2019-09-17 00:00:00
      20  60000001414457  ...        60  2019-09-17 00:00:00
      10  60000001335845  ...        60  2019-09-17 00:00:00
      10  60000001181672  ...        60  2019-09-17 00:00:00
       5  50000000871600  ...        60  2019-09-17 00:00:00
     4.9  50000001116601  ...        60  2019-09-17 00:00:00
      10  60000001577858  ...        20  2019-09-17 00:00:00
       5  50000001426201  ...        60  2019-09-17 00:00:00
     2.5  60000001608635  ...        20  2019-09-17 00:00:00
      15  60000001425846  ...        60  2019-09-17 00:00:00
       2  50000001364547  ...        60  2019-09-17 00:00:00
    """
    temp_df = pd.DataFrame()
    payload = {
        "regFileName": "",
        "itemType": "",
        "startTime": "",
        "endTime": "",
        "entityName": "",
        "leadManager": "",
        "regPrdtType": "",
        "page": int(page_num),
        "rows": 20,
    }
    r = requests.post(BOND_BANK_URL, data=payload, headers=bond_bank_headers)
    data_json = r.json()  # 数据类型为 json 格式
    for item in data_json["rows"]:  # 遍历 json 的具体格式
        temp_df = temp_df.append(
            pd.DataFrame.from_dict(item, orient="index").T, sort=False
        )
    temp_df.reset_index(inplace=True, drop=True)  # 重新设置索引
    temp_df.drop_duplicates(inplace=True)
    return temp_df[
        [
            "firstIssueAmount",
            "isReg",
            "regFileName",
            "regPrdtType",
            "releaseTime",
            "projPhase",
        ]
    ]


if __name__ == "__main__":
    df = get_bond_bank(2)
    print(df)
