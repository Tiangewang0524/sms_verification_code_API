# -*- coding: utf-8 -*-

import re
import requests
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import time
import json
import threading
import inspect
import ctypes
from urllib.parse import quote


"""
全局变量介绍：
user_name：登录用户名
password：登录密码
sid: 项目编号
phone_num: 获取的手机号
msg_info: 验证码信息
text1: 获取验证码的文本框
user_info: 账户信息
item: 项目搜索框中的信息
item_info: 服务器返回的模糊查询的项目及编号信息
sid_selection: 项目选择结果
button_list: 项目搜索弹窗的按钮列表（用于删除多余按钮）
listbox_selection: 文本框选择结果
is_area: 选择地区的标识
level: 区分省/城市的标识
i_count: 全局计数器
"""

user_name = ""
password = ""
sid = ""
phone_num = ''
msg_info = ''
text1 = ''
user_info = ''
item = ""
item_info = ""
sid_selection = ""
button_list = []
listbox_selection = ''
is_area = 0
level = ''
i_count = 0


# 登录界面类（所有界面终止并激活新界面类可这么写）
class Reg(tk.Frame):

    def __init__(self, master):
        super().__init__()
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.lab1 = tk.Label(self.frame, text="账户:")
        self.lab1.grid(row=0, column=0, sticky=tk.W)
        self.ent1 = tk.Entry(self.frame)
        self.ent1.grid(row=0, column=1, sticky=tk.W)
        self.lab2 = tk.Label(self.frame, text="密码:")
        self.lab2.grid(row=1, column=0)
        self.ent2 = tk.Entry(self.frame, show="*")
        self.ent2.grid(row=1, column=1, sticky=tk.W)
        self.button = tk.Button(self.frame, text="登录", command=lambda: self.Submit(master))
        # self.button.place(x=100, y=46)
        self.button.grid(row=2, column=1, sticky=tk.W, ipadx=20)
        self.button2 = tk.Button(self.frame, text="注册", command=lambda: self.Register(master))
        self.button2.grid(row=2, column=1, sticky=tk.E, ipadx=20)

    def Submit(self, master):
        global user_name, password
        user_name = self.ent1.get()
        password = self.ent2.get()
        token = loginIn()
        if token[0] != '0':
            tkinter.messagebox.showinfo('通知', '登陆成功！')
            master.destroy()
            first()
        else:
            tkinter.messagebox.showinfo('通知', '密码错误，请重新登陆！')

    def Register(self, master):
        if UserRegister.count < 1:
            # 如果误操作开启多个弹窗，则不会开启多个弹窗
            new_user = UserRegister()
            master.wait_window(new_user)
            UserRegister.count = 0


