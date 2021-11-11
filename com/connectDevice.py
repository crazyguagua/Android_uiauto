"""
连接设备
"""
from appium import webdriver


class Device:
    def __init__(self):
        desired_caps = {"platformName": "Android",
                        "platformVersion": "7.1.1",
                        "deviceName": "T203189A40323",
                        "appPackage": "com.qianmi.cash",
                        "appActivity": "com.qianmi.cash.activity.LaunchActivity",
                        "noReset": "True"
                        }
        # desired_caps = {"platformName": "Android",
        #                 "platformVersion": "7.1.2",
        #                 "deviceName": "DA15205P40483",
        #                 "appPackage": "com.qianmi.cash",
        #                 "appActivity": "com.qianmi.cash.activity.LaunchActivity",
        #                 "noReset": "True"
        #                 }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        # self.driver.implicitly_wait(30)
        screensize = self.driver.get_window_size()
        self.screenW = screensize['width']
        self.screenH = screensize['height']
