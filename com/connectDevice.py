"""
@author: Orangecat
@contact: sugarnut@qq.com
@software: garner
@file: connectDevice.py
@time: 2020/07/23 上午10:06
@desc:
"""

"""
连接设备
"""
from appium import webdriver
import pytest


class Device:

    # 初始化连接设备
    def init_driver(self, platformName, platformVersion, deviceName, appPackage, appActivity, noReset):
        desired_caps = {}
        desired_caps["platformName"] = platformName
        desired_caps["platformVersion"] = platformVersion
        desired_caps["deviceName"] = deviceName
        desired_caps["appPackage"] = appPackage
        desired_caps["appActivity"] = appActivity
        desired_caps["noReset"] = noReset
        # desired_caps = {"platformName": "Android",
        #                 "platformVersion": "7.1.2",
        #                 "deviceName": "DA15205P40483",
        #                 "appPackage": "com.qianmi.cash",
        #                 "appActivity": "com.qianmi.cash.activity.LaunchActivity",
        #                 "noReset": "True"
        #                 }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        return self.driver
        # self.driver.implicitly_wait(30)

    def setUp_class(self):
        pass

    def tearDown(self):
        pass