# 新用户注册类
class UserRegister(tk.Toplevel):
    count = 0

    def __init__(self):
        super().__init__()
        self.title("阿里鸽鸽 version 3.1 beta版 注册")
        UserRegister.count += 1

        # 弹窗界面

        # 第一行
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Label(row1, text="用户名:", width=15).pack(side=tk.LEFT)
        self.reg_user = tk.StringVar()
        tk.Entry(row1, textvariable=self.reg_user, width=20).pack(side=tk.LEFT)

        # 第二行
        row2 = tk.Frame(self)
        row2.pack(fill="x")
        tk.Label(row2, text="密码:", width=15).pack(side=tk.LEFT)
        self.reg_pwd = tk.StringVar()
        tk.Entry(row2, textvariable=self.reg_pwd, width=20, show="*").pack(side=tk.LEFT)

        # 第三行
        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Label(row3, text="确认密码:", width=15).pack(side=tk.LEFT)
        self.reg_repwd = tk.StringVar()
        tk.Entry(row3, textvariable=self.reg_repwd, width=20, show="*").pack(side=tk.LEFT)

        # 第四行
        row4 = tk.Frame(self)
        row4.pack(fill="x")
        tk.Label(row4, text="联系QQ:", width=15).pack(side=tk.LEFT)
        self.reg_qq = tk.StringVar()
        tk.Entry(row4, textvariable=self.reg_qq, width=20).pack(side=tk.LEFT)

        # 第五行
        row5 = tk.Frame(self)
        row5.pack(fill="x")
        tk.Label(row5, text="真实姓名:", width=15).pack(side=tk.LEFT)
        self.reg_realname = tk.StringVar()
        tk.Entry(row5, textvariable=self.reg_realname, width=20).pack(side=tk.LEFT)

        # 第六行
        row6 = tk.Frame(self)
        row6.pack(fill="x")
        tk.Label(row6, text="提现支付宝:", width=15).pack(side=tk.LEFT)
        self.reg_alipay = tk.StringVar()
        tk.Entry(row6, textvariable=self.reg_alipay, width=20).pack(side=tk.LEFT)

        # 第七行
        row7 = tk.Frame(self)
        row7.pack(fill="x")
        tk.Label(row7, text="安全问题:", width=15).pack(side=tk.LEFT)
        self.cmb = ttk.Combobox(row7)
        self.cmb.pack(side=tk.LEFT)
        self.cmb['value'] = ('你初中的老师叫什么？', '你喜欢的颜色？', '你小学的学号是什么？', '你的梦想是什么？')
        self.cmb.current(0)

        # 第八行
        row8 = tk.Frame(self)
        row8.pack(fill="x")
        tk.Label(row8, text="安全答案:", width=15).pack(side=tk.LEFT)
        self.reg_ans = tk.StringVar()
        tk.Entry(row8, textvariable=self.reg_ans, width=20).pack(side=tk.LEFT)

        # 第九行
        row9 = tk.Frame(self)
        row9.pack(fill="x")
        tk.Label(row9, text="推荐人:", width=15).pack(side=tk.LEFT)
        self.reg_referee = tk.StringVar()
        tk.Entry(row9, textvariable=self.reg_referee, width=20).pack(side=tk.LEFT)

        # 第十行
        row10 = tk.Frame(self)
        row10.pack(fill="x")
        tk.Button(row10, text="注册", command=self.register, width=10).pack(side=tk.RIGHT)

    def register(self):
        """
        注册必选参数：
        [1] reg_user 用户名
        [2] reg_pwd 密码
        [3] reg_repwd 二次确认密码
        [4] reg_qq 注册QQ
        [5] reg_realname 真实姓名
        [6] reg_alipay 支付宝账号
        [7] reg_quest 4个安全问题中的一个
        [8] reg_ans 安全答案

        可选参数：
        [1] reg_referee 推荐人id，默认为空
        """

        """
        成功返回：注册成功
        失败返回：注册失败
        """

        # 判断支付宝账号是不是合法，即是否为手机号或者邮箱
        judge = re.match(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", self.reg_alipay.get())
        judge2 = re.match(r"^[1]([3-9])[0-9]{9}$", self.reg_alipay.get())

        # 用URLencode给安全问题编码
        reg_quest = self.cmb.get()
        reg_quest = quote(reg_quest)

        if self.reg_pwd.get() != self.reg_repwd.get():
            tkinter.messagebox.showinfo('通知', '两次密码不一致！')
        elif not judge and not judge2:
            tkinter.messagebox.showinfo('通知', '输入的支付宝账号不合法！')
        else:
            url = "http://115.231.220.181:82/ZC/username={0}&password={1}&password1={2}&QQ={3}&Fullname={4}&" \
                  "account={5}&Referee={6}&problem={7}&Answer={8}" \
                  "&type=1".format(self.reg_user.get(), self.reg_pwd.get(), self.reg_repwd.get(), self.reg_qq.get(),
                                   self.reg_realname.get(), self.reg_alipay.get(), self.reg_referee.get(),
                                   reg_quest, self.reg_ans.get())
            res = requests.get(url)
            res.encoding = res.apparent_encoding
            content = res.text

            if content == '注册成功' or content == '×¢²á³É¹¦':
                tkinter.messagebox.showinfo('通知', '注册成功！')
                self.close()
            elif content == '用户名已被使用':
                tkinter.messagebox.showinfo('通知', '用户名已被使用！')
            elif content == '用户名长度少于6位。':
                tkinter.messagebox.showinfo('通知', '用户名长度少于6位！')
            elif content == '密码长度少于6位。':
                tkinter.messagebox.showinfo('通知', '密码长度少于6位！')
            else:
                tkinter.messagebox.showinfo('通知', '由于网络，服务器响应错误等原因注册失败，请稍候再试！')

    def close(self):
        self.destroy()


# 项目搜索选择类（所有弹窗类可这么写）
class ItemSearch(tk.Toplevel):
    count = 0

    def __init__(self):
        super().__init__()
        self.title("阿里鸽鸽 version 3.1 beta版 项目搜索")
        ItemSearch.count += 1

        # 弹窗界面

        # 第一行
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Label(row1, text="您要搜索的项目名称:", width=15).pack(side=tk.LEFT)
        self.item = tk.StringVar()
        tk.Entry(row1, textvariable=self.item, width=20).pack(side=tk.LEFT)

        # 第二行
        row2 = tk.Frame(self)
        row2.pack(fill="x")
        tk.Button(row2, text="搜索", command=self.Search).pack(side=tk.RIGHT)

        # 第三行
        self.row3 = tk.Frame(self)
        self.row3.pack(fill="x")

    # 展示项目id相关函数
    def show_sid(self, text, event):
        global sid_selection, sid
        button = tk.Button(self.row3, text="确定", command=self.close)

        if text.curselection():
            sid_selection = text.get(text.curselection())

            # 避免选中第一行
            try:
                sid = re.match(r"^\d+", sid_selection).group()

                if sid:
                    button.grid(row=4, column=2, sticky=tk.E, ipadx=15)
                    button_list.append(button)
            except:
                for button in button_list:
                    button.destroy()
                button_list.clear()

    def Search(self):
        global item, item_info
        item = self.item.get()
        item_info = searchItem()

        if item_info:

            listbox_var = tk.StringVar()
            text = tk.Listbox(self.row3, listvariable=listbox_var, selectbackground='red', selectmode=tk.SINGLE,
                              width=18, height=5)
            text.insert(tk.END, '搜索到的项目：\n')
            text.grid(row=4, column=0, padx=15)

            for each in item_info:
                text.insert(tk.END, each)

            # 展示项目边框的滚动条
            text_scrl = tk.Scrollbar(self.row3, width=15)
            text_scrl.grid(row=4, column=0, padx=7, ipady=20, sticky=tk.E)
            text.configure(yscrollcommand=text_scrl.set)
            text_scrl['command'] = text.yview

            text.bind("<<ListboxSelect>>", lambda event: self.show_sid(text, event))

        else:
            tkinter.messagebox.showinfo('通知', '抱歉，没搜索到相关项目！')

    def close(self):
        self.destroy()


# 区域选择类
class AreaSelect(tk.Toplevel):
    count = 0

    def __init__(self):
        super().__init__()
        self.title("阿里鸽鸽 version 3.1 beta版 区域选择")
        AreaSelect.count += 1

        # 弹窗界面

        # 第一行
        self.row1 = tk.Frame(self)
        self.row1.pack(fill="x")

        # 第二行
        self.row2 = tk.Frame(self)
        self.row2.pack(fill="x")


        # 创建下拉菜单
        self.cmb_1 = ttk.Combobox(self.row1)
        self.cmb_1.grid(row=0, column=0, pady=12, padx=20)
        # 设置下拉菜单中的值
        self.cmb_1['value'] = ('自行选择地区', '随机生成')
        # 设置默认值，即默认下拉框中的内容
        self.cmb_1.current(1)
        self.cmb_1.bind("<<ComboboxSelected>>", self.cmb_1_select_result)

        # 确认并关闭按钮
        button = tk.Button(self.row1, text="确定", command=self.close)
        button.grid(row=0, column=2, sticky=tk.E, ipadx=50)

        # 城市/省文本框初始化
        m_listbox_var = tk.StringVar()
        self.m_list = tk.Listbox(self.row2, listvariable=m_listbox_var, selectbackground='red', selectmode=tk.SINGLE,
                            width=16, height=10)

        # 文本框滚动条初始化
        self.m_scrl = tk.Scrollbar(self.row2, width=15)

        self.m_list.grid_forget()
        self.m_scrl.grid_forget()

    def cmb_2_select_result(self, cmb_2, event):

        global level

        if cmb_2.get() == '按市筛选':

            level = 'c'
            # 文本框相关
            self.m_list.delete(0, tk.END)
            with open('./dataset/city_sorted.txt', 'r', encoding='gbk') as f1:
                temp_list = f1.readlines()
            for item in temp_list:
                # 去掉换行符
                item = item.strip()
                self.m_list.insert(tk.END, item)

            self.m_list.grid(row=1, column=1, pady=10, padx=5)

            self.m_list.bind("<<ListboxSelect>>", self.show_city)

            # 滚动条
            self.m_scrl.grid(row=1, column=1, padx=5, ipady=40, sticky=tk.E)
            self.m_list.configure(yscrollcommand=self.m_scrl.set)
            self.m_scrl['command'] = self.m_list.yview

        else:
            level = 'p'
            # 文本框相关
            self.m_list.delete(0, tk.END)
            with open('./dataset/province.txt', 'r', encoding='gbk') as f1:
                temp_list = f1.readlines()
            for each in temp_list:
                # 去掉换行符
                each = each.strip()
                self.m_list.insert(tk.END, each)

            self.m_list.grid(row=1, column=1, pady=10, padx=5)

            self.m_list.bind("<<ListboxSelect>>", self.show_province)

            # 滚动条
            self.m_scrl.grid(row=1, column=1, padx=5, ipady=40, sticky=tk.E)
            self.m_list.configure(yscrollcommand=self.m_scrl.set)
            self.m_scrl['command'] = self.m_list.yview

    def cmb_1_select_result(self, event):

        # 是否选择地区标识符
        global is_area, i_count
        cmb_2 = ttk.Combobox(self.row2)

        if self.cmb_1.get() == '自行选择地区':
            is_area = 1
            if i_count != 0:
                self.row2.pack(fill="x")
                self.m_list.grid_forget()
                self.m_scrl.grid_forget()
            cmb_2.grid(row=1, column=0, pady=12, padx=20)
            # 设置下拉菜单中的值
            cmb_2['value'] = ('按市筛选', '按省筛选')
            # 设置默认值，即默认下拉框中的内容
            # cmb_2.current(0)
            i_count += 1
            cmb_2.bind("<<ComboboxSelected>>", lambda event: self.cmb_2_select_result(cmb_2, event))
        else:
            is_area = 0
            i_count += 1
            self.row2.pack_forget()

    # 按市筛选 m_list 文本框选中事件
    def show_city(self, event):
        global listbox_selection
        if self.m_list.curselection():
            listbox_selection = self.m_list.get(self.m_list.curselection())
            print(self.m_list.get(self.m_list.curselection()))

    # 按省筛选 m_list 文本框选中事件
    def show_province(self, event):
        global listbox_selection
        if self.m_list.curselection():
            listbox_selection = self.m_list.get(self.m_list.curselection())

    def close(self):
        global is_area, listbox_selection
        if self.cmb_1.get() == '自行选择地区' and listbox_selection == '':
            tkinter.messagebox.showwarning('警告', '请选择一个城市/省')
        elif self.cmb_1.get() == '随机生成':
            is_area = 0
            listbox_selection = ''
            self.destroy()
        else:
            self.destroy()


# kill线程相关
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    if thread.name != 'MainThread':
        _async_raise(thread.ident, SystemExit)

def stop_thread_step():
    # print(threading.active_count())
    stop_thread(threading.enumerate()[-1])


# 登录
def loginIn():
    """
    成功统一返回：1|token
    失败统一返回：0|失败信息
    """

    global user_name, password
    url = "http://115.231.220.181:8000/api/sign/username={0}&password={1}".format(user_name, password)
    res = requests.get(url).text
    token = res.split("|")
    return token

# 获取项目id
def searchItem():
    """
    用于搜索项目
    返回输入字符的相关搜索结果
    """
    url = "http://115.231.220.181:83/liebiao_xm/username={0}&password={1}&lx=1&ss={2}".format(user_name, password, item)
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    info = res.text.replace('#c', '')

    info_pat = re.findall(r"\d+-\w*-?[\u4e00-\u9fa5]+", info)

    return info_pat

# 获取手机号
def getNumber(Token, sid):
    """
    [传入参数]：通过监听客户端http get请求发现随机生成和指定地区请求的服务器端口号以及地址都不同！

    随机地区手机号属性可选参数：
    [1] id=项目ID (对应的项目ID可在客户端软件里查询)
    [2] operator=0 (0=默认 1=移动 2=联通 3=电信)
    [3] Region=0 (0=默认)需要哪个地区的直接输入如：上海 系统会自动筛选上海的号码
    [4] card=0 (0=默认 1=虚拟运营商 2=实卡)
    [5] phone= (你要指定获取的号码,不传入号码情况下,获取新号码.)
    [6] loop=1（1=过滤 2=不过滤）1排除已做过号码取号时不会再获取到，2不过滤已做号码可以取号时循环获取号码（号码循环做业务必须选择2）
    [7] token=(登录成功返回的token)

    指定地区手机号参数：
    [1] username (登录时的用户名)
    [2] password (登录时的对应密码)
    [3] id=项目ID (对应的项目ID可在客户端软件里查询)
    [4] phone= (你要指定获取的号码,不传入号码情况下,获取新号码.)
    [5] operator=0 (0=默认 1=移动 2=联通 3=电信)
    [6] region=具体的URLencode编码 (无默认值) 具体地区选择之后 quote函数自动转编码为URLencode
        如：选择河南后 quote('河南') 转为 %e6%b2%b3%e5%8d%97 之后服务器响应一个归属地为河南的号码
    [7] card= (默认为空/0 1=虚拟运营商 2=实卡)
    [8] loop=（默认为空/1 1=过滤 2=不过滤）1排除已做过号码取号时不会再获取到，2不过滤已做号码可以取号时循环获取号码（号码循环做业务必须选择2）
    """

    """
    成功返回: 1|获取到的手机号
    失败返回: 0|错误信息
    """

    # 指定地区
    # level =c 代表城市, =p 代表省
    # city/province 必须使用Urlencode进行中文编码
    # e.g. 郑州
    # city = '%e9%83%91%e5%b7%9e'

    global listbox_selection, is_area, level, user_name, password
    if is_area:
        if listbox_selection == '':
            tkinter.messagebox.showwarning('警告', '请在选择地区按钮里选择一个城市/省或者随机生成！')
            # 程序报错, 线程停止并不再进行操作
            stop_thread(threading.enumerate()[-1])
        else:
            city = quote(listbox_selection)
            # print(listbox_selection)
            url = "http://115.231.220.181:81/yh_qh/username={0}&password={1}&id={2}&phone=" \
                  "&operator=&region={3}&card=&loop=".format(user_name, password, sid, city)
            # print(url)
            res = requests.get(url)
            res.encoding = res.apparent_encoding
            res = res.text
            phone_num = res.split("|")
            # 返回 1 | 手机号
            # print(phone_num[1])
            if phone_num[0] == '1':
                return phone_num[1]
            else:
                tkinter.messagebox.showinfo('通知', '号码库未记录该地区号码')
                return res
    else:
        # 随机生成号码
        url = "http://115.231.220.181:8000/api/yh_qh/id={0}&operator=0&Region=0&card=0&phone=&loop=1&token={1}".format(sid, Token)
        res = requests.get(url).text
        phone_num = res.split("|")
        # 返回 1 | 手机号
        # print(phone_num[1])
        if phone_num[0] == '1':
            return phone_num[1]

# 释放手机号
def cancelAllRecv(sid, phone_num, Token):
    """
    成功返回: 1|释放成功
    失败返回: 0|错误信息
    """

    # 释放手机号
    # url = "http://115.231.220.181:8000/api/yh_sf/id={0}&phone={1}&token={2}"
    # .format(sid, phone_num, Token)
    # 释放全部手机号:
    # url = "http://115.231.220.181:8000/api/yh_sf/token={0}".format(Token)
    url = "http://115.231.220.181:8000/api/yh_sf/id={0}&phone={1}&token={2}"\
        .format(sid, phone_num, Token)  # 项目id 手机号 登录返回的口令
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    res = res.text.split('|')

    return res


# 获取用户信息
def getSummary(Token):
    """
    成功返回: 余额|可提现余额
    失败返回: 0|错误信息
    """
    global user_info
    url = "http://115.231.220.181:8000/api/yh_gx/token={0}".format(Token)
    res = requests.get(url).text
    info = res.split('|')
    # # print(res)
    # # print('您的账户余额为{0}, 等级为{1}, 批量取号数为{2}, 用户类型为{3}'.format(info[1], info[2], info[3], info[4]))
    user_info = '您的账户余额为{0}, 可提现余额为{1}'.format(info[0], info[1])
    # user_info = '您的账户余额为{0}, 可提现余额为{1}'.format(11, 1)
    return info


# 获取验证码
def getMessage(Token, sid, phone_num):
    """
    成功返回: 1|短信内容
    失败返回: 0|错误信息
    """

    global text1, user_name
    url = "http://115.231.220.181:8000/api/yh_qm/id={0}&phone={1}&t={2}&token={3}".format(sid, phone_num, user_name, Token)
    res = requests.get(url)
    # 响应自动正确转码
    res.encoding = res.apparent_encoding
    i = 1
    while res.text.split("|")[1] == '没有收到短信':
        msg_get_info = '正在获取短信中，第' + str(i) + '次尝试'
        i += 1
        res = requests.get(url)
        res.encoding = res.apparent_encoding
        text1.config(state=tk.NORMAL)
        text1.insert(tk.END, msg_get_info)
        text1.insert(tk.END, '\n')
        text1.config(state=tk.DISABLED)
        time.sleep(3)
        text1.config(state=tk.NORMAL)
        text1.delete(2.0, 3.0)
        text1.config(state=tk.DISABLED)
    else:
        if res.text.split("|")[0] == '0':
            tkinter.messagebox.showwarning(res.text.split("|")[1])

    return res.text.split("|")[1]


# 用户窗口
def first():
    top = tk.Tk()
    top.geometry("900x550")

    # 锁死窗口大小
    top.minsize(900, 550)  # 最小尺寸
    top.maxsize(900, 550)  # 最大尺寸

    top.title("阿里鸽鸽 version 3.1 beta版")
    # 用户登录接码码 返回值token
    Token = loginIn()[1]

    global text1, phone_num
    # 界面用户信息
    info = getSummary(Token)

    # 主要功能的回调函数
    def main_function():

        if sid == '':
            tkinter.messagebox.showwarning('警告', '尚未选择项目，请选择项目！')
            return 0

        text1.config(state=tk.NORMAL)
        text2.config(state=tk.NORMAL)
        text1.delete(1.0, 3.0)
        text2.delete(1.0, 'end')
        text1.insert(tk.CURRENT, '您的验证码相关信息如下：\n')
        text2.insert(tk.CURRENT, '给您提供的手机号为：\n')
        text1.update()
        text2.update()
        text1.config(state=tk.DISABLED)
        text2.config(state=tk.DISABLED)

        if threading.active_count() > 2:
            # 如果多次获取，则结束上一次获取，以最新的获取为准
            stop_thread(threading.enumerate()[-2])

        global phone_num, msg_info
        a = 1
        if info[0] != '0':
            # 如需获取多个手机号 请将循环条件改为 a < 要获取的手机号数量+1
            while a < 2:
                time.sleep(1)
                # 取手机号  return 手机号
                phone_num = getNumber(Token, sid)

                if phone_num != '没有可用号码':
                    text2.config(state=tk.NORMAL)
                    text2.insert(tk.END, phone_num)
                    text2.insert(tk.END, '\n')

                    # 检查运营商信息
                    temp_url = 'http://mobsec-dianhua.baidu.com/dianhua_api/open/location?tel=' + str(phone_num)
                    html_info = requests.get(temp_url).text
                    operator_info = json.loads(html_info)['response'][phone_num]['location']
                    # print('给您提供的手机号为:{0}, 运营商为:{1}'.format(phone_num, operator_info))
                    text2.insert(tk.END, operator_info)
                    text2.config(state=tk.DISABLED)

                    # 获取验证码
                    msg_info = getMessage(Token, sid, phone_num)
                    if msg_info:
                        text1.config(state=tk.NORMAL)
                        text1.insert(tk.END, msg_info)
                        text1.update()
                        text1.config(state=tk.DISABLED)
                        # 扣费后更新用户信息
                        getSummary(Token)
                        fm2.titleLabel['text'] = user_info
                    # if code:
                    #     print("验证码：", code)
                a = a + 1
        else:
            tkinter.messagebox.showwarning('警告', '余额不足，请充值！')

    # 搜索项目相关函数
    def item():
        if ItemSearch.count < 1:
            # 如果误操作开启多个弹窗，则不会开启多个弹窗
            new_item = ItemSearch()
            top.wait_window(new_item)  # 这一句很重要！！！
            text3.config(state=tk.NORMAL)
            text3.delete(1.0, 'end')
            text3.insert(tk.CURRENT, '您选择的项目为：\n')
            text3.insert(tk.END, sid_selection)
            text3.update()
            text3.config(state=tk.DISABLED)
            ItemSearch.count = 0
        # print(sid)

    # 选择地区相关函数
    def area():
        if AreaSelect.count < 1:
            # 如果误操作开启多个弹窗，则不会开启多个弹窗
            new_area = AreaSelect()
            top.wait_window(new_area)
            text4.config(state=tk.NORMAL)
            text4.delete(1.0, 'end')
            text4.insert(tk.CURRENT, '您选择的地区为：\n')
            if listbox_selection:
                text4.insert(tk.END, listbox_selection)
            else:
                text4.insert(tk.END, '随机生成地区')
            text4.update()
            text4.config(state=tk.DISABLED)
            AreaSelect.count = 0

    # 释放手机号的回调函数
    def release():
        phone_pat = re.match(r"^1[3456789]\d{9}$", text2.get('2.0', '3.0'))
        if phone_pat:
            if threading.active_count() > 2:
                stop_thread(threading.enumerate()[-2])
            text1.config(state=tk.NORMAL)
            text2.config(state=tk.NORMAL)
            text1.delete(1.0, 3.0)
            text2.delete(1.0, 'end')
            text1.insert(tk.CURRENT, '您的验证码相关信息如下：\n')
            text2.insert(tk.CURRENT, '给您提供的手机号为：\n')
            text1.update()
            text2.update()
            text1.config(state=tk.DISABLED)
            text2.config(state=tk.DISABLED)
            o_code = cancelAllRecv(sid, phone_num, Token)
            # time.sleep(2)
            if o_code[0] == '1':
                # print('手机号释放成功!')
                tkinter.messagebox.showinfo('通知', '手机号释放成功！')
                getSummary(Token)
                fm2.titleLabel['text'] = user_info
            else:
                tkinter.messagebox.showwarning('警告', o_code[1])
        else:
            tkinter.messagebox.showwarning('警告', '没有获取到手机号, 释放失败！请重试！')

    def thread_it(func, *args):
        '''将函数打包进线程'''
        def gothread(*args):
            # sem.acquire()
            # print(threading.current_thread().name)
            func(*args)

        # 创建
        t = threading.Thread(target=gothread, args=args)
        # 守护 !!!
        t.setDaemon(True)
        # 启动
        t.start()
        # print(threading.current_thread())
        # print(threading.active_count())

        # 阻塞--卡死界面！
        # t.join()

    # Frame
    fm1 = tk.Frame(top, bg='black')
    fm1.titleLabel = tk.Label(fm1, text="阿里鸽鸽接码客户端 版本号: 3.1 ", font=('微软雅黑', 30), fg="white", bg='black')
    fm1.titleLabel.pack()
    fm1.pack(side=tk.TOP, fill='x', pady=5)

    # row
    row1 = tk.Frame(top)
    row1.pack(fill="x")
    row2 = tk.Frame(top)
    row2.pack(fill="x")
    row3 = tk.Frame(top)
    row3.pack(fill="x")
    row4 = tk.Frame(top)
    row4.pack(fill="x")

    text2 = tk.Text(row3, width=30, height=4)
    text2.insert(tk.CURRENT, '给您提供的手机号为：\n')
    text2.grid(row=2, column=1, padx=10)
    text2.config(state=tk.DISABLED, highlightbackground='black')

    text1 = tk.Text(row3, width=50, height=4)
    text1.insert(tk.CURRENT, '您的验证码相关信息如下：\n')
    text1.grid(row=2, column=2, padx=10)
    text1.config(state=tk.DISABLED, highlightbackground='black')

    text3 = tk.Text(row1, width=30, height=4)
    text3.insert(tk.CURRENT, '您选择的项目为：\n')
    text3.grid(row=0, column=1, padx=10)
    text3.config(state=tk.DISABLED, highlightbackground='black')

    text4 = tk.Text(row2, width=30, height=4)
    text4.insert(tk.CURRENT, '您选择的地区为：\n')
    text4.grid(row=1, column=1, padx=10)
    text4.config(state=tk.DISABLED, highlightbackground='black')

    button1 = tk.Button(row1, text="憨憨，选择项目！！！", command=lambda: thread_it(item), font=('微软雅黑', 12),
                        width=30, height=2, bg="yellow")
    button1.grid(row=0, column=0, padx=20, pady=30)

    button2 = tk.Button(row2, text="憨憨，选择归属地！！！", command=lambda: thread_it(area), font=('微软雅黑', 12),
                        width=30, height=2, bg="yellow")
    button2.grid(row=1, column=0, padx=20, pady=30)

    button3 = tk.Button(row3, text="憨憨，准备接码！！！", command=lambda: thread_it(main_function), font=('微软雅黑', 12),
                        width=30, height=3, bg="yellow")
    button3.grid(row=2, column=0, padx=20, pady=30)

    button4 = tk.Button(row4, text="憨憨，释放手机号！！！", command=lambda: thread_it(release), font=('微软雅黑', 12),
                        width=30, height=2, bg="yellow")
    button4.grid(row=3, column=0, padx=20, pady=30)

    # 底部frame,实时显示用户余额
    fm2 = tk.Frame(top, bg='black')
    fm2.titleLabel = tk.Label(fm2, text=user_info, font=('微软雅黑', 20), fg="white", bg='black')
    fm2.titleLabel.pack()
    fm2.pack(side=tk.BOTTOM, fill='x', pady=5)

    top.mainloop()


if __name__ == "__main__":

    root = tk.Tk()
    root.title("阿里鸽鸽 version 3.1 beta版 用户登录")

    # 锁死窗口大小
    root.minsize(230, 90)  # 最小尺寸
    root.maxsize(230, 90)  # 最大尺寸
    # root.resizable(0, 0)

    app = Reg(root)
    root.mainloop()
