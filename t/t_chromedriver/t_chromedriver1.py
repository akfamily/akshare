import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urlencode

if __name__ == '__main__':
    # 创建 Chrome 选项
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)  # 关键选项：保持浏览器打开

    # 创建 Service 对象
    service = Service(r"D:\Program Files\chromedriver-win64\141.0.7390.78\chromedriver.exe")

    # 通过 service 和 options 参数传递
    driver = webdriver.Chrome(service=service, options=chrome_options)

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
    driver.get(full_url)
    time.sleep(5)

    pre_element = driver.find_element(By.TAG_NAME, "pre")
    data = json.loads(pre_element.text)
    print(data)


