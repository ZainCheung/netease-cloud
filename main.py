#coding:utf-8
'''
@author: ZainCheung
@LastEditors: ZainCheung
@description:网易云音乐全自动每日打卡300首歌升级账号等级,使用前请先到init.config文件配置
@Date: 2020-06-25 14:28:48
@LastEditTime: 2020-09-01 18:20:00
'''
from configparser import ConfigParser
from threading import Timer
import requests 
import random
import hashlib
import datetime
import time
import json
import logging
import math
import os

'''
使用绝对路径时，切换到项目的当前目录。
'''
os.chdir(os.path.dirname(os.path.abspath(__file__)))
logFile = open("run.log", encoding="utf-8", mode="a")
logging.basicConfig(stream=logFile, format="%(asctime)s %(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
grade = [10,40,70,130,200,400,1000,3000,8000,20000]
api = ''

class Task(object):
    
    '''
    对象的构造函数
    '''

    def __init__(self, uin, pwd, pushmethod, sckey, appToken, wxpusheruid, barkServer, barkKey, countrycode):
        self.uin = uin
        self.pwd = pwd
        self.countrycode = countrycode
        self.pushmethod = pushmethod
        self.sckey = sckey
        self.appToken = appToken
        self.wxpusheruid = wxpusheruid
        self.barkServer = barkServer
        if barkServer == "":
            self.barkServer = "https://api.day.app"
        self.barkKey = barkKey
    '''
    带上用户的cookie去发送数据
    url:完整的URL路径
    postJson:要以post方式发送的数据
    返回response
    '''
    def getResponse(self, url, postJson):
        response = requests.post(url, data=postJson, headers={'Content-Type':'application/x-www-form-urlencoded'},cookies=self.cookies)
        return response

    '''
    登录
    '''
    def login(self):
        data = {"uin":self.uin,"pwd":self.pwd,"countrycode":self.countrycode,"r":random.random()}
        if '@' in self.uin:
            url = api + '?do=email'
        else:
            url = api + '?do=login'
        response = requests.post(url, data=data, headers={'Content-Type':'application/x-www-form-urlencoded'})
        code = json.loads(response.text)['code']
        self.name = json.loads(response.text)['profile']['nickname']
        self.uid = json.loads(response.text)['account']['id']
        if code==200:
            self.error = ''
        else:
            self.error = '登录失败，请检查账号'
        self.cookies = response.cookies.get_dict()
        self.log('登录成功')
        logging.info("登录成功")

    '''
    每日签到
    '''
    def sign(self):
        url = api + '?do=sign'
        response = self.getResponse(url, {"r":random.random()})
        data = json.loads(response.text)
        if data['code'] == 200:
            self.log('签到成功')
            logging.info('签到成功')
        else:
            self.log('重复签到')
            logging.info('重复签到')

    '''
    每日打卡300首歌
    '''
    def daka(self):
        url = api + '?do=daka'
        response = self.getResponse(url, {"r":random.random()})
        self.log(response.text)

    '''
    查询用户详情
    '''
    def detail(self):
        url = api + '?do=detail'
        data = {"uid":self.uid, "r":random.random()}
        response = self.getResponse(url, data)
        data = json.loads(response.text)
        self.level = data['level']
        self.listenSongs = data['listenSongs']
        self.log('获取用户详情成功')
        logging.info('获取用户详情成功')


    '''
    Wxpusher推送
    '''
    def wxpusher(self):
        if (self.appToken == '' or self.wxpusheruid == ''):
            self.log('未填写WxPusher推送所需参数，请检查')
            logging.info('未填写WxPusher推送所需参数，请检查')
            return
        self.diyText() # 构造发送内容
        url = 'https://wxpusher.zjiecode.com/api/send/message/'
        data = json.dumps({
            "appToken":self.appToken,
            "content":self.content,
            "summary":self.title,
            "contentType":3,
            "uids":[self.wxpusheruid]
        })
        response = requests.post(url, data = data, headers = {'Content-Type': 'application/json;charset=UTF-8'})
        if (response.json()['data'][0]['status']) == '创建发送任务成功':
            self.log('用户:' + self.name + '  WxPusher推送成功')
            logging.info('用户:' + self.name + '  WxPusher推送成功')
        else:
            self.log('用户:' + self.name + '  WxPusher推送失败,请检查appToken和uid是否正确')
            logging.info('用户:' + self.name + '  WxPusher推送失败,请检查appToken和uid是否正确')

    '''
    Bark推送
    '''
    def bark(self):
        if self.barkServer == '' or self.barkKey == '':
            self.log('未填写Bark推送所需参数，请检查')
            return
        self.diyText()  # 构造发送内容
        url = self.barkServer+'/push'
        data = json.dumps({
            "title": self.title,
            "body": self.content,
            "device_key": self.barkKey,
            "ext_params": {"group": "网易云签到"}
        })
        response = requests.post(url, data=data, headers={'Content-Type': 'application/json;charset=UTF-8'})
        if (response.json()['message']) == 'success':
            self.log('用户:' + self.name + '  Bark推送成功')
        else:
            self.log('用户:' + self.name + '  bark推送失败,请检查appToken和uid是否正确')

    '''
    自定义要推送到微信的内容
    title:消息的标题
    content:消息的内容,支持MarkDown格式
    contentType:消息类型,1为普通文本,2为html,3为markdown
    '''

    '''
    Server推送
    '''
    def server(self):
        if self.sckey == '':
            return
        self.diyText() # 构造发送内容
        data = {
            "text":self.title,
            "desp":self.content
        }
        if (self.pushmethod.lower() == 'scturbo'):      #Server酱 Turbo版
            url = 'https://sctapi.ftqq.com/' + self.sckey + '.send'
            response = requests.post(url, data=data, headers = {'Content-type': 'application/x-www-form-urlencoded'})
            errno = response.json()['data']['errno']
        else:                                           #Server酱 普通版
            url = 'http://sc.ftqq.com/' + self.sckey + '.send'
            response = requests.post(url, data=data, headers = {'Content-type': 'application/x-www-form-urlencoded'})
            errno = response.json()['errno']
        if errno == 0:
            self.log('用户:' + self.name + '  Server酱推送成功')
            logging.info('用户:' + self.name + '  Server酱推送成功')
        else:
            self.log('用户:' + self.name + '  Server酱推送失败,请检查sckey是否正确')
            logging.info('用户:' + self.name + '  Server酱推送失败,请检查sckey是否正确')

    '''
    自定义要推送到微信的内容
    title:消息的标题
    content:消息的内容,支持MarkDown格式
    '''

    def diyText(self):
        # today = datetime.date.today()
        # kaoyan_day = datetime.date(2020,12,21) #2021考研党的末日
        # date = (kaoyan_day - today).days
        for count in grade:
            if self.level < 10:
                if self.listenSongs < 20000:
                    if self.listenSongs < count:
                        self.tip = '还需听歌' + str(count-self.listenSongs) + '首即可升级'
                        break
                else:
                    self.tip = '你已经听够20000首歌曲,如果登录天数达到800天即可满级'
            else:
                self.tip = '恭喜你已经满级!'
        if self.error == '':
            state = ("- 目前已完成签到\n"
                     "- 今日共打卡" + str(self.dakanum) + "次\n"
                     "- 今日共播放" + str(self.dakaSongs) + "首歌\n"
                     "- 还需要打卡" + str(self.day) +"天")
            self.title = ("网易云今日打卡" + str(self.dakaSongs) + "首，已播放" + str(self.listenSongs) + "首")
        else:
            state = self.error
            self.title = '网易云听歌任务出现问题！'
        self.content = (
            "------\n"
            "#### 账户信息\n"
            "- 用户名称：" + str(self.name) + "\n"
            "- 当前等级：" + str(self.level) + "级\n"
            "- 累计播放：" + str(self.listenSongs) + "首\n"
            "- 升级提示：" + self.tip + "\n\n"
            "------\n"
            "#### 任务状态\n" + str(state) + "\n\n"
            "------\n"
            "#### 注意事项\n- 网易云音乐等级数据每天下午2点更新 \n\n"
            "------\n"
            "#### 打卡日志\n" + self.dakaSongs_list + "\n\n")

    '''
    打印日志
    '''
    def log(self, text):
        time_stamp = datetime.datetime.now()
        print(time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + '   ' + str(text))
        self.time =time_stamp.strftime('%H:%M:%S')
        self.list.append("- [" + self.time + "]    " + str(text) + "\n\n")

    '''
    开始执行
    '''
    def start(self):
        try:
            self.list = []
            self.list.append("- 初始化完成\n\n")
            self.login()
            self.sign()
            self.detail()
            counter  = self.listenSongs
            self.list.append("- 开始打卡\n\n")
            for i in range(1, 10):
                self.daka()
               # self.log('用户:' + self.name + '  第' + str(i) + '次打卡成功,即将休眠30秒')
                self.log('第' + str(i) + '次打卡成功')
                logging.info('用户:' + self.name + '  第' + str(i) + '次打卡成功,即将休眠10秒')
                time.sleep(10)
                self.dakanum =i
                self.detail()
                self.dakaSongs = self.listenSongs - counter
                self.log('今日已打卡' + str(self.dakaSongs) + '首')
                if self.dakaSongs == 300:
                    break

            if self.listenSongs >= 20000:
                self.day = 0
            else:
                self.day = math.ceil((20000 - self.listenSongs)/300)
            
            self.list.append("- 打卡结束\n\n")
            self.list.append("- 消息推送\n\n")
            self.dakaSongs_list = ''.join(self.list)
            if self.pushmethod.lower() == 'wxpusher':
                self.wxpusher()
            elif self.pushmethod.lower() == 'bark':
                self.bark()
            else:
                self.server()
        except:
            self.log('用户任务执行中断,请检查账号密码是否正确')
            logging.error('用户任务执行中断,请检查账号密码是否正确========================================')
        else:
            self.log('用户:' + self.name + '  今日任务已完成')
            logging.info('用户:' + self.name + '  今日任务已完成========================================')
            
        
'''
初始化：读取配置,配置文件为init.config
返回字典类型的配置对象
'''
def init():
    global api # 初始化时设置api
    config = ConfigParser()
    config.read('init.config', encoding='UTF-8-sig')
    uin = config['token']['account']
    pwd = config['token']['password']
    countrycode = config['token']['countrycode']
    api = config['setting']['api']
    md5Switch = config.getboolean('setting','md5Switch')
    peopleSwitch = config.getboolean('setting','peopleSwitch')
    pushmethod = config['setting']['pushmethod']
    sckey = config['setting']['sckey']
    appToken = config['setting']['appToken']
    wxpusheruid = config['setting']['wxpusheruid']
    barkServer = config['setting']['barkServer']
    barkKey = config['setting']['barkKey']
    print('配置文件读取完毕')
    logging.info('配置文件读取完毕')
    conf = {
            'uin': uin,
            'pwd': pwd,
            'countrycode': countrycode,
            'api': api,
            'md5Switch': md5Switch, 
            'peopleSwitch':peopleSwitch,
            'pushmethod':pushmethod,
            'sckey':sckey,
            'appToken':appToken,
            'wxpusheruid':wxpusheruid,
            'barkServer':barkServer,
            'barkKey':barkKey
        }
    return conf

'''
MD5加密
str:待加密字符
返回加密后的字符
'''
def md5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()

'''
加载Json文件
jsonPath:json文件的名字,例如account.json
'''
def loadJson(jsonPath):
    with open(jsonPath,encoding='utf-8') as f:
        account = json.load(f)
    return account

'''
检查api
'''
def check():
    url = api + '?do=check'
    respones = requests.get(url)
    if respones.status_code == 200:
        print('api测试正常')
        logging.info('api测试正常')
    else:
        print('api测试异常')
        logging.error('api测试异常')

'''
任务池
'''
def taskPool():
    
    config = init()
    check() # 每天对api做一次检查
    if config['peopleSwitch'] is True:
        print('多人开关已打开,即将开始执行多人任务')
        logging.info('多人开关已打开,即将执行进行多人任务')
        account = loadJson("account.json")
        for man in account:
            print('账号: ' + man['account'] + '  开始执行')
            logging.info('账号: ' + man['account'] + '  开始执行========================================')
            task = Task(man['account'], man['password'], man['pushmethod'], man['sckey'], man['appToken'], man['wxpusheruid'], man['barkServer'], man['barkKey'], man['countrycode'])
            task.start()
            time.sleep(10)
        print('所有账号已全部完成任务,服务进入休眠中,等待明天重新启动')
        logging.info('所有账号已全部完成任务,服务进入休眠中,等待明天重新启动')
    else :
        print('账号: ' + config['uin'] + '  开始执行')
        logging.info('账号: ' + config['uin'] + '  开始执行========================================')
        if config['md5Switch'] is True:
            print('MD5开关已打开,即将开始为你加密,密码不会上传至服务器,请知悉')
            logging.info('MD5开关已打开,即将开始为你加密,密码不会上传至服务器,请知悉')
            config['pwd'] = md5(config['pwd'])
        task = Task(config['uin'], config['pwd'], config['pushmethod'], config['sckey'], config['appToken'], config['wxpusheruid'], config['barkServer'], config['barkKey'], config['countrycode'])
        task.start()

'''
程序的入口
'''
if __name__ == '__main__':
    while True:
        Timer(0, taskPool, ()).start()
        time.sleep(60*60*24) # 间隔一天
