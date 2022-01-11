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

import pytest
# from pytest import assume
from com.fastSale import *

IP = 'T203189A40323'
@pytest.fixture(scope='class')
def driver(IP):
    return openCommon(IP)

@allure.epic('茶饮模块'.center(30, '*'))
@allure.suite('茶饮下单主流程')
class TestNormal:
    @pytest.mark.parametrize("driver", IP)
    @pytest.mark.usefixtures("appInit")
    # @pytest.mark.skip
    @allure.feature('标准商品')
    @allure.story('未开启组合支付')
    @allure.title('TC_未开启组合支付_001')
    # @allure.title('TC_按数量下单_001')
    @allure.description('加购商品下单，微信扫码付，收银成功')
    # @allure.testcase('测试用例地址（暂时不用）:http://172.19.32.234:8081/#/track/case/all')
    @allure.tag('用例负责人：周成志')
    @allure.step('测试脚本主体')
    @allure.severity('critical')
    def test_未开启组合支付_001(self, driver):
        self.sleep(3)
        driver.storeChange("测试蓝卡")
        self.sleep(1)
        # 选中商品
        driver.buttonClick1(0.62, 0.37)
        print('1.选中商品')
        self.sleep(1)
        # 点击结算
        driver.xpathClick('//*[@resource-id="com.qianmi.cash:id/tv_cash_to_cash"]')
        print('2.点击结算')
        self.sleep(1)
        # 选择现金支付
        driver.xpathClick('//*[@resource-id="com.qianmi.cash:id/layout_pay_mode" and @index="1"]')
        self.sleep(1)
        print('3.选择现金支付')
        # 点击结账
        driver.buttonClick1(0.89, 0.66)
        print('4.点击结账成功')
        self.sleep(2)

        # 切换订单页
        # 点击云小店
        driver.xpathClick('//*[@resource-id="com.qianmi.cash:id/icon_shop"]')
        self.sleep(1)
        # 点击订单
        driver.xpathClick('//*[@resource-id="com.qianmi.cash:id/class_a_recycleView"]/android.widget.RelativeLayout[3]')
        self.sleep(1)
        # 点击销售订单
        driver.xpathClick('//*[@resource-id="com.qianmi.cash:id/class_b_recycleView"]/android.widget.RelativeLayout[1]')
        print('5.切换到订单页')
        self.sleep(1)

        # # 检查订单
        # # 获取首单状态
        # status = self.xpathTextGet('//*[@resource-id="com.qianmi.cash:id/recyclerview_order"]/android'
        #                            '.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android'
        #                            '.widget.LinearLayout[2]/android.widget.TextView[1]')
        #
        # assert (status == "已完成"), "订单状态非已完成，用例失败"
        # # 检查金额
        # price = self.xpathTextGet('//*[@resource-id="com.qianmi.cash:id/recyclerview_order"]/android.'
        #                           'widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.'
        #                           'LinearLayout[1]/android.widget.TextView[1]')
        # assert (price == "¥23.62"), "金额错误，用例失败"
        # print("确认结果：商品订单已完成！")
        #
        # self.sleep(2)
        #
        # # 切换收银页
        # # 点击云小店
        # self.xpathClick('//*[@resource-id="com.qianmi.cash:id/icon_shop"]')
        # self.sleep(1)
        # # 点击订单
        # self.xpathClick('//*[@resource-id="com.qianmi.cash:id/class_a_recycleView"]/android.widget.RelativeLayout[1]')
        # print("6.切换回收银页")
        # print("7.下单流程结束")
        # print("测试流程结束")

    # @pytest.mark.usefixtures("start")
    # # @pytest.mark.skip
    # @allure.feature('基础流程')
    # @allure.story('单位：件 下单收银：TC_按数量下单_002')
    # @allure.title('TC_按数量下单_002')
    # @allure.description('计件下单，现金支付')
    # @allure.testcase('测试用例地址:http://172.19.32.234:8081/#/track/case/all')
    # @allure.tag('单位 件 下单结算')
    # @allure.step('单位 件 单结算流程')
    # @allure.severity('critical')
    # def test_jiJianXiaDan(self):
    #     self.sleep(3)
    #     self.storeChange("测试蓝卡")
    #     self.sleep(1)
    #     # 添加2件商品
    #     self.buttonClick1(0.756, 0.43)
    #     self.sleep(0.5)
    #     self.xpathClick('//*[@resource-id="com.qianmi.cash:id/cash_list_rv"]/android.widget.'
    #                     'LinearLayout[1]/android.view.ViewGroup[1]/android.widget.LinearLayout[1]/'
    #                     'android.widget.LinearLayout[3]/android.widget.TextView[3]')
    #     print('1.选中商品增加为两件')
    #     self.sleep(1)
    #     # 点击结算
    #     self.xpathClick('//*[@resource-id="com.qianmi.cash:id/tv_cash_to_cash"]')
    #     print('2.点击结算')
    #     self.sleep(1)
    #     # 选择现金支付
    #     self.xpathClick('//*[@resource-id="com.qianmi.cash:id/layout_pay_mode" and @index="1"]')
    #     self.sleep(1)
    #     print('3.选择现金支付')
    #     # 点击结账
    #     self.buttonClick1(0.89, 0.66)
    #     print('4.点击结账成功')
    #     self.sleep(2)
    #
    #     # 切换订单页
    #     # 点击云小店
    #     self.xpathClick('//*[@resource-id="com.qianmi.cash:id/icon_shop"]')
    #     self.sleep(1)
    #     # 点击订单
    #     self.xpathClick('//*[@resource-id="com.qianmi.cash:id/class_a_recycleView"]/android.widget.RelativeLayout[3]')
    #     self.sleep(1)
    #     # 点击销售订单
    #     self.xpathClick('//*[@resource-id="com.qianmi.cash:id/class_b_recycleView"]/android.widget.RelativeLayout[1]')
    #     print('5.切换到订单页')
    #     self.sleep(1)
    #
    #     # 检查订单
    #     # 获取首单状态
    #     status = self.xpathTextGet('//*[@resource-id="com.qianmi.cash:id/recyclerview_order"]/android'
    #                                '.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android'
    #                                '.widget.LinearLayout[2]/android.widget.TextView[1]')
    #
    #     assert (status == "已完成"), "订单状态非已完成，用例失败"
    #     # 检查金额
    #     price = self.xpathTextGet('//*[@resource-id="com.qianmi.cash:id/recyclerview_order"]/android.'
    #                               'widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.'
    #                               'LinearLayout[1]/android.widget.TextView[1]')
    #     assert (price == "¥36"), "金额错误，用例失败"
    #     print("确认结果：商品订单已完成！")
    #
    #     self.sleep(2)
    #
    #     # 切换收银页
    #     # 点击云小店
    #     self.xpathClick('//*[@resource-id="com.qianmi.cash:id/icon_shop"]')
    #     self.sleep(1)
    #     # 点击订单项
    #     self.xpathClick('//*[@resource-id="com.qianmi.cash:id/class_a_recycleView"]/android.widget.RelativeLayout[1]')
    #     print("6.切换回收银页")
    #     print("7.下单流程结束")
    #     print("测试流程结束")


if __name__ == '__main__':
    os.system("pytest --reruns 2 ./test_UI2.py  --alluredir=./report --clean-alluredir")
