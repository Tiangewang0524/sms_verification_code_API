import requests
import hashlib
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import time
import json
import threading
import inspect
import ctypes
import webbrowser
from urllib.parse import quote

# import phone

# 用户名
# 密码
# 项目编号 T3出行:70122
user_name = ""
password = ""
sid = "70122"
ph_num = ''
msg_info = ''
text1 = ''
user_info = ''
# 文本框选择结果
listbox_selection = ''
# 选择地区的标识
is_area = 0
# 区分省/城市的标识
level = ''
# 全局计数器
i_count = 0


hl = hashlib.md5()
hl.update(password.encode(encoding='utf-8'))

# 登录界面类
class Reg(tk.Frame):

    def __init__(self, master):
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
        self.button.place(x=100, y=46)
        self.button2 = tk.Button(self.frame, text="注册", command=self.Register)
        self.button2.grid(row=2, column=1, sticky=tk.E)

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

    def Register(self):
        webbrowser.open("http://www.sfoxer.com/reg.html", new=0)

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
    print(threading.active_count())
    stop_thread(threading.enumerate()[-1])


# 登录
def loginIn():
    global user_name, password
    url = "http://api.sfoxer.com/api/do.php?action=loginIn&name={0}&password={1}".format(user_name, password)
    res = requests.get(url).text
    token = res.split("|")
    return token


# 获取手机号
def getNumber(Token, sid):
    """
    手机号属性可选参数：
    1.size=要获取手机号数量。1<size<50
    2.phone=你要指定获取的号码,传入号码不正确的情况下,获取新号码.
    3.phoneType=CMCC，CMCC是指移动，UNICOM是指联通，TELECOM是指电信
    4.vno=0或1，0是指排除所有虚拟运营商号码，1是只获取虚拟运营商号码
    5.locationMatching、locationLevel、location三个必须一起使用。用来指定获取某个地区的号码
        5.1 locationMatching=include(包含区域) 或 locationMatching=exclude(排除区域)
        5.2 locationLevel=p(省份) 或 locationLevel=c(城市)
        5.3 location=(要包含或排除的省份或城市,该值对应locationLevel)
        5.4 locationMatching、locationLevel、location三个必须一起使用。用来指定取某些区域的手机号或者不要某些区域的手机号
    特别注意:
    locationMatching的参数值只能是include或者exclude中的一个。
    include指的是包含区域，exclude指的是不包含区域
    locationLevel参数只能是p或者c中的一个。p指的是省（province），c指的是市（city）
    location指的是具体地区，中文值。需要UrlEncode编码 例：湖南编码后的值为 u%e6%b9%96%e5%8d%97
    """

    # 随机获取手机号
    # url = "http://api.sfoxer.com/api/do.php?action=getPhone&token={0}&sid={1}".format(Token, sid)

    # 指定地区
    # level =c 代表城市, =p 代表省
    # city/province 必须使用Urlencode进行中文编码
    # e.g. 郑州
    # city = '%e9%83%91%e5%b7%9e'
    global listbox_selection, is_area, level
    if is_area:
        if listbox_selection == '':
            tkinter.messagebox.showwarning('警告','请选择一个城市/省')
            # 程序报错, 线程停止并不再进行操作
            stop_thread(threading.enumerate()[-1])
        else:
            city = quote(listbox_selection)
            # print(listbox_selection)
            url = "http://api.sfoxer.com/api/do.php?action=getPhone&token={0}&sid={1}" \
                  "&locationMatching=include&locationLevel={2}&location={3}".format(Token, sid, level, city)
            # print(url)
            res = requests.get(url).text
            phone_num = res.split("|")
            # 返回 1 | 手机号
            # print(phone_num[1])
            if phone_num[0] == '1':
                return phone_num[1]
            else:
                tkinter.messagebox.showinfo('通知', '号码库未记录该地区号码')
                return phone_num[1]
    else:
        # 随机生成号码
        url = "http://api.sfoxer.com/api/do.php?action=getPhone&token={0}&sid={1}".format(Token, sid)
        res = requests.get(url).text
        phone_num = res.split("|")
        # 返回 1 | 手机号
        # print(phone_num[1])
        if phone_num[0] == '1':
            return phone_num[1]

