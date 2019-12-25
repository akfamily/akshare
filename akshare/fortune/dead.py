# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/12/25 14:17
contact: jindaxiang@163.com
desc: 
"""
import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}

# 将被请求的url全部整合到一个列表中
urls = [
    "https://www.itjuzi.com/api/closure?com_prov=&fund_status=&sort=&page=1",
    "https://www.itjuzi.com/api/closure?com_prov=&fund_status=&sort=&page=2",
    "https://www.itjuzi.com/api/closure?com_prov=&fund_status=&sort=&page=3",
]
# 开始事件
start = time.time()


# 特殊函数
async def get_request(url):
    # 基于上下文管理 来使用 aiohttp
    async with aiohttp.ClientSession() as s:
        # s.get(url,headers,params,proxy="http://ip:port")
        async with await s.get(url, headers=headers) as response:
            # response.read()二进制（.content）
            page_text = await response.json()
            print(page_text)
            return page_text


# 回调函数
def parse(task):
    # 获取 特殊函数的返回值 并赋值给page_text
    page_text = task.result()
    print(page_text)


tasks = []
# 循环urls
for url in urls:
    # 执行特殊函数 并给了c 其实就是一个协程
    c = get_request(url)
    # 创建一个任务对象
    task = asyncio.ensure_future(c)
    # 绑定回调函数
    task.add_done_callback(parse)
    # 并将任务对象添加到列表中
    tasks.append(task)
# 创建事件循环对象
loop = asyncio.get_event_loop()
# 将任务对象列表注册到该对象中并且开队该对象列表 当有多个对象时 假如遇见io阻塞 则必须执行完这个任务才执行下一个 所以这时候用到了 wait 挂起 遇见io阻塞则执行下一个
loop.run_until_complete(asyncio.wait(tasks))

print("总耗时：", time.time() - start)
# 结果为 2s多点
