# coding = utf-8

import os
import platform
import time
import re

import pytest
import uiautomator2 as u2
import allure
from com.ADBCommon import ADBTools


class Nox:
    # 关闭模拟器
    @allure.step('关闭模拟器')
    def close(self, name):
        # 查询进程号关闭模拟器
        rep = os.popen('tasklist|findstr ' + str(name) + '.exe')
        list_str =rep.read()
        pid = re.findall(r"\d+", list_str)[0]
        os.popen('taskkill.exe /pid:' + str(pid))
        print("关闭模拟器")

    # 打开模拟器
    @allure.step('打开模拟器')
    def open(self, appPath):
        # 打开模拟器
        if platform.system() == "Windows":
            runAPP = "start " + appPath
            os.system(runAPP)
        else:
            runAPP = "open " + appPath
            os.system(runAPP)
        print("等待模拟器启动")
        tools = ADBTools()
        for i in range(1, 20):
            resp = os.popen(tools.adb('devices')).read()
            if '127.0.0.1' in resp:
                print("模拟器正常启动！")
                break
            elif '127.0.0.1' not in resp and i != 20:
                time.sleep(2)
            else:
                raise Exception("模拟器启动异常！")


class openCommon:
    def __init__(self, IP='127.0.0.1:62001'):
        self.driver = self.driver(IP)
        # d.implicitly_wait(10)
    # uiAutoMator2连接
    @allure.step('连接uiAutoMator2')
    def driver(self, IP='127.0.0.1:62001'):
        d = u2.connect(IP)
        # d.implicitly_wait(10)
        return d

    @allure.step('打开app')
    def appOpen(self, package_name='com.qianmi.cash'):
        self.driver.app_start(package_name, stop=True)
        # os.system("start adb shell am start -n com.qianmi.cash/.activity.LaunchActivity")
        print("启动云小店")

    # 关闭app
    @allure.step('关闭app')
    def appClose(self, package_name='com.qianmi.cash'):
        self.driver.app_stop(package_name)
        # os.system("start adb shell am force-stop com.qianmi.cash")
        print("关闭云小店")

    # 安装apk
    @allure.step("安装apk")
    def appInstall(self, path='F:\\软件包\\云小店\\cash-android_QianMi-test_2.14.0_release_520.apk'):
        self.driver.app_install(path)
        print("安装apk")

    # 卸载app
    @allure.step("卸载app")
    def appUninstall(self, package_name='com.qianmi.cash'):
        self.driver.app_uninstall(package_name)
        print("卸载app")




