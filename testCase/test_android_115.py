# from appium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
import random
import time
from com.comFunction import *


class test_Main(findFunction):
    def startTest(self):
        # alldata = [("native", "dalvik", "TOTAL", "Time")]
        # 系统弹窗
        self.findElement_ByID("com.android.packageinstaller:id/permission_allow_button").click()
        time.sleep(1)
        # 保存提醒弹窗
        # save = self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/textview_save'][@text='保存']")
        save = self.findElement_ByID("com.qianmi.cash:id/textview_save")
        # save = self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/textview_cancel'][@text='取消']")
        save.click()
        # self.tapScreenPoint(1088, 710)
        # print("guole")
        # 手机号
        phone = self.findElement_ByID("com.qianmi.cash:id/edittext_login_by_password_phone")
        phone.clear()
        phone.send_keys("18009611556")

        # 密码
        passwd = self.findElement_ByID("com.qianmi.cash:id/edittext_password")
        passwd.clear()
        passwd.send_keys("111111")

        # 登录
        bt = self.findElement_ByID("com.qianmi.cash:id/textview_login_by_password_submit")
        bt.click()

        # 选择店铺
        # 滑动弹窗元素
        store = None
        while store == None:
            try:
                store = self.findElement_ByXpath(
                    "//*[@resource-id='com.qianmi.cash:id/textview_store_name'][@text='测试蓝卡']", 1)
            except Exception:
                self.swipeByVertical(0.7, 0.2)
        store.click()

        confirm = self.findElement_ByID("com.qianmi.cash:id/textview_confirm")
        confirm.click()

        # 新人引导弹窗
        try:
            self.findElement_ByID("com.qianmi.cash:id/dialog_close_btn", 15).click()
        except Exception:
            pass

        # 关闭自动打印
        self.findElement_ByID("com.qianmi.cash:id/icon_shop").click()
        time.sleep(1)
        self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/tv_class_a_name'][@text='设置']").click()
        self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/tv_class_b_name'][@text='硬件设置']").click()
        self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/tv_device_name'][@text='内置打印机']").click()
        self.findElement_ByID("com.qianmi.cash:id/rb_auto_print_off").click()
        self.tapScreenPoint(1702, 985)
        self.findElement_ByID("com.qianmi.cash:id/cash_to_cash_btn").click()

        # # 切换单机
        # self.findElement_ByID("com.qianmi.cash:id/single_version_layout_ll").click()
        # self.findElement_ByID("com.qianmi.cash:id/cash_switch").click()
        # time.sleep(3)
        list = 0
        totalMoney = 0
        for t in range(1000):
            # 选择分类
            goodsList = self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/textview_category'][@text='新品']")
            goodsList.click()

            # 点击加购商品
            for i in range(3):
                k = random.randint(9, 16)
                goods = self.findElement_ByXpath(
                    "//android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/androidx"
                    ".recyclerview.widget.RecyclerView/android.widget.LinearLayout[" + str(
                        k) + "]/android.widget.LinearLayout")
                goods.click()
                # if k in (8, 17, 18):
                #     weightInput = self.findElement_ByID("com.qianmi.cash:id/fragment_dialog_weight_hand_et")
                #     weightInput.send_keys(str(random.randint(1, 50)))
                #     confirmWeight = self.findElement_ByID("com.qianmi.cash:id/weight_hand_confirm_tv")
                #     confirmWeight.click()
            # 结算
            toCash = self.findElement_ByID("com.qianmi.cash:id/tv_cash_to_cash")
            toCash.click()
            # 选择现金
            selCash = self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/pay_mode_name'][@text='现金付']")
            money = self.findElement_ByID("com.qianmi.cash:id/amount_receivable_tv").text.split("￥")[1]
            selCash.click()
            time.sleep(1)
            # 使用Tap坐标的方式，点击结账
            # self.tapScreenPoint(1655, 968, 1840, 990)
            self.tapScreenPoint(1715, 675, 300)
            time.sleep(1)
            self.findElement_ByID("com.qianmi.cash:id/tv_close").click()
            # time.sleep(1)
            list += 1
            print("第" + str(list) + "单，金额：" + money)
            totalMoney += float(money)
            print("总金额" + str(totalMoney))


if __name__ == "__main__":
    test_Main().startTest()
