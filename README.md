# SJTUAppointment

基于 python selenium 实现的SJTU体育场馆自动预约脚本

## 实现思路

python 的 selenium 库可以方便地利用id、class、css来定位元素定位，模拟预约的点击操作。交大基本体育场馆的预约流程为：
1. 打开上海交通大学体育场馆预约平台 https://sports.sjtu.edu.cn/
2. 输入jaccount账号与密码，识别图形验证码，点击登录
3. 选择场馆(Venue)、细分项目(VenueItem)、日期、时间(Time)
4. 如果有空余场地，则点击预约按钮，确认预约; 如果没有就刷新网页继续检测
5. 若成功预约则发消息给手机，提醒用户付款

利用 selenium 库实现以上操作即可。

## 环境配置(Anaconda)

python环境配置
```
conda create -n sjtu python=3.8
```

安装对应的包
```
conda activate sjtu
pip install selenium
pip install pillow
pip install pytesseract
pip install requests
```

安装与浏览器对应版本的 webDriver (以Firefox为例)
- 下载地址 https://github.com/mozilla/geckodriver/releases

安装 tesseract-ocr，用于识别图形验证码
- 下载地址 https://digi.bib.uni-mannheim.de/tesseract/

## 使用方式

首先在`SJTUAppointment/config.py`中设定个人的jaccount账号与密码。之后可在`SJTUAppointment/SJTUVenueTabLists.py`中查看各个场馆及其细分项目，选择自己需要预约的场馆和项目。

以下提供了2种预约方式：

1、**使用命令行参数进行预约**
```
python main.py --venue '气膜体育中心' --venueItem '羽毛球' --date '[2,3]' --time '[19,21]' --head
```

2、**使用json配置文件进行预约**
```
python main.py --json template.json --head
```

> 若要开启无头模式则可去掉参数 `--head`

抢到场地通知方式

1、**方糖API**：一个用python给微信发送信息的API，可以通过注册登录获取AppKey，然后将AppKey填入`SJTUAppointment/config.py`中的`FANGTANG_KEY`变量中
- API地址 https://sct.ftqq.com/

## 问题与改进方向

- selenium 库框架相当于模拟浏览器的各种操作，它的请求发送速度和响应速度都比较慢，所以在抢羽毛球这样的热门场地时并不占优势。
- selenium 使用时会很占电脑资源，所以这个脚本其实并不适合部署在服务器上长时间运行。
- 之后会基于HTTP协议写一个更快速轻量的抢场地脚本。

## 致谢

> 感谢以下项目作者:
> - [**ifarewell/jAutoVenue**](https://github.com/ifarewell/jAutoVenue)
> - [**PhotonQuantum/jaccount-captcha-solver**](https://github.com/PhotonQuantum/jaccount-captcha-solver)