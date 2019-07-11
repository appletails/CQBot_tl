# -*- coding: utf-8 -*-
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import codecs
import datetime
import time

# ------------------------usersetting-------
# 打开json文件
def openjson(path):
	fb = open('jsons/'+path+'.json','rb')
	data = json.load(fb)  
	fb.close()
	return data

# 写入json文件
def writejson(data,path):
	fb = codecs.open('jsons/'+path+'.json','w', 'utf-8')  
	fb.write(json.dumps(data,indent=4,ensure_ascii=False))  
	fb.close()

# 将日期转换为时间戳
def timeStamp(dt):
    timeStamp = time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S"))
    return timeStamp

# 将时间轴转换时间格式(2016-05-05 20:28:54)
def timeDate(dt):
	timeDate = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(dt))
	return timeDate
# ----------------------摩点微打赏设置----------------------

# 摩点项目对应pro_id
def idol_name():
    data = openjson('ini')
    idolName = data['modian']['idol']
    return (idolName)

# 摩点项目对应pro_id
def pro_id(i = 1):
    data = openjson('ini')
    array = data['modian']['pro_id']
    if data['modian']['pk']:
        if i:
            return [data['modian']['pk']]
        else:
            array.append(data['modian']['pk'])
    return (array)
# 摩点查询时间间隔读取
def md_interval():
    data = openjson('ini')
    interval = data['modian']['interval']
    return int(interval)

# ----------------------qq群设置----------------------

# qq群id
def groupid():
    data = openjson('ini')
    id = data['QQqun']['id']
    return id

# 欢迎信息
def welcome():
    data = openjson('ini')
    welcome = data['QQqun']['welcome']
    msg = welcome.replace('\\n', '\n')
    return msg


# 关键词触发
# 禁言关键词,留空则无禁言
def shutup():
    data = openjson('ini')
    shutword = data['QQqun']['shutword']
    return shutword


# --------------------------------------------------------
# ----------------------微博设置----------------------


# 手机网页版微博地址
def weibo_url():
    data = openjson('ini')
    weibo_url = data['weibo']['weiboURL']
    return str(weibo_url)


# weibo container id
def weibo_id():
    data = openjson('ini')
    weibo_id = data['weibo']['weiboID']
    return int(weibo_id)


# weibo房间查询时间间隔读取
def wb_interval():
    data = openjson('ini')
    interval = data['weibo']['interval']
    return int(interval)


# --------------------------------------------------------

# ---------------------长网址转短网址----------------------------


def get_short_url(long_url_str):
    url = 'http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=' + str(long_url_str)
    response = requests.get(
        url,
        verify=False
        ).json()
    # print(response)
    return response[0]['url_short']


# -------------------------------------------------------

# 倒计时
def timeCount(year=2018,month=10,days=29,hour=0,min=0,sce=0):
    times = time.strftime('%Y %m %d %H %M %S',time.localtime(time.time()))
    times = times.split( )
    start = datetime.datetime(int(times[0]),int(times[1]),int(times[2]),int(times[3]),int(times[4]),int(times[5]))
    end = datetime.datetime(year,month,days,hour,min,sce)
    day = str(end-start)
    msg = ("距离%s年%s月%s日还有" % (year,month,days))
    if "days," in day:
        day = day.split( )
        del day[1]
        day[1] = day[1].split(":")
        msg = msg + day[0] + "天" + day[1][0] + "小时" + str(int(day[1][1])) + "分钟" + str(int(day[1][2])) + "秒"
    else:
        day = day.split(":")
        msg = msg + "0天" + day[0] + "小时" + str(int(day[1])) + "分钟" + str(int(day[2])) + "秒"
    return msg

# 摩点库排序
def sortOrder(data):
    for item in data:
        item["pay_success_time"] = timeStamp(item["pay_success_time"])
    data = sorted(data,key = lambda data:data["pay_success_time"] , reverse = True)
    for item in data:
        item["pay_success_time"] = timeDate(item["pay_success_time"])
    return data