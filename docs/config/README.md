# 配置账号

!> 为了保护账号信息，所有的账号密匙都打上了*号，使用时请换成自己的账号

打开`init.config`文件，进行配置

```bash
# setting.config(UTF-8)
```

第一句注释是为了声明编码格式，请不要删除该行注释

------



## 账号

```bash
[token]
# 网易云音乐账号（手机号/网易邮箱）
account = 150********

# 密码，明文/MD5,建议自己去MD5在线加密网站给密码加密,然后填到下面
# 明文例如：123456abcd
# MD5例如：efa224f8de55cb668cd01edbccdfc8a9
password = bfa834f7de58cb650ca01edb********

# 国家码，用于国外手机号登陆，国内为86
countrycode = 86
```

`token`区域下存放个人账号信息，`account`存放网易云账号，`password`存放密码，`countrycode`为手机号的国家码

!> 注意，这里密码填写类型与后面的md5开关相关联，具体见后面介绍

------



## 设置

```bash
[setting]
# 开关的选项只有 True 和 False
# 打卡网站的网址，如果失效请提issue：https://github.com/ZainCheung/netease-cloud-api/issues/new
api = https://netease-cloud-api.glitch.me/
```

api是指提供接口的服务器地址，这里提供一个Demo，源码也已经全部开源，如有对项目存在疑问欢迎查看源码，项目地址：[ZainCheung/netease-cloud-api](https://github.com/ZainCheung/netease-cloud-api)

另外想快速拥有一个一模一样的api服务并且使用自己定义的域名，那么可以按照上面项目的教程自己快速搭建

------



### MD5


```bash
# 密码是否需要MD5加密，如果是明文密码一定要打开
# true  需要, 则直接将你的密码（明文）填入password,程序会替你进行加密
# false 不需要, 那就自己计算出密码的MD5，然后填入上面的password内
md5Switch = false
```

md5开关，如果自己不会加密md5，那么将这个开关置为true，并且将你的密码（明文）填入password，程序会为你加密。如果已经知道密码的md5，则将这个开关置为false，将md5填入上面的password内

!> 自己制作MD5时一定要是32位小写！！！

------



### 任务推送

```bash
# 推送方式选择
# 可选参数wxpusher、SCTurbo或留空
# wxpusher: 使用 WxPusher 推送
# SCTurbo: 使用 Server酱Turbo版 推送
# 留空：使用 Server酱免费版 推送或不推送
pushmethod =

# Server酱的密匙,不需要推送就留空
# 免费版密匙的免费申请参考:http://sc.ftqq.com/
# Turbo版的密钥获取:https://sct.ftqq.com/sendkey
# 免费版和Turbo版的密钥长度不一样，请注意检查，不可混用
sckey = SCU97783T70c13167b4daa422f4d419a765eb4ebb5ebc9********

# Wxpusher 推送参数，需要将pushmethod指定为wxpusher，应用和uid的免费申请参考:https://wxpusher.zjiecode.com/
appToken = AT_6kBmt***************************
wxpusheruid = UID_t***************************
```

新版本新增了WxPusher微信推送服务和Server酱的订阅版推送，可通过更改`pushmethod`自行选择推送方式；`sckey`内容为自己申请的Server酱微信推送服务的密钥，分为免费版和订阅版，具体选择看个人需求；`appToken`和`wxpusheruid`都是WxPusher需要的参数，如果推送方式选择了WxPusher则需要配置。

附：Server酱，是一个可以向你的微信推送消息的服务，并且消息内容完全自定义，使用之前只需要前往官网，使用GitHub登陆，扫码绑定微信，便可以获得密匙，从此免费使用Server酱。

------



## 配置多账号

```bash
# 是否开启多账号功能,如果打开将会忽视配置文件里的账号而从account.json中寻找账号信息
# 如果选择使用多账号,请配置好account里的账号和密码,即account和password,而sckey不是必需的,如果为空则不会进行微信推送
# 介于账号安全着想,account.json中的密码必须填写md5加密过的,请不要向他人透露自己的明文密码
peopleSwitch = false
```

这个开关是为那些拥有多账号或者准备带朋友一起使用的朋友准备的，正如注释所说，如果你有多个账号，都想使用这个服务，那么可以打开`peopleSwitch`置为true，那么配置文件里的账号就会被程序忽略，直接读取`account.json`中的账号信息。

第一次打开`account.json`，内容会是这样

```json
[
    {
        "account": "ZainCheung@163.com",
        "password": "10ca5e4c316f81c5d9b56702********",
        "sckey": "SCU97783T70c13167b4daa422f4d419a765eb4ebb5ebc9********",
        "pushmethod": "",
        "appToken": "",
        "wxpusheruid": ""
    },
    {
        "account": "150********",
        "password": "bfa834f7de58cb650ca01edb********",
        "sckey": "SCU97783T70c13167b4daa422f4d419a765eb4ebb5ebc9********",
        "pushmethod": "",
        "appToken": "",
        "wxpusheruid": ""
    },
    {
        "account": "132********",
        "password": "f391235b15781c95384cd5bb********",
        "sckey": "SCU97783T70c13167b4daa422f4d419a765eb4ebb5ebc9********",
        "pushmethod": "",
        "appToken": "",
        "wxpusheruid": ""
    }
]
```

可见里面是一个数组文件，成员为账号对象，对象有六个属性，分别是账号、密码、Server酱密匙，推送方式以及WxPusher所需要的两个配置项。

`pushmethod`留空默认为Server推送；`sckey`留空默认不推送。

不同的账号对应不同的推送方法和相应的密匙，在做完这个账号的任务后会给这个密匙绑定的微信发送消息提醒，如果留空则不提醒，留空也请注意语法，记得加双引号，列举一个正确的案例

```json
[
    {
        "account": "ZainCheung@163.com",
        "password": "10ca5e4c316f81c5d9b56702********",
        "sckey": "",
        "pushmethod": "",
        "appToken": "",
        "wxpusheruid": ""
    },
]
```

可见这里的`sckey`和`pushmethod`都为空，那么完成任务后便不会发送消息提醒，如果不确定是否成功可以查看日志