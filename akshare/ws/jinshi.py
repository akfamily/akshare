# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/11/16 22:47
contact: jindaxiang@163.com
desc: 金十数据 websocket 实时数据接口
"""
import json
import time
from threading import Timer, Event, Thread

import requests
import websocket


def _get_sid():
    """
    XHR 监听 sid
    需要动态获取sid, 拼接后访问
    https://www.jb51.net/article/149738.htm
    用轮询获取 sid 用 sid 请求
    :return:
    :rtype:
    """
    url = "https://sshhbhekjf.jin10.com:9081/socket.io/?EIO=3&transport=polling"
    r = requests.get(url)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{") :])
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
    接收信息
    :param ws: 
    :type ws:
    :param message:
    :type message:
    :return:
    :rtype:
    """
    print(message)


def on_error(ws, error):
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
    """请求连接"""
    ws.send("2probe")
    time.sleep(0.02)
    ws.send("5")


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

    while True:
        content = input("input: ")
        # 发送信息
        # 4: engine.io message
        # 2: socket.io event
        # chat message event message
        ws.send('42["chat message","{0}"]'.format(content))
        time.sleep(0.2)


def watch():

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        f"wss://sshhbhekjf.jin10.com:9081/socket.io/?EIO=3&transport=websocket&sid={_get_sid()}",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    t = Timer(3, on_emit, args=(ws,))
    t.start()
    ws.run_forever()


if __name__ == "__main__":
    watch()
