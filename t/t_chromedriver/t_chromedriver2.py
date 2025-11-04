import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urlencode

"""
失败
添加用户代理和绕过自动化检测
"""
if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    # 添加用户代理，模拟真实浏览器
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # 绕过自动化检测
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    service = Service(r"D:\Program Files\chromedriver-win64\141.0.7390.78\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 执行脚本来隐藏webdriver属性
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

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

    try:
        driver.get(full_url)
        time.sleep(5)

        pre_element = driver.find_element(By.TAG_NAME, "pre")
        data = json.loads(pre_element.text)
        print(data)
    except Exception as e:
        print(f"错误: {e}")