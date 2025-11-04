import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    # 创建 Chrome 选项
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)  # 关键选项：保持浏览器打开

    # 创建 Service 对象
    service = Service(r"D:\Program Files\chromedriver-win64\141.0.7390.78\chromedriver.exe")

    # 通过 service 和 options 参数传递
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get('http://www.google.com/')
    time.sleep(5)

    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys('ChromeDriver')
    search_box.submit()

    time.sleep(5)
