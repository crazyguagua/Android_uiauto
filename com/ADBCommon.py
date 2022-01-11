#!/usr/bin/env python

# -*- coding: utf-8 -*-

# FileName ADBCommon.py
# Author: Orangecat
# Created Time: 2020/04/01
u"""
adb 工具类
"""

import os
import platform
import re
import time


class ADBTools(object):
    # 初始化方法
    def __init__(self, device_id=''):
        # 定义当前系统类型 windows/linux/ios
        self.__system = platform.system()
        # 定义find内容为空，后续运用__get_find赋值
        self.__find = ''
        # 定义command具体内容，后续运用
        self.__command = ''
        # 定义设备id
        self.__device_id = device_id
        # 执行__get_find方法，定义__find具体内容
        self.__get_find()
        # 调用__check_adb方法检查当前环境变量是否设置，并添加内容
        self.__check_adb()
        # 调用预设方法通过device_id连接设备
        self.__connection_devices()

    # 定义get_find方法，确认__find的值
    def __get_find(self):
        """
        判断系统类型，windows使用findstr，linux使用grep
        :return:
        """
        if self.__system == "Windows":
            self.__find = "findstr"
        else:
            self.__find = "grep"

    def __check_adb(self):
        """
        检查adb判断是否设置环境变量ANDROID_HOME，未设置则报错提示
        :return:
        """
        # 在当前系统环境变量中找到了ANDROID_HOME
        if "ANDROID_HOME" in os.environ:
            # 判断当前系统为windows，走入下列分支
            if self.__system == "Windows":
                # 自定义path变量值，待下一步判断环境变量path中是否已设置*\platform-tools\adb.exe
                path = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb.exe")
                # 判断当前系统环境变量path中是否已设置 *\platform - tools\adb.exe
                if os.path.exists(path):
                    # path存在，将path赋值到__command中
                    self.__command = path
                # path不存在,报错提示检查PATH变量是否已添加*\platform-tools\adb.exe
                else:
                    raise EnvironmentError("%s\\platform-tools\\adb.exe is not in environ.PATH, Pls check!" % os.environ["ANDROID_HOME"])
            # 现在用的是本机安装的adb,指向环境变量设置的路径,没有在工程中另外放置adb
            # if self.__system == "Windows":
            #     self.__command = os.path.join(".\\", "Windows\\", "adb.exe")
            # 当前系统为Linux的时候
            elif self.__system == "Linux":
                path = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
                if os.path.exists(path):
                    self.__command = path
                else:
                    raise EnvironmentError(
                        "%s\\platform-tools\\adb is not in environ.PATH, Pls check!" % os.environ["ANDROID_HOME"])
            # 暂定为IOS "Darwin"
            else:
                # 直接定位到当前工程给出的mac\adb工具,相对路径
                self.__command = os.path.join(".", "Mac/", "adb")
        # 在当前系统环境变量中未找到ANDROID_HOME,报错提示添加
        else:
            raise EnvironmentError(
                "Can not found $ANDROID_HOME right here in environ, pls add right now!")

    def __connection_devices(self):
        """
        连接指定设备，单个设备可不传device_id，不影响后续拼接adb命令
        :return:
        """
        # 没指定device_id的时候，为空字符串
        if self.__device_id == "":
            return
        # 指定device_id的时候，为“-s device_id”
        self.__device_id = "-s %s" % self.__device_id

    def adb(self, args):
        """
        执行adb命令的方法，args为adb的参数内容
        """
        # 拼接为adb命令
        cmd = "%s %s %s" % (self.__command, self.__device_id, args)
        # 使用os.popen执行
        return cmd
        # return os.popen(cmd)

    # shell方法，同上
    def shell(self, args):
        u"""
        执行adb shell命令 args为adb的参数内容
        """
        cmd = "%s %s shell %s" % (self.__command, self.__device_id, args)
        # print(cmd)
        return os.popen(cmd)

    # 创建文件夹
    def mkdir(self, path):
        """
        创建目录:param path: 路径
        """
        return self.shell('mkdir %s' % path)

    def get_devices(self):
        u"""
        获取设备列表
        :return:
        """
        devicesList = self.adb('devices').readlines()
        # print(devicesList)
        return (i.split()[0] for i in devicesList if 'devices' not in i and len(i) > 5)

    def get_current_application(self):
        u"""
        获取当前运行的应用信息
        """
        # mSurface = Surface(name=com.qianmi.cash / com.qianmi.cash.activity.MainActivity)
        # 原文是\/，也不会执行错误，这里为了美观改成了\\/
        application = self.shell('dumpsys window w | %s \\/ | %s name=' % (self.__find, self.__find)).read()
        return application

    def get_current_package(self):
        u"""
        获取当前运行app包名
        :return:
        """
        # reg = re.compile(r'name=(.+?)/')
        reg = re.compile(r'name=(.+?)/')
        return re.findall(reg, self.get_current_application())[0]

    def get_current_activity(self):
        u"""
        获取当前运行activity
        :return: package/activity
        """
        reg = re.compile(r'name=(.+?)\)')
        return re.findall(reg, self.get_current_application())[0]

    def __get_process(self, package_name):
        u"""
        获取进程信息
        :param package_name:
        :return:
        """
        if self.__system == "Windows":
            pid_command = self.shell("ps | %s %s$" % (self.__find, package_name)).read()
        else:
            pid_command = self.shell("ps | %s -w %s" % (self.__find, package_name)).read()
        return pid_command

    def process_exists(self, package_name):
        u"""
        返回进程是否存在
        :param package_name:
        :return:
        """
        process = self.__get_process(package_name)
        return package_name in process

    def get_pid(self, package_name):
        u"""
        获取pid
        :return:
        """
        pid_command = self.__get_process(package_name)
        if pid_command == '':
            print("The process doesn't exist.")
            return pid_command

        req = re.compile(r"\d+")
        result = str(pid_command).split()
        result.remove(result[0])
        return req.findall(" ".join(result))[0]

    def get_uid(self, pid):
        u"""
        获取uid
        :param pid:
        :return:
        """
        result = self.shell("cat /proc/%s/status" % pid).readlines()
        for i in result:
            if 'uid' in i.lower():
                return i.split()[1]

    def get_flow_data_tcp(self, uid):
        u"""
        获取应用tcp流量
        :return:(接收, 发送)
        """
        tcp_rcv = self.shell("cat proc/uid_stat/%s/tcp_rcv" % uid).read().split()[0]
        tcp_snd = self.shell("cat proc/uid_stat/%s/tcp_snd" % uid).read().split()[0]
        return tcp_rcv, tcp_snd

    def get_flow_data_all(self, uid):
        u"""
        获取应用流量全部数据
        包含该应用多个进程的所有数据 tcp udp等
        (rx_bytes, tx_bytes) >> (接收, 发送)
        :param uid:
        :return:list(dict)
        """
        all_data = []
        d = {}
        data = self.shell("cat /proc/net/xt_qtaguid/stats | %s %s" % (self.__find, uid)).readlines()
        for i in data:
            if not i.startswith('\n'):
                item = i.strip().split()
                d['idx'] = item[0]
                d['iface'] = item[1]
                d['acct_tag_hex'] = item[2]
                d['uid_tag_int'] = item[3]
                d['cnt_set'] = item[4]
                d['rx_bytes'] = item[5]
                d['rx_packets'] = item[6]
                d['tx_bytes'] = item[7]
                d['tx_packets'] = item[8]
                d['rx_tcp_bytes'] = item[9]
                d['rx_tcp_packets'] = item[10]
                d['rx_udp_bytes'] = item[11]
                d['rx_udp_packets'] = item[12]
                d['rx_other_bytes'] = item[13]
                d['rx_other_packets'] = item[14]
                d['tx_tcp_bytes'] = item[15]
                d['tx_tcp_packets'] = item[16]
                d['tx_udp_bytes'] = item[17]
                d['tx_udp_packets'] = item[18]
                d['tx_other_bytes'] = item[19]
                d['tx_other_packets'] = item[20]

                all_data.append(d)
                d = {}
        return all_data

    @staticmethod
    def dump_apk(path):
        u"""
        dump apk文件
        :param path: apk路径
        :return:
        """
        # 检查build-tools是否添加到环境变量中
        # 需要用到里面的aapt命令
        l = os.environ['PATH'].split(';')
        build_tools = False
        for i in l:
            if 'build-tools' in i:
                build_tools = True
        if not build_tools:
            raise EnvironmentError("ANDROID_HOME BUILD-TOOLS COMMAND NOT FOUND.\nPlease set the environment variable.")
        return os.popen('aapt dump badging %s' % (path,))

    @staticmethod
    def dump_xml(path, filename):
        u"""
        dump apk xml文件
        :return:
        """
        return os.popen('aapt dump xmlstrings %s %s' % (path, filename))

    def uiautomator_dump(self):
        u"""
        获取屏幕uiautomator xml文件
        :return:
        """
        return self.shell('uiautomator dump').read().split()[-1]

    def pull(self, source, target):
        u"""
        从手机端拉取文件到电脑端
        :return:
        """
        self.adb('pull %s %s' % (source, target))


    def push(self, source, target):
        u"""
        从电脑端推送文件到手机端
        :param source:
        :param target:
        :return:
        """
        self.adb('push %s %s' % (source, target))

    def remove(self, path):
        u"""
        从手机端删除文件
        :return:
        """
        self.shell('rm %s' % (path,))

    def clear_app_data(self, package):
        u"""
        清理应用数据
        :return:
        """
        self.shell('pm clear %s' % (package,))

    def install(self, path):
        u"""
        安装apk文件
        :return:
        """
        # adb install 安装错误常见列表
        errors = {'INSTALL_FAILED_ALREADY_EXISTS': u'程序已经存在',
                  'INSTALL_DEVICES_NOT_FOUND': u'找不到设备',
                  'INSTALL_FAILED_DEVICE_OFFLINE': u'设备离线',
                  'INSTALL_FAILED_INVALID_APK': u'无效的APK',
                  'INSTALL_FAILED_INVALID_URI': u'无效的链接',
                  'INSTALL_FAILED_INSUFFICIENT_STORAGE': u'没有足够的存储空间',
                  'INSTALL_FAILED_DUPLICATE_PACKAGE': u'已存在同名程序',
                  'INSTALL_FAILED_NO_SHARED_USER': u'要求的共享用户不存在',
                  'INSTALL_FAILED_UPDATE_INCOMPATIBLE': u'版本不能共存',
                  'INSTALL_FAILED_SHARED_USER_INCOMPATIBLE': u'需求的共享用户签名错误',
                  'INSTALL_FAILED_MISSING_SHARED_LIBRARY': u'需求的共享库已丢失',
                  'INSTALL_FAILED_REPLACE_COULDNT_DELETE': u'需求的共享库无效',
                  'INSTALL_FAILED_DEXOPT': u'dex优化验证失败',
                  'INSTALL_FAILED_DEVICE_NOSPACE': u'手机存储空间不足导致apk拷贝失败',
                  'INSTALL_FAILED_DEVICE_COPY_FAILED': u'文件拷贝失败',
                  'INSTALL_FAILED_OLDER_SDK': u'系统版本过旧',
                  'INSTALL_FAILED_CONFLICTING_PROVIDER': u'存在同名的内容提供者',
                  'INSTALL_FAILED_NEWER_SDK': u'系统版本过新',
                  'INSTALL_FAILED_TEST_ONLY': u'调用者不被允许测试的测试程序',
                  'INSTALL_FAILED_CPU_ABI_INCOMPATIBLE': u'包含的本机代码不兼容',
                  'CPU_ABIINSTALL_FAILED_MISSING_FEATURE': u'使用了一个无效的特性',
                  'INSTALL_FAILED_CONTAINER_ERROR': u'SD卡访问失败',
                  'INSTALL_FAILED_INVALID_INSTALL_LOCATION': u'无效的安装路径',
                  'INSTALL_FAILED_MEDIA_UNAVAILABLE': u'SD卡不存在',
                  'INSTALL_FAILED_INTERNAL_ERROR': u'系统问题导致安装失败',
                  'INSTALL_PARSE_FAILED_NO_CERTIFICATES': u'文件未通过认证 >> 设置开启未知来源',
                  'INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES': u'文件认证不一致 >> 先卸载原来的再安装',
                  'INSTALL_FAILED_INVALID_ZIP_FILE': u'非法的zip文件 >> 先卸载原来的再安装',
                  'INSTALL_CANCELED_BY_USER': u'需要用户确认才可进行安装',
                  'INSTALL_FAILED_VERIFICATION_FAILURE': u'验证失败 >> 尝试重启手机',
                  'DEFAULT': u'未知错误'
                  }
        print('Installing...')
        l = self.adb('install -r %s' % (path,)).read()
        if 'Success' in l:
            print('Install Success')
        if 'Failure' in l:
            reg = re.compile('\\[(.+?)\\]')
            key = re.findall(reg, l)[0]
            try:
                print('Install Failure >> %s' % errors[key])
            except KeyError:
                print('Install Failure >> %s' % key)
        return l

    def uninstall(self, package):
        u"""
        卸载apk
        :param package: 包名
        :return:
        """
        print('Uninstalling...')
        l = self.adb('uninstall %s' % (package,)).read()
        print(l)

    def screenshot(self, target_path: object = '') -> object:
        u"""
        手机截图
        :param target_path: 目标路径
        :return:
        """
        format_time = time.strftime("%Y%m%d%H%M%S", time.localtime())

        self.shell('screencap -p /sdcard/%s.png' % str(format_time))
        time.sleep(1)
        if target_path == '':
            self.pull('/sdcard/%s.png' % (format_time), os.path.expanduser('~'))
        else:
            self.pull('/sdcard/%s.png' % (format_time), target_path)
        time.sleep(2)
        self.remove('/sdcard/%s.png' % (format_time))

    def get_cache_logcat(self):
        u"""
        导出缓存日志
        :return:
        """
        return self.adb('logcat -v time -d')

    def get_crash_logcat(self):
        u"""
        导出崩溃日志
        :return:
        """
        return self.adb('logcat -v time -d | %s AndroidRuntime' % (self.__find,))

    def clear_cache_logcat(self):
        u"""
        清理缓存区日志
        :return:
        """
        self.adb('logcat -c')

    def get_device_time(self):
        u"""
        获取设备时间
        :return:
        """
        return self.shell('date').read().strip()

    def ls(self, command):
        u"""
        shell ls命令
        :return:
        """
        return self.shell('ls %s' % (command,)).readlines()

    def file_exists(self, target):
        u"""
        判断文件在目标路径是否存在
        :return:
        """
        l = self.ls(target)
        for i in l:
            if i.strip() == target:
                return True
        return False

    def is_install(self, target_app):
        u"""
        判断目标app在设备上是否已安装
        :param target_app: 目标app包名
        :return: bool
        """
        return target_app in self.shell('pm list packages %s' % (target_app,)).read()

    def get_device_model(self):
        u"""
        获取设备型号
        :return:
        """
        return self.shell('getprop ro.product.model').read().strip()

    def get_device_id(self):
        u"""
        获取设备id
        :return:
        """
        return self.adb('get-serialno').read().strip()

    def get_device_android_version(self):
        u"""
        获取设备Android版本
        :return:
        """
        return self.shell('getprop ro.build.version.release').read().strip()

    def get_device_sdk_version(self):
        u"""
        获取设备SDK版本
        :return:
        """
        return self.shell('getprop ro.build.version.sdk').read().strip()

    def get_device_mac_address(self):
        u"""
        获取设备MAC地址
        :return:
        """
        return self.shell('cat /sys/class/net/wlan0/address').read().strip()

    def get_device_ip_address(self):
        u"""
        获取设备IP地址
        pass: 适用WIFI 蜂窝数据
        :return:
        """
        if not self.get_wifi_state() and not self.get_data_state():
            return
        l = self.shell('ip addr | %s global' % self.__find).read()
        reg = re.compile('\d+\.\d+\.\d+\.\d+')
        return re.findall(reg, l)[0]

    def get_device_imei(self):
        u"""
        获取设备IMEI
        :return:
        """
        sdk = self.get_device_sdk_version()
        # Android 5.0以下方法
        if int(sdk) < 21:
            l = self.shell('dumpsys iphonesubinfo').read()
            reg = re.compile('[0-9]{15}')
            return re.findall(reg, l)[0]
        elif self.root():
            l = self.shell('service call iphonesubinfo 1').read()
            print(l)
            print(re.findall(re.compile("'.+?'"), l))
            imei = ''
            for i in re.findall(re.compile("'.+?'"), l):
                imei += i.replace('.', '').replace("'", '').replace(' ', '')
            return imei
        else:
            print('The device not root.')
            return ''

    def check_sim_card(self):
        u"""
        检查设备SIM卡
        :return:
        """
        return len(self.shell('getprop | %s gsm.operator.alpha]' % self.__find).read().strip().split()[-1]) > 2

    def get_device_operators(self):
        u"""
        获取运营商
        :return:
        """
        return self.shell('getprop | %s gsm.operator.alpha]' % self.__find).read().strip().split()[-1]

    def get_device_state(self):
        u"""
        获取设备状态
        :return:
        """
        return self.adb('get-state').read().strip()

    def get_display_state(self):
        u"""
        获取屏幕状态
        :return: 亮屏/灭屏
        """
        l = self.shell('dumpsys power').readlines()
        for i in l:
            if 'mScreenOn=' in i:
                return i.split()[-1] == 'mScreenOn=true'
            if 'Display Power' in i:
                return 'ON' in i.split('=')[-1].upper()

    def get_screen_normal_size(self):
        u"""
        获取设备屏幕分辨率 >> 标配
        :return:
        """
        return self.shell('wm size').read().strip().split()[-1].split('x')

    def get_screen_reality_size(self):
        u"""
        获取设备屏幕分辨率 >> 实际分辨率
        :return:
        """
        x = 0
        y = 0
        l = self.shell(r'getevent -p | %s -e "0"' % self.__find).readlines()
        for n in l:
            if len(n.split()) > 0:
                if n.split()[0] == '0035':
                    x = int(n.split()[7].split(',')[0])
                elif n.split()[0] == '0036':
                    y = int(n.split()[7].split(',')[0])
        return x, y

    def get_device_interior_sdcard(self):
        u"""
        获取内部SD卡空间
        :return: (path,total,used,free,block)
        """
        return self.shell('df | %s \/mnt\/shell\/emulated' % self.__find).read().strip().split()

    def get_device_external_sdcard(self):
        u"""
        获取外部SD卡空间
        :return: (path,total,used,free,block)
        """
        return self.shell('df | %s \/storage' % self.__find).read().strip().split()

    def __fill_rom(self, path, stream, count):
        u"""
        填充数据
        :param path: 填充地址
        :param stream: 填充流大小
        :param count: 填充次数
        :return:
        """
        self.shell('dd if=/dev/zero of=%s bs=%s count=%s' % (path, stream, count)).read().strip()

    def fill_interior_sdcard(self, filename, size):
        u"""
        填充内置SD卡
        :param filename: 文件名
        :param size: 填充大小，单位byte
        :return:
        """
        if size > 10485760:  # 10m
            self.__fill_rom('sdcard/%s' % filename, 10485760, size / 10485760)
        else:
            self.__fill_rom('sdcard/%s' % filename, size, 1)

    def fill_external_sdcard(self, filename, size):
        u"""
        填充外置SD卡
        :param filename: 文件名
        :param size: 填充大小，单位byte
        :return:
        """
        path = self.get_device_external_sdcard()[0]
        if size > 10485760:  # 10m
            self.__fill_rom('%s/%s' % (path, filename), 10485760, size / 10485760)
        else:
            self.__fill_rom('%s/%s' % (path, filename), size, 1)

    def kill_process(self, pid):
        u"""
        杀死进程
        pass: 一般需要权限不推荐使用
        :return:
        """
        return self.shell('kill %s' % pid).read().strip()

    def quit_app(self, package):
        u"""
        退出应用
        :return:
        """
        return self.shell('am force-stop %s' % package).read().strip()

    def reboot(self):
        u"""
        重启设备
        :return:
        """
        self.adb('reboot')

    def recovery(self):
        u"""
        重启设备并进入recovery模式
        :return:
        """
        self.adb('reboot recovery')

    def fastboot(self):
        u"""
        重启设备并进入fastboot模式
        :return:
        """
        self.adb('reboot bootloader')

    def root(self):
        u"""
        获取root状态
        :return:
        """
        return 'not found' not in self.shell('su -c ls -l /data/').read().strip()

    def wifi(self, power):
        u"""
        开启/关闭wifi
        pass: 需要root权限
        :return:
        """
        if not self.root():
            print('The device not root.')
            return
        if power:
            self.shell('su -c svc wifi enable').read().strip()
        else:
            self.shell('su -c svc wifi disable').read().strip()

    def data(self, power):
        u"""
        开启/关闭蜂窝数据
        pass: 需要root权限
        :return:
        """
        if not self.root():
            print('The device not root.')
            return
        if power:
            self.shell('su -c svc data enable').read().strip()
        else:
            self.shell('su -c svc data disable').read().strip()

    def get_wifi_state(self):
        u"""
        获取WiFi连接状态
        :return:
        """
        return 'enabled' in self.shell('dumpsys wifi | %s ^Wi-Fi' % self.__find).read().strip()

    def get_data_state(self):
        u"""
        获取移动网络连接状态
        :return:
        """
        return '2' in self.shell('dumpsys telephony.registry | %s mDataConnectionState' % self.__find).read().strip()

    def get_network_state(self):
        u"""
        设备是否连上互联网
        :return:
        """
        return 'unknown host' not in self.shell('ping -w 1 www.baidu.com').read().strip()

    def get_wifi_password_list(self):
        u"""
        获取WIFI密码列表
        :return:
        """
        if not self.root():
            print('The device not root.')
            return []
        l = re.findall(re.compile('ssid=".+?"\s{3}psk=".+?"'), self.shell('su -c cat /data/misc/wifi/*.conf').read())
        return [re.findall(re.compile('".+?"'), i) for i in l]

    def call(self, number):
        u"""
        拨打电话
        :param number:
        :return:
        """
        self.shell('am start -a android.intent.action.CALL -d tel:%s' % number)

    def open_url(self, url):
        u"""
        打开网页
        :return:
        """
        self.shell('am start -a android.intent.action.VIEW -d %s' % url)

    def start_application(self, component):
        u"""
        启动一个应用
        e.g: com.android.settings/com.android.settings.Settings
        """
        self.shell("am start -n %s" % component)

    def send_keyevent(self, keycode):
        u"""
        发送一个按键事件
        https://developer.android.com/reference/android/view/KeyEvent.html
        :return:
        """
        self.shell('input keyevent %s' % keycode)

    def rotation_screen(self, param):
        u"""
        旋转屏幕
        :param param: 0 >> 纵向，禁止自动旋转; 1 >> 自动旋转
        :return:
        """
        self.shell('/system/bin/content insert --uri content://settings/system --bind '
                   'name:s:accelerometer_rotation --bind value:i:%s' % param)

    def instrument(self, command):
        u"""
        启动instrument app
        :param command: 命令
        :return:
        """
        return self.shell('am instrument %s' % command).read()

    def export_apk(self, package, target_path='', timeout=5000):
        u"""
        从设备导出应用
        :param timeout: 超时时间
        :param target_path: 导出后apk存储路径
        :param package: 包名
        :return:
        """
        num = 0
        if target_path == '':
            self.adb('pull /data/app/%s-1/base.apk %s' % (package, os.path.expanduser('~')))
            while 1:
                num += 1
                if num <= timeout:
                    if os.path.exists(os.path.join(os.path.expanduser('~'), 'base.apk')):
                        os.rename(os.path.join(os.path.expanduser('~'), 'base.apk'),
                                  os.path.join(os.path.expanduser('~'), '%s.apk' % package))

        else:
            self.adb('pull /data/app/%s-1/base.apk %s' % (package, target_path))
            while 1:
                num += 1
                if num <= timeout:
                    if os.path.exists(os.path.join(os.path.expanduser('~'), 'base.apk')):
                        os.rename(os.path.join(os.path.expanduser('~'), 'base.apk'),
                                  os.path.join(os.path.expanduser('~'), '%s.apk' % package))


