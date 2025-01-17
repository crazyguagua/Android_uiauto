"""
@author: Orangecat
@contact: sugarnut@qq.com
@software: garner
@file: comFunction.py
@time: 2020/07/23 上午10:16
@desc:
"""

"""
封装查找元素公共方法
"""

from com.connectDevice import Device
from selenium.webdriver.support.wait import WebDriverWait


class findFunction(Device):
    # 构造函数，初始化驱动
    def __init__(self, platformName, platformVersion, deviceName, appPackage, appActivity, noReset):
        self.driver = Device.init_driver(self, platformName, platformVersion, deviceName, appPackage, appActivity, noReset)

    # 封装显示等待根据ID获取元素
    def findElement_ByID(self, element, waitTime=5):
        return WebDriverWait(self.driver, waitTime, 0.5).until(
            lambda driver: self.driver.find_element_by_id(element)
        )

    # 封装显示等待根据Xpath获取元素
    def findElement_ByXpath(self, element, waitTime=5):
        return WebDriverWait(self.driver, waitTime, 0.5).until(
            lambda driver: self.driver.find_element_by_xpath(element)
        )

    # 封装显示等待根据Xpath获取元素组
    def findElements_ByXpath(self, element, waitTime=5):
        return WebDriverWait(self.driver, waitTime, 0.5).until(
            lambda driver: self.driver.find_elements_by_xpath(element)
        )

    # 封装显示等待根据选择使用方式获取元素
    def findElement(self, waitTime=5, *element):
        return WebDriverWait(self.driver, waitTime, 0.5).until(
            lambda driver: self.driver.find_element(*element)
        )

    # 获取屏幕尺寸
    def getScreenSize(self):
        screensize = self.driver.get_window_size()
        return screensize

    # 屏幕水平中间位置上下滑动屏幕
    def swipeByVertical(self, p1, p2):
        screensize = self.driver.get_window_size()
        self.screenW = screensize["width"]
        self.screenH = screensize["height"]
        x = self.screenW / 2
        y1 = int(self.screenH * p1)
        y2 = int(self.screenH * p2)

        self.driver.swipe(x, y1, x, y2, 3000)

    # 屏幕上下中间位置左右滑动屏幕
    def swipeByHorizon(self, p1, p2):
        screensize = self.driver.get_window_size()
        self.screenW = screensize["width"]
        self.screenH = screensize["height"]
        y = self.screenH / 2
        x1 = int(self.screenW * p1)
        x2 = int(self.screenW * p2)

        self.driver.swipe(x1, y, x2, y, 3000)

    def tapScreenPoint(self, x1, y1, duration=500):
        # print(str(self.screenW) +"*"+ str(self.screenH))
        # xd_x = (x1/1920)*self.screenW
        # xd_y = (y1/1080)*self.screenH
        self.driver.tap([(x1, y1)], duration)