# 释放手机号
def cancelAllRecv(sid, phone_num, Token):  # 释放手机号
    # url = "http://api.xinheyz.com/api/do.php?action=addBlacklist&sid={0}&phone={1}&token={2}"
    # .format(sid, phone_num, Token)
    url = "http://api.sfoxer.com/api/do.php?action=cancelAllRecv&token={0}".format(Token)
    #  url = "http://api.xinheyz.com/api/do.php?action=cancelRecv&sid={0}&phone={1}&token={2}"
    #  .format(sid,phone_num,Token) #项目id 手机号 登录返回的口令
    # print(url)
    res = requests.get(url).text
    res = res.split('|')
    # print(res)

    return res


# 获取用户信息
def getSummary(Token):
    """
    1.成功返回: 1|余额|等级|批量取号数|用户类型
    2.失败返回: 0|错误信息
    """
    global user_info
    url = "http://api.sfoxer.com/api/do.php?action=getSummary&token={0}".format(Token)
    res = requests.get(url).text
    info = res.split('|')
    # print(res)
    # print('您的账户余额为{0}, 等级为{1}, 批量取号数为{2}, 用户类型为{3}'.format(info[1], info[2], info[3], info[4]))
    user_info = '您的账户余额为{0}, 等级为{1}, 批量取号数为{2}, 用户类型为{3}'.format(info[1], info[2], info[3], info[4])


# 获取验证码
def getMessage(Token, sid, phone_num, user_name):
    global text1
    url = "http://api.sfoxer.com/api/do.php?action=getMessage&token={0}&sid={1}&phone={2}".format(Token, sid, phone_num)
    res = requests.get(url)
    i = 1
    while res.text.split("|")[1] == '还没有接收到短信，请过3秒再试':
        msg_get_info = '正在获取短信中，第' + str(i) + '次尝试'
        # print(msg_get_info)
        i += 1
        res = requests.get(url)
        text1.insert(tk.END, msg_get_info)
        text1.insert(tk.END, '\n')
        time.sleep(3)
        text1.delete(2.0, 3.0)
    else:
        if res.text.split("|")[0] == '0':
            tkinter.messagebox.showwarning(res.text.split("|")[1])
        # else:
        #     print('接收到验证码, 验证码为{}'.format(res.text.split("|")[1]))

    return res.text.split("|")[1]


