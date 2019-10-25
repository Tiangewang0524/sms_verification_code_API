import requests
import hashlib
import win32gui
import win32con
import win32clipboard as w
import tkinter as tk
import tkinter.messagebox
import time
import json
import threading

# import phone

# 用户名
# 密码
# 项目编号 T3出行:70122
user_name = "qa******"
password = "qw******"
sid = "70122"
ph_num = ''
msg_info = ''
text1 = ''

hl = hashlib.md5()
hl.update(password.encode(encoding='utf-8'))


# 登录
def loginIn():
    url = "http://api.sfoxer.com/api/do.php?action=loginIn&name={0}&password={1}".format(user_name, password)
    print(url)
    res = requests.get(url).text
    print(res)
    #    dic=eval(res)
    token = res.split("|")
    token[0] = int(token[0])
    if token[0] == 1:
        print("登录成功")
    print("token值为：" + token[1])
    return token[1]


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
    city = '%e9%83%91%e5%b7%9e'
    url = "http://api.sfoxer.com/api/do.php?action=getPhone&token={0}&sid={1}" \
          "&locationMatching=include&locationLevel=c&location={2}".format(Token, sid, city)
    # print(url)
    res = requests.get(url).text
    phone_num = res.split("|")
    # 返回 1 | 手机号
    # print(phone_num[1])
    return phone_num[1]


# 检测手机号
def check(phone_num):
    # 发送的消息
    msg = str(phone_num)
    # 窗口名字
    name = "检测检测检测啊"
    # 将测试消息复制到剪切板中
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, msg)
    w.CloseClipboard()
    # 获取窗口句柄
    handle = win32gui.FindWindow(None, name)
    # while 1==1:
    if 1 == 1:
        # 填充消息
        win32gui.SendMessage(handle, 770, 0, 0)
        # 回车发送消息
        win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)


# 释放手机号
def cancelAllRecv(sid, phone_num, Token):  # 释放手机号
    # url = "http://api.xinheyz.com/api/do.php?action=addBlacklist&sid={0}&phone={1}&token={2}"
    # .format(sid, phone_num, Token)
    url = "http://api.sfoxer.com/api/do.php?action=cancelAllRecv&token={0}".format(Token)
    #  url = "http://api.xinheyz.com/api/do.php?action=cancelRecv&sid={0}&phone={1}&token={2}"
    #  .format(sid,phone_num,Token) #项目id 手机号 登录返回的口令
    print(url)
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
    url = "http://api.sfoxer.com/api/do.php?action=getSummary&token={0}".format(Token)
    res = requests.get(url).text
    info = res.split('|')
    # print(res)
    print('您的账户余额为{0}, 等级为{1}, 批量取号数为{2}, 用户类型为{3}'.format(info[1], info[2], info[3], info[4]))


# 获取验证码
def getMessage(Token, sid, phone_num, user_name):
    global text1
    url = "http://api.sfoxer.com/api/do.php?action=getMessage&token={0}&sid={1}&phone={2}".format(Token, sid, phone_num)
    res = requests.get(url)
    i = 1
    while res.text.split("|")[1] == '还没有接收到短信，请过3秒再试':
        msg_get_info = '正在获取短信中，第' + str(i) + '次尝试'
        print(msg_get_info)
        i += 1
        res = requests.get(url)
        text1.insert(tk.END, msg_get_info)
        text1.insert(tk.END, '\n')
        time.sleep(3)
        text1.delete(2.0, 3.0)
    else:
        if res.text.split("|")[0] == '0':
            print(res.text.split("|")[1])
        else:
            print('接收到验证码, 验证码为{}'.format(res.text.split("|")[1]))

    return res.text.split("|")[1]


# 用户窗口
def first():
    top = tk.Tk()
    top.geometry("900x600")
    top.title("阿里鸽鸽 version 1.2 beta版")
    phone_num = 0
    # 用户登录接码码 返回值token
    Token = loginIn()
    # 设置
    sem = threading.Semaphore(1)
    global text1

    def helloCallBack():
        global ph_num, msg_info
        a = 1
        # # 如需获取多个手机号 请将循环条件改为 a < 要获取的手机号数量+1
        while a < 2:
            time.sleep(1)
            # 用户登录接码码 返回值token
            # Token = loginIn()
            # 取手机号  return 手机号
            phone_num = getNumber(Token, sid)
            ph_num = phone_num
            text2.insert(tk.END, ph_num)
            text2.insert(tk.END, '\n')
            # check(phone_num)

            # 检查运营商信息
            temp_url = 'http://mobsec-dianhua.baidu.com/dianhua_api/open/location?tel=' + str(phone_num)
            html_info = requests.get(temp_url).text
            operator_info = json.loads(html_info)['response'][phone_num]['location']
            print('给您提供的手机号为:{0}, 运营商为:{1}'.format(phone_num, operator_info))
            text2.insert(tk.END, operator_info)

            # 获取用户信息
            getSummary(Token)

            # 获取验证码
            msg_info = getMessage(Token, sid, ph_num, user_name)
            if msg_info:
                text1.insert(tk.END, msg_info)
                text1.update()
            # if code:
            #     print("验证码：", code)
            a = a + 1

    def release():

        o_code = cancelAllRecv(sid, phone_num, Token)
        time.sleep(3)
        if o_code[0] == '1':
            print('手机号释放成功!')
            getSummary(Token)
        else:
            print(o_code[1])

    def thread_it(func, *args):
        '''将函数打包进线程'''

        def gothread():
            sem.acquire()
            # print(threading.current_thread().name)
            func()

        # 创建
        t = threading.Thread(target=gothread, args=args)
        # 守护 !!!
        t.setDaemon(True)
        # 启动
        t.start()
        # 阻塞--卡死界面！
        # t.join()

    # Frame
    fm1 = tk.Frame(top, bg='black')
    fm1.titleLabel = tk.Label(fm1, text="阿里鸽鸽接码客户端 1.2版", font=('微软雅黑', 40), fg="white", bg='black')
    fm1.titleLabel.pack()
    fm1.pack(side=tk.TOP, expand=tk.YES, fill='x', pady=5)

    # Grid
    a = tk.Frame(top, height=50, width=200)
    a.pack(side='top', fill='both', expand=True, padx=100)
    button1 = tk.Button(a, text="憨憨，准备接码！！！", command=lambda: thread_it(helloCallBack), font=('微软雅黑', 12),
                        width=20, height=2, bg="yellow")
    button1.grid(row=0, column=0, padx=20)

    text2 = tk.Text(a, width=20, height=5)
    text2.insert(tk.CURRENT, '给您提供的手机号为：\n')
    text2.grid(row=0, column=1, padx=20)

    text1 = tk.Text(a, width=60, height=5)
    text1.insert(tk.CURRENT, '您的验证码相关信息如下：\n')
    text1.grid(row=0, column=2, padx=20)

    button2 = tk.Button(a, text="憨憨，释放手机号吗？？？", command=lambda: thread_it(release), font=('微软雅黑', 12), width=20,
                        height=2, bg="yellow")
    button2.grid(row=2, column=0, pady=50)

    top.mainloop()


if __name__ == "__main__":
    first()
    # Token = loginIn()
    # phone_num = getNumber(Token, sid)
    # check(phone_num)
    # print(phone_num)
    # code = getMessage(Token, sid, phone_num, user_name)
    # print("验证码：", code)
    # o_code = input("请问是否需要释放手机号? 1释放 2不释放:")
    # if o_code == 1:
    #     cancelAllRecv(sid, phone_num, Token)
    # getSummary(Token)