class KeyCode:
    KEYCODE_CALL = 5  # 拨号键
    KEYCODE_ENDCALL = 6  # 挂机键
    KEYCODE_HOME = 3  # Home键
    KEYCODE_MENU = 82  # 菜单键
    KEYCODE_BACK = 4  # 返回键
    KEYCODE_SEARCH = 84  # 搜索键
    KEYCODE_CAMERA = 27  # 拍照键
    KEYCODE_FOCUS = 80  # 对焦键
    KEYCODE_POWER = 26  # 电源键
    KEYCODE_NOTIFICATION = 83  # 通知键
    KEYCODE_MUTE = 91  # 话筒静音键
    KEYCODE_VOLUME_MUTE = 164  # 扬声器静音键
    KEYCODE_VOLUME_UP = 24  # 音量+键
    KEYCODE_VOLUME_DOWN = 25  # 音量-键
    KEYCODE_ENTER = 66  # 回车键
    KEYCODE_ESCAPE = 111  # ESC键
    KEYCODE_DPAD_CENTER = 23  # 导航键 >> 确定键
    KEYCODE_DPAD_UP = 19  # 导航键 >> 向上
    KEYCODE_DPAD_DOWN = 20  # 导航键 >> 向下
    KEYCODE_DPAD_LEFT = 21  # 导航键 >> 向左
    KEYCODE_DPAD_RIGHT = 22  # 导航键 >> 向右
    KEYCODE_MOVE_HOME = 122  # 光标移动到开始键
    KEYCODE_MOVE_END = 123  # 光标移动到末尾键
    KEYCODE_PAGE_UP = 92  # 向上翻页键
    KEYCODE_PAGE_DOWN = 93  # 向下翻页键
    KEYCODE_DEL = 67  # 退格键
    KEYCODE_FORWARD_DEL = 112  # 删除键
    KEYCODE_INSERT = 124  # 插入键
    KEYCODE_TAB = 61  # Tab键
    KEYCODE_NUM_LOCK = 143  # 小键盘锁
    KEYCODE_CAPS_LOCK = 115  # 大写锁定键
    KEYCODE_BREAK = 121  # Break / Pause键
    KEYCODE_SCROLL_LOCK = 116  # 滚动锁定键
    KEYCODE_ZOOM_IN = 168  # 放大键
    KEYCODE_ZOOM_OUT = 169  # 缩小键
    KEYCODE_0 = 7
    KEYCODE_1 = 8
    KEYCODE_2 = 9
    KEYCODE_3 = 10
    KEYCODE_4 = 11
    KEYCODE_5 = 12
    KEYCODE_6 = 13
    KEYCODE_7 = 14
    KEYCODE_8 = 15
    KEYCODE_9 = 16
    KEYCODE_A = 29
    KEYCODE_B = 30
    KEYCODE_C = 31
    KEYCODE_D = 32
    KEYCODE_E = 33
    KEYCODE_F = 34
    KEYCODE_G = 35
    KEYCODE_H = 36
    KEYCODE_I = 37
    KEYCODE_J = 38
    KEYCODE_K = 39
    KEYCODE_L = 40
    KEYCODE_M = 41
    KEYCODE_N = 42
    KEYCODE_O = 43
    KEYCODE_P = 44
    KEYCODE_Q = 45
    KEYCODE_R = 46
    KEYCODE_S = 47
    KEYCODE_T = 48
    KEYCODE_U = 49
    KEYCODE_V = 50
    KEYCODE_W = 51
    KEYCODE_X = 52
    KEYCODE_Y = 53
    KEYCODE_Z = 54
    KEYCODE_PLUS = 81  # +
    KEYCODE_MINUS = 69  # -
    KEYCODE_STAR = 17  # *
    KEYCODE_SLASH = 76  # /
    KEYCODE_EQUALS = 70  # =
    KEYCODE_AT = 77  # @
    KEYCODE_POUND = 18  # #
    KEYCODE_APOSTROPHE = 75  # '
    KEYCODE_BACKSLASH = 73  # \
    KEYCODE_COMMA = 55  # ,
    KEYCODE_PERIOD = 56  # .
    KEYCODE_LEFT_BRACKET = 71  # [
    KEYCODE_RIGHT_BRACKET = 72  # ]
    KEYCODE_SEMICOLON = 74  # ;
    KEYCODE_GRAVE = 68  # `
    KEYCODE_SPACE = 62  # 空格键
    KEYCODE_MEDIA_PLAY = 126  # 多媒体键 >> 播放
    KEYCODE_MEDIA_STOP = 86  # 多媒体键 >> 停止
    KEYCODE_MEDIA_PAUSE = 127  # 多媒体键 >> 暂停
    KEYCODE_MEDIA_PLAY_PAUSE = 85  # 多媒体键 >> 播放 / 暂停
    KEYCODE_MEDIA_FAST_FORWARD = 90  # 多媒体键 >> 快进
    KEYCODE_MEDIA_REWIND = 89  # 多媒体键 >> 快退
    KEYCODE_MEDIA_NEXT = 87  # 多媒体键 >> 下一首
    KEYCODE_MEDIA_PREVIOUS = 88  # 多媒体键 >> 上一首
    KEYCODE_MEDIA_CLOSE = 128  # 多媒体键 >> 关闭
    KEYCODE_MEDIA_EJECT = 129  # 多媒体键 >> 弹出
    KEYCODE_MEDIA_RECORD = 130  # 多媒体键 >> 录音


# print(os.path.expanduser("~"))
# print(ADBTools().get_devices())