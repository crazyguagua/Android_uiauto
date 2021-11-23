#!/usr/bin/env python
# encoding: utf-8

"""
@author: Orangecat
@contact: sugarnut@qq.com
@software: garner
@file: runTest.py
@time: 2021/11/23 上午11:06
@desc:
"""
from com.comFunction import findFunction

class testMain():
    desired_caps = {"platformName": "Android",
                    "platformVersion": "7.1.1",
                    "deviceName": "T203189A40323",
                    "appPackage": "com.qianmi.cash",
                    "appActivity": "com.qianmi.cash.activity.LaunchActivity",
                    "noReset": "True"
                    }
    def testPrintDevices(self):

        print(testMain.desired_caps["platformName"])

        self.testDevices = findFunction(testMain.desired_caps["platformName"], testMain.desired_caps["platformVersion"],
                                        testMain.desired_caps["deviceName"], testMain.desired_caps["appPackage"],
                                        testMain.desired_caps["appActivity"], testMain.desired_caps["noReset"])



        print("高度：", self.testDevices.getScreenSize()["height"])
        print("宽度：", self.testDevices.getScreenSize()["width"])


if __name__ == '__main__':
    testMain().testPrintDevices()