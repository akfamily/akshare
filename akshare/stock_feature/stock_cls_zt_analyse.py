import re
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

from akshare.stock_feature.stock_cls_alerts import cls_url, cls_headers


def stock_zh_a_zt_analyse_cls(date: Optional[str] = None, img_path: str = "./") -> None:
    """
    财联社涨停分析-并下载涨停分析图片
    https://www.cls.cn/detail/756269
    :rtype: None
    """

    def get_schema_id(input_date) -> Optional[str]:
        # 财联社 加上年份获取不到内容，因此只用月份和天进行搜索
        input_date_cn = "%s月%s日" % (input_date.month, input_date.day)
        schema_payload = payload % (input_date_cn + "涨停分析")
        print(schema_payload)
        response = requests.request(
            "POST", cls_url, headers=cls_headers, data=schema_payload.encode("utf-8")
        )
        js = response.json()
        data = js["data"]["telegram"]["data"]
        if len(data) > 0:
            for i in data:
                schema = i["schema"]
                img_time_stamp = i["time"]
                dt = datetime.fromtimestamp(img_time_stamp)
                if dt.date() == input_date.date():
                    schema_id = re.search("\d+", schema).group(0)
                    if schema_id:
                        return schema_id
        return None

    def save_img(schema_id: str, img_path, input_date) -> None:
        url = "http://www.cls.cn/detail/%s" % schema_id
        response = requests.request("GET", url, headers=cls_headers)
        page = response.text
        pagesoup = BeautifulSoup(page, "lxml")
        links = [
            link
            for link in pagesoup.find_all(
                name="img", attrs={"src": re.compile(r"^https://img")}
            )
        ]
        if len(links) == 1:
            src_link = links[0].get("src")
            url = src_link.split("?")[0]
            html = requests.get(url)
            img_name = str(input_date.date())
            print(img_name)
            with open("%s/%s_zt_analyse.png" % (img_path, img_name), "wb") as file:
                file.write(html.content)
            print("获取今日涨停分析成功")

    payload = (
        '{"type":"all","keyword":"%s","os":"web","sv":"7.2.2","app":"CailianpressWeb"}'
    )

    if date:
        date = datetime.strptime(date, "%Y%m%d")
    else:
        date = datetime.today()
    schema_id = get_schema_id(date)
    if schema_id:
        save_img(schema_id, img_path, date)
    else:
        print("无法获取当日涨停分析")


# if __name__ == "__main__":
#     stock_zh_a_zt_analyse_cls = stock_zh_a_zt_analyse_cls(date="20210512")
#     print(stock_zh_a_zt_analyse_cls)
