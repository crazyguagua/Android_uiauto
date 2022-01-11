# coding = utf-8
import sys
from com.appBase import *


class fastSaleFunction(functionCommon):
    # 选择商品类型
    def goodsTypeSelect(self, goodstype):
        d = u2.connect()
        for num in range(0, 10):
            element = d(text=goodstype)
            if element.count == 0:
                self.horizontalSwipe(0.932, 0.834, 0.281)
            elif element.count == 1:
                element.click()
                break

    # 称重商品键盘
    def weightKeyboard(self, num):
        # 判断输入内容是否为数字
        if self.is_positiveNumber(num):
            for i in num:
                if i == '1':
                    self.buttonClick1(0.696, 0.793)
                elif i == '2':
                    self.buttonClick1(0.752, 0.786)
                elif i == '3':
                    self.buttonClick1(0.83, 0.782)
                elif i == '4':
                    self.buttonClick1(0.688, 0.679)
                elif i == '5':
                    self.buttonClick1(0.756, 0.686)
                elif i == '6':
                    self.buttonClick1(0.838, 0.683)
                elif i == '7':
                    self.buttonClick1(0.68, 0.587)
                elif i == '8':
                    self.buttonClick1(0.758, 0.587)
                elif i == '9':
                    self.buttonClick1(0.834, 0.59)
                elif i == '0':
                    self.buttonClick1(0.756, 0.893)
                elif i == '.':
                    self.buttonClick1(0.68, 0.893)
                else:
                    print('称重商品计量输入错误！！')
        else:
            raise TypeError('请输入正确的重量！！')
        # buttonClick1(0.918, 0.804)

    # 自定义收款键盘
    def customKeyboard(self, num):
        if self.is_positiveNumber(num):
            if num == 10:
                self.buttonClick1(0.656, 0.398)
            elif num == 20:
                self.buttonClick1(0.644, 0.498)
            elif num == 50:
                self.buttonClick1(0.646, 0.594)
            elif num == 100:
                self.buttonClick1(0.648, 0.704)
            else:
                for i in str(num):
                    if i == '1':
                        self.buttonClick1(0.708, 0.608)
                    elif i == '2':
                        self.buttonClick1(0.762, 0.612)
                    elif i == '3':
                        self.buttonClick1(0.812, 0.601)
                    elif i == '4':
                        self.buttonClick1(0.708, 0.501)
                    elif i == '5':
                        self.buttonClick1(0.758, 0.498)
                    elif i == '6':
                        self.buttonClick1(0.824, 0.508)
                    elif i == '7':
                        self.buttonClick1(0.712, 0.391)
                    elif i == '8':
                        self.buttonClick1(0.768, 0.395)
                    elif i == '9':
                        self.buttonClick1(0.818, 0.395)
                    elif i == '0':
                        self.buttonClick1(0.766, 0.704)
                    elif i == '.':
                        self.buttonClick1(0.712, 0.69)
                    else:
                        print('自定义价格输入错误！！')
                        sys.exit()
        else:
            raise TypeError('请输入正确的收款金额！！')

    # 现金收款键盘
    def cashKeyboard(self, num):
        # 判断输入是否为整数
        if self.is_positiveNumber(num):
            if num == 10:
                self.buttonClick1(0.644, 0.462)
            elif num == 20:
                self.buttonClick1(0.644, 0.565)
            elif num == 50:
                self.buttonClick1(0.648, 0.658)
            elif num == 100:
                self.buttonClick1(0.656, 0.743)
            else:
                for i in str(num):
                    if i == '1':
                        self.buttonClick1(0.702, 0.658)
                    elif i == '2':
                        self.buttonClick1(0.76, 0.651)
                    elif i == '3':
                        self.buttonClick1(0.816, 0.658)
                    elif i == '4':
                        self.buttonClick1(0.704, 0.555)
                    elif i == '5':
                        self.buttonClick1(0.764, 0.551)
                    elif i == '6':
                        self.buttonClick1(0.824, 0.544)
                    elif i == '7':
                        self.buttonClick1(0.7, 0.466)
                    elif i == '8':
                        self.buttonClick1(0.76, 0.451)
                    elif i == '9':
                        self.buttonClick1(0.82, 0.459)
                    elif i == '0':
                        self.buttonClick1(0.772, 0.747)
                    elif i == '.':
                        self.buttonClick1(0.712, 0.747)
                    else:
                        print('现金收款价格输入错误！！')
        else:
            raise TypeError('请输入正确的收款金额！！')

    # 快速收款键盘
    def fastPayKeyboard(self, num):
        if self.is_positiveIntegerNumber(num):
            self.xpathClick('//*[@text="快速收款"]')
            if num == 10:
                self.buttonClick1(0.584, 0.53)
            elif num == 20:
                self.buttonClick1(0.592, 0.622)
            elif num == 50:
                self.buttonClick1(0.58, 0.729)
            elif num == 100:
                self.buttonClick1(0.592, 0.836)
            else:
                for i in str(self, num):
                    if i == '1':
                        self.buttonClick1(0.64, 0.743)
                    elif i == '2':
                        self.buttonClick1(0.704, 0.729)
                    elif i == '3':
                        self.buttonClick1(0.742, 0.743)
                    elif i == '4':
                        self.buttonClick1(0.64, 0.647)
                    elif i == '5':
                        self.buttonClick1(0.704, 0.637)
                    elif i == '6':
                        self.buttonClick1(0.758, 0.64)
                    elif i == '7':
                        self.buttonClick1(0.64, 0.544)
                    elif i == '8':
                        self.buttonClick1(0.7, 0.548)
                    elif i == '9':
                        self.buttonClick1(0.76, 0.54)
                    elif i == '0':
                        self.buttonClick1(0.688, 0.836)
                    elif i == '.':
                        self.buttonClick1(0.65, 0.836)
                    else:
                        print('快速收款价格输入错误！！')
        else:
            raise TypeError('请输入正确的收款金额！！')

    # 会员登录键盘
    def vipKeyboard(self, num):
        if self.is_positiveIntegerNumber(num):
            for i in str(num):
                if i == '1':
                    self.buttonClick1(0.672, 0.836)
                elif i == '2':
                    self.buttonClick1(0.756, 0.822)
                elif i == '3':
                    self.buttonClick1(0.84, 0.818)
                elif i == '4':
                    self.buttonClick1(0.676, 0.729)
                elif i == '5':
                    self.buttonClick1(0.762, 0.736)
                elif i == '6':
                    self.buttonClick1(0.842, 0.729)
                elif i == '7':
                    self.buttonClick1(0.688, 0.629)
                elif i == '8':
                    self.buttonClick1(0.766, 0.615)
                elif i == '9':
                    self.buttonClick1(0.824, 0.626)
                elif i == '0':
                    self.buttonClick1(0.764, 0.932)
                # elif i == '.':
                #     buttonClick1(0.68, 0.921)
                else:
                    raise TypeError('未输入纯数字！！')
            self.buttonClick1(0.906, 0.814)
        else:
            raise TypeError('请输入正整数！！')

    # 会员号码登录
    @allure.step('会员登录')
    def vipLoginNum(self, cardNo):
        self.xpathClick('//*[@resource-id="com.qianmi.cash:id/select_vip_tv"]')
        self.xpathClick('//*[@resource-id="com.qianmi.cash:id/cash_right_frame"]'
                   '/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]')
        self.vipKeyboard(self, cardNo)
        for num in range(1, 10):
            ele = self.driver(textContains=str(cardNo))
            if ele.exists:
                print('登录会员成功')
                break
            else:
                print('尚未登录继续等待')
                time.sleep(1)

    # 会员昵称登录
    @allure.step('会员登录')
    def vipLoginName(self, vipName):
        self.nameClick('点击选择会员')
        self.nameClick('切换键盘')
        self.sendMsg(vipName)
        if self.driver(text=vipName).count == 2:
            self.buttonClick1(0.692, 0.302)
            for i in range(1, 5):
                if self.driver(textContains=vipName).count == 1:
                    print('登录成功')
                    break
                else:
                    time.sleep(2)
        else:
            raise ValueError('会员查询异常，请检查会员昵称orNum！！')


