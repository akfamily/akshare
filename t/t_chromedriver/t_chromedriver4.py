import math

import pandas as pd
import undetected_chromedriver as uc
import json
import time
from selenium.webdriver.common.by import By
from urllib.parse import urlencode

"""
使用 undetected-chromedriver
指定chrome.exe
"""
if __name__ == '__main__':
    try:
        # 指定 Chrome 浏览器路径和驱动路径
        driver = uc.Chrome(
            browser_executable_path=r"D:\Program Files\chrome-win64\141.0.7390.78\chrome.exe",  # 你的 Chrome.exe 路径
            driver_executable_path=r"D:\Program Files\chromedriver-win64\141.0.7390.78\chromedriver.exe"
        )

        pre_url = "https://eastmoney.com"
        print('访问主页...')
        driver.get(pre_url)
        time.sleep(3)

        url = "https://88.push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": "1",
            "pz": "100",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "wbp2u": "|0|0|0|web",
            "fid": "f3",
            "fs": "b:MK0021,b:MK0022,b:MK0023,b:MK0024",
            "fields": "f3,f12,f13",
        }
        full_url = f"{url}?{urlencode(params)}"
        print(f"访问URL: {full_url}")
        driver.get(full_url)
        time.sleep(5)

        pre_element = driver.find_element(By.TAG_NAME, "pre")
        data = json.loads(pre_element.text)
        print("获取数据成功:")
        # print(json.dumps(data, indent=2, ensure_ascii=False))
        # data_json = json.dumps(data, indent=2, ensure_ascii=False)
        per_page_num = len(data["data"]["diff"])
        total_page = math.ceil(data["data"]["total"] / per_page_num)
        # 存储所有页面数据
        temp_list = []
        # 添加第一页数据
        temp_list.append(pd.DataFrame(data["data"]["diff"]))
        print(f'per_page_num: {per_page_num}')
        print(f'total_page: {total_page}')
        print(f'temp_list: {temp_list}')
    except Exception as e:
        print(f"错误: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()