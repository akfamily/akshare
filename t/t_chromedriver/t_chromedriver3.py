import undetected_chromedriver as uc
import json
import time
from selenium.webdriver.common.by import By
from urllib.parse import urlencode

"""
使用 undetected-chromedriver
"""
if __name__ == '__main__':
    try:
        # 使用 undetected_chromedriver
        driver = uc.Chrome(
            driver_executable_path=r"D:\Program Files\chromedriver-win64\141.0.7390.78\chromedriver.exe"
        )

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
        time.sleep(8)  # 等待更长时间

        # 尝试多种方式获取内容
        try:
            pre_element = driver.find_element(By.TAG_NAME, "pre")
            data = json.loads(pre_element.text)
            print("通过pre标签获取数据成功:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            # 如果pre标签失败，尝试获取整个页面内容
            page_source = driver.page_source
            print("页面源代码:")
            print(page_source)

    except Exception as e:
        print(f"错误: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()