class functionCommon(openCommon):

    # 获取屏幕的像素尺寸
    @allure.step('获取屏幕的像素尺寸')
    def getSize(self):
        y, x = self.driver.window_size()
        return x, y

    # 按坐标比例点击按钮
    def buttonClick1(self, p1, p2):
        y, x = self.driver.window_size()
        # x = getSize()[0]
        # y = getSize()[1]
        self.driver.click(p1 * x, p2 * y)

    # 按坐标绝对值点击按钮
    def buttonClick2(self, p1, p2):
        self.driver.click(p1, p2)

    # 按坐标比例长点击
    def buttonLongClick1(self, p1, p2, duration=1.0):
        y, x = self.driver.window_size()
        self.driver.long_click(p1 * x, p2 * y, duration)

    # 按坐标比例长点击
    def buttonLongClick2(self, p1, p2, duration=1.0):
        self.driver.long_click(p1, p2, duration)

    # 保存元素名称
    def nameValue(self, name):
        d = self.driver
        ele = d(text=name)
        return ele

    # 按名称点击
    def nameClick(self, name):
        self.nameValue(name).click()

    # 按名称长点击
    def nameLongClick(self, name, duration=1.0):
        self.nameValue(name).long_click(duration)

    # 设置公用xpath并设置显示等待5s
    def xpathValue(self, xpathstr, waitTime=5):
        return self.driver.xpath(xpathstr).wait(waitTime)

    # 按xpath点击按钮
    def xpathClick(self, xpathstr):
        self.xpathValue(xpathstr).click()

    # xpath长点击
    def xpathLongClick(self, xpathstr, duration=1.0):
        self.xpathValue(xpathstr).long_click(duration)

    # 按xpath获取页面元素的文本信息
    def xpathTextGet(self, xpathstr):
        # resp = XpathValue(xpathstr).text
        return self.xpathValue(xpathstr).text

    # 垂直滑动
    def verticalSwipe(self, l1, l2, l3):
        y, x = self.driver.window_size()
        # l2>l3为向上滑动，l3>l2为向下滑动
        x1 = x * l1
        y1 = y * l2
        y2 = y * l3
        self.driver.swipe(x1, y1, x1, y2)

    # 水平滑动
    def horizontalSwipe(self, l1, l2, l3):
        y, x = self.driver.window_size()
        # l1>l2为向左滑动，l2>l1为向右滑动
        x1 = x * l1
        x2 = x * l2
        y1 = y * l3
        self.driver.swipe(x1, y1, x2, y1)

    # 输入中文文本
    def sendMsg(self, string):
        d = self.driver
        d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
        d.send_keys(string)  # adb广播输入
        d.set_fastinput_ime(False)  # 切换成正常的输入法

    # # 切换小店
    # @allure.step('切换门店')
    # def storeChange(store):
    #     d = u2.connect()
    #     # 切换到第1个门店
    #     pageChange('店铺切换')
    #     time.sleep(5)
    #     xpathClick('//*[@resource-id="com.qianmi.cash:id/main_recycleView"]/android.widget.LinearLayout[1]/'
    #                'android.widget.RelativeLayout[1]')
    #     time.sleep(10)
    #     waitUpdate(12)
    #     noJiaoJie()
    #     # 切换到门店进行选择
    #     pageChange('店铺切换')
    #     time.sleep(5)
    #     for num in range(0, 10):
    #         element = d(text=store)
    #         if element.count == 0:
    #             verticalSwipe(0.384, 0.775, 0.444)
    #         elif element.count == 1:
    #             element.click()
    #             break
    #     time.sleep(10)
    #     waitUpdate(12)
    #     noJiaoJie()

    # 切换店铺
    @allure.step('店铺切换')
    def storeChange(self, store):
        d = self.driver
        # 切换到门店进行选择
        self.pageChange('店铺切换')
        for num in range(0, 10):
            element = d(text=store)
            if element.count == 0:
                self.verticalSwipe(0.384, 0.775, 0.444)
            elif element.count == 1:
                element.click()
                break
        self.waitUpdate(12)
        self.noJiaoJie()

    # 暂不升级
    def noUpdate(self):
        d = u2.connect()
        if d(text='暂不升级').exists:
            d.xpath('//*[@resource-id="com.qianmi.cash:id/upgrade_activity_update_cancel"]').click()
        else:
            print('不需要取消升级')

    # 取消交接班
    def noJiaoJie(self):
        d = self.driver
        for num in range(1, 11):
            if d(text='取消').exists:
                # buttonClick1(0.46, 0.654)
                d(text='取消').click()
                break
            else:
                time.sleep(1)
                print('等待取消交接班窗口第', num, '次')

    # 清空购物车
    def clear(self):
        self.xpathClick('//*[@resource-id="com.qianmi.cash:id/cash_list_clear"]')
        d = self.driver
        for num in range(1, 11):
            if d(text='确定').exists:
                d(text='确定').click()
                break
            else:
                time.sleep(1)
                print('等待确定第', num, '次')

    # 切换订单页
    @allure.step('页面切换')
    def pageChange(self, pagename):
        self.xpathClick('//*[@resource-id="com.qianmi.cash:id/icon_shop"]')
        time.sleep(1)
        if pagename in ["销售订单", "预约单", "退货记录"]:
            self.xpathClick('//*[@text="订单"]')
            self.xpathClick('//*[@text=' + '"' + pagename + '"' + ']')
        elif pagename in ["商品管理", "展示分类", "商品辅料", "商品备注", "库存查询", "商品入库", "库存预警", "库存盘点", "商品报损"]:
            self.xpathClick('//*[@text="商品"]')
            self.xpathClick('//*[@text=' + '"' + pagename + '"' + ']')
        elif pagename in ["会员资料", "会员账单", "积分账单", "积分设置"]:
            self.xpathClick('//*[@text="会员"]')
            self.xpathClick('//*[@text=' + '"' + pagename + '"' + ']')
        elif pagename in ["促销活动"]:
            self.xpathClick('//*[@text="营销"]')
            self.xpathClick('//*[@text=' + '"' + pagename + '"' + ']')
        elif pagename in ["交易分析", "收支概览", "商品分析", "日结记录", "交接班记录", "交易明细", "退款明细"]:
            self.xpathClick('//*[@text="数据"]')
            self.xpathClick('//*[@text=' + '"' + pagename + '"' + ']')
        elif pagename in ["收银设置", "硬件设置", "财务设置", "员工管理", "店铺切换"]:
            self.xpathClick('//*[@resource-id="com.qianmi.cash:id/class_a_recycleView"]/android.widget'
                            '.RelativeLayout[7]')
            self.xpathClick('//*[@text=' + '"' + pagename + '"' + ']')
        elif pagename in ["收银"]:
            self.xpathClick('//*[@resource-id="com.qianmi.cash:id/class_a_recycleView"]/'
                            'android.widget.RelativeLayout[1]/android.widget.TextView[2]')

    # 等待后台更新
    def waitUpdate(self, times):
        d = self.driver
        for num in range(1, times):
            if d(text='切换至后台同步').exists and num != times:
                print('第'+str(num)+'次等待后台更新')
                d.sleep(5)
            elif d(text='切换至后台同步').exists and num == times:
                print('后台更新时间过长，超过'+str(num*5-5)+'s')
                self.xpathClick('//*[@resource-id="com.qianmi.cash:id/tv_sync_data_to_background"]')
                break
            else:
                print('后台更新完成或不需要更新')
                break

    # 小店登录
    @allure.step('小店登录')
    def storeLogin(self, name, passwd, store='测试蓝卡'):
        d = self.driver
        if d(text='保存').wait(timeout=3).real == 1:
            self.xpathClick('//*[@resource-id="com.qianmi.cash:id/textview_save"]')
        d.sleep(2)
        self.xpathClick('//*[@resource-id="com.qianmi.cash:id/edittext_login_by_password_phone"]')
        d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
        d.send_keys(str(name))
        d.set_fastinput_ime(False)  # 切换成正常的输入法
        self.xpathClick('//*[@resource-id="com.qianmi.cash:id/edittext_password"]')
        d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
        d.send_keys(str(passwd))
        d.set_fastinput_ime(False)  # 切换成正常的输入法
        d.sleep(1)
        self.nameClick('登录')
        d.sleep(5)
        for num in range(0, 30):
            element = d(text=str(store))
            if element.count == 0:
                self.verticalSwipe(0.63, 0.608, 0.352)
            elif element.count == 1:
                element.click()
                break
        self.nameClick('确定')
        d.sleep(5)
        self.noUpdate()
        self.waitUpdate(12)

    # 选择小店
    def storeChoose(self, store='测试蓝卡'):
        for num in range(0, 30):
            element = self.driver(text=str(store))
            if element.count == 0:
                self.verticalSwipe(0.63, 0.608, 0.352)
            elif element.count == 1:
                element.click()
        self.nameClick('确定')

    # 判断是否是正数
    def is_positiveNumber(self, num):
        newNum = str(num)
        if newNum.count(".") == 1:  # 小数的判断
            if newNum[0] == "-":
                return False
            if newNum[0] == ".":
                return False
            newNum = newNum.replace(".", "")
            for i in newNum:
                if i not in "0123456789":
                    return False
            else:  # 这个else与for对应的
                return True
        elif newNum.count(".") == 0:  # 整数的判断
            if newNum[0] == "-":
                return False
            for i in newNum:
                if i not in "0123456789":
                    return False
            else:
                return True
        else:
            return False

    # 判断是否是正整数
    def is_positiveIntegerNumber(self, num):
        newNum = str(num)
        if newNum.count(".") == 1:  # 小数的判断
            return False
        elif newNum.count(".") == 0:  # 整数的判断
            if newNum[0] == "-":
                return False
            for i in newNum:
                if i not in "0123456789":
                    return False
            else:
                return True
        else:
            return False

    # wifi操作 operate必须填写 "开启" or "关闭"其中之一
    def wifiOperate(self, operate):
        if str(operate) in ["开启", "关闭"]:
            pass
        else:
            raise ValueError('入参不正确！')
        self.xpathClick('//*[@resource-id="com.qianmi.cash:id/icon_wifi"]')
        self.nameClick('WLAN')
        # 存取当前wifi的状态
        ele1 = self.driver(text=str(operate)).wait(1)
        # 检查当前wifi状态是否符合要做的操作
        if ele1.real:
            raise Exception('操作异常：wifi状态符合预期，无需操作')
        else:
            self.xpathClick('//*[@resource-id="com.android.settings:id/switch_widget"]')
        if str(operate) == "关闭":
            ele2 = self.driver(text='要查看可用网络，请打开WLAN。').wait(3)
            if ele2.real:
                print('无线网已关闭')
                self.driver.app_start('com.qianmi.cash')
            else:
                raise Exception('操作异常：无线网未关闭！')
        else:
            ele2 = self.driver(text='已连接').wait(3)
            if ele2.real:
                print('无线网已连接')
                self.driver.app_start('com.qianmi.cash')
            else:
                raise Exception('操作异常：无线网未关闭！')

# 等待
    def sleep(self, t):
        self.driver.sleep(t)
