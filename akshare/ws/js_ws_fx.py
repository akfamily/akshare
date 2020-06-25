# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2019/11/16 22:47
Desc: 金十数据 websocket 实时数据接口
先对: https://sshhbhekjf.jin10.com:9081/socket.io/?EIO=3&transport=polling 做长轮询, 后面还有个参数 t 可以去除
返回: 97:0{"sid":"C10ZwKOEHslD9QOyAGrS","upgrades":["websocket"],"pingInterval":25000,"pingTimeout":60000}
获取里面的 sid 传入 wss
wss://sshhbhekjf.jin10.com:9081/socket.io/?EIO=3&transport=websocket&sid=SntBLMopyaK6Z-sVAGr1
访问即可

websocket test website: http://www.websocket-test.com/
reference list:
1. https://www.jianshu.com/p/848d99c041bd
2. https://www.jianshu.com/p/a3e06ec1a3a0
"""
import json
import time
from threading import Timer, Event, Thread

import requests
import websocket


def _get_sid() -> str:
    """
    XHR 监听 sid
    需要动态获取sid, 拼接后访问
    https://www.jb51.net/article/149738.htm
    用轮询获取 sid 用 sid 请求
    :return: sid 内容
    :rtype: str
    """
    url = "https://sshhbhekjf.jin10.com:9081/socket.io/?EIO=3&transport=polling"
    r = requests.get(url)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{"):])
    return data_json["sid"]


class HeartbeatThread(Thread):
    """
    心跳
    """
    def __init__(self, event, ws):
        super(HeartbeatThread, self).__init__()
        self.event = event
        self.ws = ws

    def run(self):
        while True:
            # 发送ping包
            self.ws.send("2")
            self.event.wait(timeout=2)


def on_message(ws, message):
    """
    接收信息, 如果要存数据需要在这里处理
    :param ws: 
    :type ws:
    :param message:
    :type message:
    :return:
    :rtype:
    """
    print(message)


def on_error(ws, error):
    """

    :param ws:
    :type ws:
    :param error:
    :type error:
    :return:
    :rtype:
    """
    print(error)


def on_close(ws):
    """
    :param ws:
    :type ws:
    :return:
    :rtype:
    """
    print("### closed ###")


def on_open(ws):
    """
    请求连接
    :param ws:
    :type ws:
    :return:
    :rtype:
    """
    ws.send("2probe")
    time.sleep(0.02)  # 发送第二次需要短暂暂停
    ws.send("5")  # 发送字符串 5 来完成握手


def on_emit(ws):
    """
    创建心跳线程
    :param ws: object
    :type ws: websocket object
    :return: None
    :rtype: None
    """
    event = Event()
    heartbeat = HeartbeatThread(event, ws)
    heartbeat.start()


def watch_jinshi_fx():

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        f"wss://sshhbhekjf.jin10.com:9081/socket.io/?EIO=3&transport=websocket&sid={_get_sid()}",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    t = Timer(20, on_emit, args=(ws,))
    t.start()
    ws.run_forever()


if __name__ == "__main__":
    watch_jinshi_fx()
