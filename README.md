# 短信验证码接收API
#### 目前最新版本为3.1版:smile:	
#### Windows用户如需使用源代码请将：
* 364行 


`with open('./dataset/city_sorted.txt', 'r', encoding='gbk') as f1:`


改为 


`with open('.\dataset\city_sorted.txt', 'r', encoding='gbk') as f1:`


* 384行 


`with open('./dataset/province.txt', 'r', encoding='gbk') as f1:`


改为 


`with open('.\dataset\province.txt', 'r', encoding='gbk') as f1:`

## 功能介绍：
Function name  | Description
------------- | -------------
login()  | 输入用户名和密码登录并获取token。
item_selection() | 选取需要接收验证码的项目。
area_selection()  | 选取手机号的归属地。（可能由于号码库未收录该地区而无法满足号码来自所选地点）
SMS_receive()  | 主要功能函数：接收验证码。
release_phone()  | 释放手机号，用于重新接收号码。（收不到验证码或其他原因）
show_userinfo()  | 显示用户的账户余额等信息。

#### 界面预览：

* 登录界面
<img src="https://github.com/Tiangewang0524/sms_verification_code_API/blob/master/dataset/SMS/login.png" width="20%">


* 注册界面
<img src="https://github.com/Tiangewang0524/sms_verification_code_API/blob/master/dataset/SMS/register.png" width="20%">


* 主界面
<img src="https://github.com/Tiangewang0524/sms_verification_code_API/blob/master/dataset/SMS/main_interface.png" width="50%">


* 项目搜索弹窗界面
<img src="https://github.com/Tiangewang0524/sms_verification_code_API/blob/master/dataset/SMS/item_dialog_selection.png" width="40%">

在搜索框中输入你要接收验证码的项目，支持模糊搜索，在结果中选择并确定即可。
<img src="https://github.com/Tiangewang0524/sms_verification_code_API/blob/master/dataset/SMS/item_search.png" width="50%">

* 区域选择界面
<img src="https://github.com/Tiangewang0524/sms_verification_code_API/blob/master/dataset/SMS/area_diglog_selection.png" width="40%">

* 等待接码页面
<img src="https://github.com/Tiangewang0524/sms_verification_code_API/blob/master/dataset/SMS/waitSMS_click.png" width="50%">

* 接码页面（分配江苏地区手机号）
<img src="https://github.com/Tiangewang0524/sms_verification_code_API/blob/master/dataset/SMS/waitSMS_interface.png" width="50%">

* 随机生成地区接码界面
<img src="https://github.com/Tiangewang0524/sms_verification_code_API/blob/master/dataset/SMS/random_area_waitSMS.png" width="50%">

* 释放手机号用于新手机号接码
<img src="https://github.com/Tiangewang0524/sms_verification_code_API/blob/master/dataset/SMS/release_phone.png" width="50%">

## 更新历史：
3.1

* 增加了新用户注册功能。
* 修正了新用户余额不足导致程序无法响应的bug。


3.0

* 界面优化，使主界面更加简洁。
* 对于选项目和归属地，使用弹窗方式替代了之前平铺方式。
* 修正了一些bug。


2.3

* 通过抓取http请求获取到了服务器查询项目列表的URL，添加了项目模糊搜索和选择功能，项目的选择更多了。
* 修正了一些废旧代码，避免过多打开项目搜索弹窗，优化了内存。
* 修正了Mac/Linux环境下，登录框按钮位置显示不正常的bug。


2.2

* 更新了新的接码平台，原平台已跑路。
* 修正了一些废旧代码，更新了方法参数、服务器以及端口号。


2.1

* 修正了不能正确释放手机号的问题。


2.0

* 修正了获取完短信不更新用户余额的bug。
* 增加了省和城市的选择，增加了随机选择号码库任意地区的号码，号码的选择更多了。
* 增加了登录界面。
* 整合成exe文件，可以直接使用。


1.3

* 修正了几处线程相关的可能导致程序卡死崩溃的bug。
* 增加了城市选择，号码的选择更多了。
* 支持多次获取手机号，多次释放手机号。

1.2

* 修正了一处可能导致程序卡死崩溃的bug。
* 更新了界面，获取手机号和短信更加便捷。

1.1

* 修正了不能显示运营商的bug。


1.0

* 多平台，代替客户端使用。
* 可接收市面大部分app和网页的验证码，需提前注册并充值账号后使用用户名和密码登录获得token。
* 自动获取，一次性可获取50个号。
* 获取完可点击释放账号。
* 账号使用完即自动进入服务器黑名单，该app内不会再次使用。

#### prerequisite:

* pip install tkinter
* pip install requests

原phone package因不准确不再使用