# 用户窗口
def first():
    top = tk.Tk()
    top.geometry("960x650")
    top.title("阿里鸽鸽 version 1.4 beta版")
    phone_num = 0
    # 用户登录接码码 返回值token
    Token = loginIn()[1]
    # 设置进程数，无效已废弃使用
    # sem = threading.Semaphore(3)
    global text1
    # 界面用户信息
    getSummary(Token)

    # 主要功能的回调函数
    def helloCallBack():

        text1.delete(1.0, 3.0)
        text2.delete(1.0, 'end')
        text1.insert(tk.CURRENT, '您的验证码相关信息如下：\n')
        text2.insert(tk.CURRENT, '给您提供的手机号为：\n')
        text1.update()
        text2.update()

        if threading.active_count() > 2:
            # 如果多次获取，则结束上一次获取，以最新的获取为准
            stop_thread(threading.enumerate()[-2])

        global ph_num, msg_info
        a = 1
        # 如需获取多个手机号 请将循环条件改为 a < 要获取的手机号数量+1
        while a < 2:
            time.sleep(1)
            # 用户登录接码码 返回值token
            # Token = loginIn()
            # 取手机号  return 手机号
            phone_num = getNumber(Token, sid)
            ph_num = phone_num
            if phone_num != '未获取到号码':
                text2.insert(tk.END, ph_num)
                text2.insert(tk.END, '\n')
            # else:
            #     break
            # check(phone_num)

            # 检查运营商信息
            temp_url = 'http://mobsec-dianhua.baidu.com/dianhua_api/open/location?tel=' + str(phone_num)
            html_info = requests.get(temp_url).text
            operator_info = json.loads(html_info)['response'][phone_num]['location']
            # print('给您提供的手机号为:{0}, 运营商为:{1}'.format(phone_num, operator_info))
            text2.insert(tk.END, operator_info)

            # 获取验证码
            msg_info = getMessage(Token, sid, ph_num, user_name)
            if msg_info:
                text1.insert(tk.END, msg_info)
                text1.update()
                # 扣费后更新用户信息
                getSummary(Token)
                fm2.titleLabel['text'] = user_info
            # if code:
            #     print("验证码：", code)
            a = a + 1

    # 释放手机号的回调函数
    def release():
        if threading.active_count() > 2:
            stop_thread(threading.enumerate()[-2])
            text1.delete(1.0, 3.0)
            text2.delete(1.0, 'end')
            text1.insert(tk.CURRENT, '您的验证码相关信息如下：\n')
            text2.insert(tk.CURRENT, '给您提供的手机号为：\n')
            text1.update()
            text2.update()
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
    fm1.titleLabel = tk.Label(fm1, text="阿里鸽鸽接码客户端 1.4版", font=('微软雅黑', 30), fg="white", bg='black')
    fm1.titleLabel.pack()
    fm1.pack(side=tk.TOP, expand=tk.YES, fill='x', pady=5)


    # Grid
    grid_a = tk.Frame(top, height=50, width=200)
    grid_a.pack(side='top', fill='both', expand=True, padx=100, pady=10, ipadx=300)

    grid_a_right = tk.Frame(top, height=30, width=200)
    grid_a_right.pack(side='top', fill='both', expand=True, padx=150, pady=5, after=grid_a, ipadx=250, ipady=10)

    grid_b = tk.Frame(top, height=70, width=200)
    grid_b.pack(side='top', fill='both', expand=True, padx=100)

    grid_c = tk.Frame(top, height=50, width=200)
    grid_c.pack(side='top', fill='both', expand=True, padx=100)

    # 创建下拉菜单
    cmb_1 = ttk.Combobox(grid_a)
    cmb_1.grid(row=0, column=1, pady=10, padx=4)
    # 设置下拉菜单中的值
    cmb_1['value'] = ('自行选择地区', '随机生成')
    # 设置默认值，即默认下拉框中的内容
    # cmb_1.current(0)

    # 城市/省文本框初始化
    m_listbox_var = tk.StringVar()
    m_list = tk.Listbox(grid_a_right, listvariable=m_listbox_var, selectbackground='red', selectmode=tk.SINGLE,
                        width=20, height=10)

    # 文本框滚动条初始化
    m_scrl = tk.Scrollbar(grid_a_right, width=15)

    m_list.grid_forget()
    m_scrl.grid_forget()


    # 下拉菜单选择事件

    def cmb_2_select_result(event, cmb_2):

        global level

        if cmb_2.get() == '按市筛选':

            level = 'c'
            # 文本框相关
            m_list.delete(0, tk.END)
            with open('./dataset/city_sorted.txt', 'r') as f1:
                # temp_list = ['南京', '北京', '乌鲁木齐', 'hello Miss4', 'hello Miss5', 'hello Miss6']
                temp_list = f1.readlines()
            for item in temp_list:
                # 去掉换行符
                item = item.strip()
                m_list.insert(tk.END, item)

            m_list.grid(row=1, column=1, pady=10, padx=5)

            # m_list 文本框选中事件
            def show_city(event):
                global listbox_selection
                if m_list.curselection():
                    listbox_selection = m_list.get(m_list.curselection())
                    # print(m_list.get(m_list.curselection()))

            # show_city = lambda x: print(temp_list[x])
            m_list.bind("<<ListboxSelect>>", show_city)

            # 滚动条
            m_scrl.grid(row=1, column=1, padx=5, ipady=40, sticky=tk.E)
            m_list.configure(yscrollcommand=m_scrl.set)
            m_scrl['command'] = m_list.yview

        else:
            level = 'p'
            # 文本框相关
            m_list.delete(0, tk.END)
            with open('./dataset/province.txt', 'r') as f1:
                temp_list = f1.readlines()
            for item in temp_list:
                # 去掉换行符
                item = item.strip()
                m_list.insert(tk.END, item)

            m_list.grid(row=1, column=1, pady=10, padx=5)

            # m_list 文本框选中事件
            def show_province(event):
                global listbox_selection
                if m_list.curselection():
                    listbox_selection = m_list.get(m_list.curselection())

            m_list.bind("<<ListboxSelect>>", show_province)

            # 滚动条
            m_scrl.grid(row=1, column=1, padx=5, ipady=40, sticky=tk.E)
            m_list.configure(yscrollcommand=m_scrl.set)
            m_scrl['command'] = m_list.yview

    # cmb_2 下拉菜单选择中间适配函数
    def cmb_2_step_1(func, *args):
        """事件处理函数的适配器，相当于中介"""
        return lambda event, func=func, args=args: func(event, *args)

    def cmb_1_select_result(event):

        # 是否选择地区标识符
        global is_area, i_count
        cmb_2 = ttk.Combobox(grid_a_right)

        if cmb_1.get() == '自行选择地区':
            is_area = 1
            if i_count != 0:
                grid_a_right.pack(side='top', fill='both', expand=True, padx=150, pady=5, after=grid_a, ipadx=250, ipady=10)
                m_list.grid_forget()
                m_scrl.grid_forget()
            cmb_2.grid(row=1, column=0, pady=12, padx=20)
            # 设置下拉菜单中的值
            cmb_2['value'] = ('按市筛选', '按省筛选')
            # 设置默认值，即默认下拉框中的内容
            # cmb_2.current(0)
            i_count += 1
            cmb_2.bind("<<ComboboxSelected>>", cmb_2_step_1(cmb_2_select_result, cmb_2))
        else:
            is_area = 0
            i_count += 1
            grid_a_right.pack_forget()

    cmb_1.bind("<<ComboboxSelected>>", cmb_1_select_result)

    text2 = tk.Text(grid_b, width=30, height=5)
    text2.insert(tk.CURRENT, '给您提供的手机号为：\n')
    text2.grid(row=2, column=0, padx=10)

    text1 = tk.Text(grid_b, width=70, height=5)
    text1.insert(tk.CURRENT, '您的验证码相关信息如下：\n')
    text1.grid(row=2, column=1, padx=10)


    button1 = tk.Button(grid_a, text="憨憨，准备接码！！！", command=lambda: thread_it(helloCallBack), font=('微软雅黑', 12),
                        width=20, height=2, bg="yellow")
    button1.grid(row=0, column=0, padx=20)


    button2 = tk.Button(grid_c, text="憨憨，释放手机号吗？？？", command=lambda: thread_it(release), font=('微软雅黑', 12),
                        width=20,height=2, bg="yellow")
    button2.grid(row=3, column=0, pady=50, padx=20)

    # 底部frame,实时显示用户余额
    fm2 = tk.Frame(top, bg='black')
    fm2.titleLabel = tk.Label(fm2, text=user_info, font=('微软雅黑', 20), fg="white", bg='black')
    fm2.titleLabel.pack()
    fm2.pack(side=tk.BOTTOM, expand=tk.YES, fill='x', pady=5)

    top.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("用户登录")
    app = Reg(root)
    root.mainloop()
