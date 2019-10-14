# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
contact: jindaxiang@163.com
desc: 
"""

# -*- coding:utf-8 -*-
import sys
import numpy as np
import matplotlib.pyplot as plt

# 加载图片的名称
pathname = r'C:\Users\king\PycharmProjects\akshare\大连商品交易所_豆一.jpg'
# Mac下用GIMP查看坐标，注意下面提到的坐标顺序是[y, x]，windows下系统自带画图似乎就可以
# 起始像素点坐标（左上角）
start_points = [31, 56]
# 结束像素点点坐标（右下角）
end_points = [250, 735]
# 要显示曲线的像素点的y的坐标范围（从上到下）
pivot_ys = [29, 252]
# 要显示曲线的y的真实坐标范围（从上到下）
pivot_metrics = [70000, 0]
# 曲线的颜色RGB
line_color = np.asarray([0., 0., 0.])
img = None
try:
    import cv2

    img = cv2.imread(pathname)
    # cv2颜色的顺序是GBR
    line_color = [line_color[2], line_color[1], line_color[0]]
except ImportError:
    print('cv2 modular not found!')

if img is None:
    try:
        from PIL import Image

        img = np.array(Image.open(pathname))
    except ImportError:
        print('PIL modular not found!')

if img is None:
    print('PIL or cv2 not found!')
    sys.exit()

ratio = (pivot_metrics[1] - pivot_metrics[0] + 0.0) / (pivot_ys[1] - pivot_ys[0] + 0.0)  # 0.0的作用是转化为float型

cand = {}

min_c = 100000
max_c = -1

temp = {}
for r in range(start_points[0], end_points[0]):
    for c in range(start_points[1], end_points[1]):
        rgb = img[r, c, :]
        # rgb = img[r, c][0:3]
        diff1 = np.linalg.norm(rgb - line_color)
        if diff1 < 40:
            if c not in cand:
                cand[c] = []
                temp[c] = []
            y = pivot_metrics[0] + ratio * (r - pivot_ys[0])
            cand[c].append(y)  # cand [c] 存储了多个 x坐标为c的有颜色的点的y坐标
            temp[c].append(r)
            if c < min_c:
                min_c = c
            if c > max_c:
                max_c = c

n = max_c - min_c + 1
data = np.zeros((n, 1))
for i in range(n):
    print(i)
    try:
        ys = np.asarray(cand[i + min_c])
        y = np.mean(ys)
        data[i] = y
    except:
        continue

# data = [item for item in data if item != 0]
x_values = [v for v in range(0, len(data))]
y_values = data
plt.plot(x_values, y_values)
plt.show()
