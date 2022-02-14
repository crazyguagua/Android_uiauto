#!/usr/bin/env python
# encoding: utf-8

"""
@author: Orangecat
@contact: sugarnut@qq.com
@software: garner
@file: test_UI2.py
@time: 2021/12/6 下午4:44
@desc:
"""

import uiautomator2 as u2
import time

d = u2.connect("127.0.0.1:7555")

# 打开抖音
d(text="抖音").click()
time.sleep(5)
# 点击搜索
d(resourceId="com.ss.android.ugc.aweme:id/fie").click()
d(resourceId="com.ss.android.ugc.aweme:id/fl_intput_hint_container").click()
d.send_keys("348288672")

# # 循环点赞
# while True:
#     time.sleep(0.5)
#     d.double_click(0.22, 0.388)
