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

d = u2.connect("T203189A40323")
d(resourceId="com.qianmi.cash:id/textview_category", text="面").click()
d(resourceId="com.qianmi.cash:id/textview_name", text="加面").click()
d(resourceId="com.qianmi.cash:id/tv_cash_to_cash").click()
time.sleep(2)
d(focused=True).set_text("135372564846507493 \\n")
# d.send_keys()