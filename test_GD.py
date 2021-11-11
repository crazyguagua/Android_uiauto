"""
安卓收银挂单
"""
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
                    "//*[@resource-id='com.qianmi.cash:id/textview_store_name'][@text='测试蓝卡']", 4)
            except Exception:
                self.swipeByVertical(0.7, 0.2)
        store.click()

        confirm = self.findElement_ByID("com.qianmi.cash:id/textview_confirm")
        confirm.click()

        # # 切换单机
        # self.findElement_ByID("com.qianmi.cash:id/single_version_layout_ll").click()
        # self.findElement_ByID("com.qianmi.cash:id/cash_switch").click()
        # time.sleep(3)
        list = 0
        totalMoney = 0
        for t in range(1000):
            # 选择分类
            goodsList = self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/textview_category'][@text='新品']",300)
            goodsList.click()

            # 点击加购商品
            for i in range(3):
                k = random.randint(2, 6)
                goods = self.findElement_ByXpath(
                    "//*[@resource-id='com.qianmi.cash:id/recycler_goods']/android.widget.RelativeLayout[" + str(
                        k) + "]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]")
                goods.click()
            # 登录会员
            self.findElement_ByID("com.qianmi.cash:id/select_vip_tv").click()
            if self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/tv_title'][@text='选择会员']"):

                self.tapScreenPoint(1305, 887)  # num1
                self.tapScreenPoint(1443, 783)  # num5
                self.tapScreenPoint(1443, 783)  # num5
                self.tapScreenPoint(1601, 783)  # num6
                # self.tapScreenPoint(1751, 875)  # 登录
                self.findElement_ByXpath("//*[@resource-id='com.qianmi.cash:id/tv_login_nickname'][@text='大尾巴猫']").click()

            self.findElement_ByXpath(
                "//*[@resource-id='com.qianmi.cash:id/cash_bottom_bar_title_tv'][@text='挂单']").click()


if __name__ == "__main__":
    test_Main().startTest()
