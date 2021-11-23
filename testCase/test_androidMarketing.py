"""
安卓收银下单营销活动
"""
import random
import time
from com.comFunction import *
import csv


class test_Main():
    desired_caps = {"platformName": "Android",
                    "platformVersion": "7.1.1",
                    "deviceName": "T203189A40323",
                    "appPackage": "com.qianmi.cash",
                    "appActivity": "com.qianmi.cash.activity.LaunchActivity",
                    "noReset": "True"
                    }

    def startTest(self):
        # alldata = [("native", "dalvik", "TOTAL", "Time")]
        self.testAndroid = findFunction(self.desired_caps['platformName'], self.desired_caps["platformVersion"], self.desired_caps["deviceName"], self.desired_caps["appPackage"], self.desired_caps["appActivity"], self.desired_caps["noReset"])
        # 系统弹窗
        self.testAndroid.findElement_ByID("com.android.packageinstaller:id/permission_allow_button").click()
        time.sleep(1)
        # 保存提醒弹窗
        # save = self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/textview_save'][@text='保存']")
        save = self.testAndroid.findElement_ByID("com.qianmi.cash:id/textview_save")
        # save = self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/textview_cancel'][@text='取消']")
        save.click()
        # self.tapScreenPoint(1088, 710)
        # print("guole")
        # 手机号
        phone = self.testAndroid.findElement_ByID("com.qianmi.cash:id/edittext_login_by_password_phone")
        phone.clear()
        phone.send_keys("18009611556")

        # 密码
        passwd = self.testAndroid.findElement_ByID("com.qianmi.cash:id/edittext_password")
        passwd.clear()
        passwd.send_keys("111111")

        # 登录
        bt = self.testAndroid.findElement_ByID("com.qianmi.cash:id/textview_login_by_password_submit")
        bt.click()

        # 选择店铺
        # 滑动弹窗元素
        store = None
        while store == None:
            try:
                store = self.testAndroid.findElement_ByXpath(
                    "//*[@resource-id='com.qianmi.cash:id/textview_store_name'][@text='测试蓝卡']", 1)
            except Exception:
                if self.testAndroid.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/textview_title'][@text='请选择店铺']", 6):
                    self.testAndroid.swipeByVertical(0.7, 0.2)
        store.click()

        confirm = self.testAndroid.findElement_ByID("com.qianmi.cash:id/textview_confirm")
        confirm.click()
        # 等待同步商品完成
        # while self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/tv_sync_data_to_background']["
        #                                "@text='切换至后台同步']", 10):
        #     time.sleep(1)

        # # 新人引导弹窗
        # try:
        #     self.findElement_ByID("com.qianmi.cash:id/dialog_close_btn", 4).click()
        # except Exception:
        #     pass
        if self.testAndroid.findElement_ByXpath("//*[@class='android.widget.Toast']", 300).text == "同步成功":
            # 关闭自动打印
            self.testAndroid.findElement_ByID("com.qianmi.cash:id/icon_shop").click()

        time.sleep(1)
        self.testAndroid.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/tv_class_a_name'][@text='设置']").click()
        self.testAndroid.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/tv_class_b_name'][@text='硬件设置']").click()
        self.testAndroid.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/tv_device_name'][@text='内置打印机']").click()
        self.testAndroid.findElement_ByID("com.qianmi.cash:id/rb_auto_print_off").click()
        self.testAndroid.tapScreenPoint(1693, 983)
        self.testAndroid.findElement_ByID("com.qianmi.cash:id/cash_to_cash_btn").click()
        list = 0
        totalMoney = 0
        f = "线上统计时间.csv"
        while True:
            # 点击商品列表分类
            goodsList = self.testAndroid.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/textview_category'][@text='新品']",
                                                 30)
            goodsList.click()

            # 点击加购商品
            for i in range(5):
                k = random.randint(2, 6)
                goods = self.testAndroid.findElement_ByXpath(
                    "//*[@resource-id='com.qianmi.cash:id/recycler_goods']/android.widget.RelativeLayout[" + str(
                        k) + "]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]", 10)
                goods.click()

            # 结算
            toCash = self.testAndroid.findElement_ByID("com.qianmi.cash:id/tv_cash_to_cash")
            toCash.click()
            time_Start = time.time()
            self.testAndroid.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/settlement_pay_right_view']/android.widget"
                                     ".LinearLayout[1]", 10)

            # 创建订单成功用时
            time_CreateList = time.time()
            createListTime = float("%.1f" % (time_CreateList - time_Start))

            # 选择现金
            selCash = self.testAndroid.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/pay_mode_name'][@text='现金']")
            selCash.click()
            time_selectCash = time.time()
            # 选择支付方式用时
            selectCashTime = float("%.1f" % (time_selectCash - time_CreateList))
            money = self.testAndroid.findElement_ByID("com.qianmi.cash:id/amount_pending_tv").text.split("￥")[1]
            time.sleep(1)
            # 使用Tap坐标的方式，点击结账
            # self.tapScreenPoint(1655, 968, 1840, 990)
            self.testAndroid.tapScreenPoint(1718, 717, 800)
            # 点击结账时间
            time_ClickPay = time.time()
            # 选择支付方式到点击结账用时
            payCashTime = float("%.1f" % (time_ClickPay - time_CreateList))
            list += 1
            print("第" + str(list) + "单，金额：" + money)
            totalMoney += float(money)
            print("总金额" + str(float("%.2f" % totalMoney)))
            # time.sleep(2)
            try:
                self.testAndroid.findElement_ByXpath("//*[@class='android.widget.Toast']", 10)
                time_end = time.time()
                # 支付用时
                paySuccessTime = float("%.1f" % (time_end - time_ClickPay))
                # print("点击结账到结账成功用时:" + str(float('%.1f' % paySuccessTime)))
                # 点结算到支付成功总时间
                totalTime = float("%.1f" % (time_end - time_Start))
                # print("结算用时：" + str(float('%.1f' % totalTime)))
                with open(f, "a+", newline='') as file:
                    timeData = [str(createListTime), str(selectCashTime), str(payCashTime), str(paySuccessTime), str(totalTime)]
                    csv_write = csv.writer(file)
                    csv_write.writerow(timeData)
            except Exception:
                pass


if __name__ == "__main__":
    test_Main().startTest()
