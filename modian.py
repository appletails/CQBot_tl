# -*- coding: utf-8 -*-
import setting
import requests
import urllib
import hashlib
import time
from CQLog import INFO, WARN
import card


# -------------------------------
# init
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}


# 计算签名
def getSign(ret):
    # 将字典按键升序排列，返回一个元组tuple
    tuple = sorted(ret.items(), key=lambda e: e[0], reverse=False)
    md5_string = urllib.parse.urlencode(tuple).encode(
        encoding='utf_8', errors='strict')
    md5_string += b'&p=das41aq6'
    # md5计算 & 十六进制转化 & 根据规则从第6位开始取16位
    sign = hashlib.md5(md5_string).hexdigest()[5: 21]
    return sign


# page从1开始，每页最多20条数据


# 项目订单查询
def getOrders(pro_id, page):
    url = 'https://wds.modian.com/api/project/orders'
    form = {
        'page': page,
        'pro_id': pro_id
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    return response


# 20180613API更新，增加自定义订单排序
# sort_by = 1 按支付时间倒序
# sort_by = 0 按下单时间倒序
def sorted_orders(pro_id, page, sort_by=1):
    url = 'https://wds.modian.com/api/project/sorted_orders'
    form = {
        'page': page,
        'pro_id': pro_id,
        'sort_by': sort_by
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    return response

# 项目聚聚榜查询
# type = 1 聚聚榜
# type = 2 打卡榜
def getRankings(pro_id, type, page):
    url = 'https://wds.modian.com/api/project/rankings'
    form = {
        'page': page,
        'pro_id': pro_id,
        'type': type
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    return response


# 项目筹款结果查询
# 查询多个项目用逗号分隔，如getDetail(10250,10280)
def getDetail(*pro_id):
    # 将pro_id（一个元组）中int元素转为str元素，用逗号拼接成字符串
    pro_id_str = ','.join(map(str, pro_id))
    url = 'https://wds.modian.com/api/project/detail'
    form = {
        'pro_id': pro_id_str
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    return response


# init end
# ---------------------------------
# func


def md_init(proid_array):
    array = []
    for id in proid_array:
        dict = {}
        dict['pro_id'] = int(id)
        id_url = 'https://zhongchou.modian.com/item/%d.html' % int(id)
        try:
            dict['url_short'] = setting.get_short_url(id_url)
        except:
            dict['url_short'] = 'https://m.modian.com/project/%d.html' % int(id)
        dict['url_long'] = 'https://m.modian.com/project/%d.html' % int(id)
        detail = getDetail(id)
        dict['name'] = detail['data'][0]['pro_name']
        dict['left_time'] = detail['data'][0]['left_time']
        array.append(dict)
    return array


# rank
def rank(type):
    msg_array = []
    err = False
    err_msg = '返回rank错误\n'
    pro_id_array = md_init(setting.pro_id())
    for pro_id_dict in pro_id_array:
        msg = ''
        detail = getDetail(pro_id_dict['pro_id'])
        # type=1:总额榜
        if type == 1:
            msg = msg + pro_id_dict['name'] + '·聚聚榜TOP20\n' + '------------\n'
            dic = getRankings(pro_id_dict['pro_id'], 1, 1)
            if int(dic['status']) == 0:
                for data in dic['data']:
                    msg = msg + '【第' + \
                        str(data['rank']) + '名】: ' + data['nickname'] + \
                        '支持了' + str(data['backer_money']) + '元\n'
            elif int(dic['status']) == 2:
                err = True
                err_msg += dic['message']
        elif type == 2:
            msg = msg + pro_id_dict['name'] + '·打卡榜TOP20\n' + '------------\n'
            dic = getRankings(pro_id_dict['pro_id'], 2, 1)
            if int(dic['status']) == 0:
                for data in dic['data']:
                    msg = msg + '【第' + \
                        str(data['rank']) + '名】: ' + data['nickname'] + \
                        '已打卡' + str(data['support_days']) + '天\n'
            elif int(dic['status']) == 2:
                err = True
                err_msg += dic['message']
        msg = msg + '------------\n【摩点】：' + pro_id_dict['url_short'] + '\n目前集资进度：¥' +\
            str(detail['data'][0]['already_raised']) + '\n目标：¥' +\
            detail['data'][0]['goal']
        msg_array.append(msg)
    if err is True:
        WARN("modian rank error", err_msg)
        return err_msg
    elif err is False:
        return msg_array


def result(pro_id_array):
    msg_array = []
    for pro_id in pro_id_array:
        response = getDetail(pro_id)
        msg = ''
        msg += response['data'][0]['pro_name'] + '\n' + \
            '项目进度：' + str(response['data'][0]['already_raised']) + '/' + response['data'][0]['goal'] + \
            '\n结束时间：' + response['data'][0]['end_time'] + \
            '\n参与人数：' + str(response['data'][0]['backer_count']) + '人'
        msg_array.append(msg)
    return msg_array

import tool
def newOrder(stamp10, secondsDelay):
    msgDict_array = []
    pro_id_array = md_init(setting.pro_id(0))
    for pro_id_dict in pro_id_array:
        newOrders = []
        # 获取一次订单信息，返回一个dictionary
        orderDict = sorted_orders(pro_id_dict['pro_id'], 1)
        # 查询失败则返回错误信息
        if int(orderDict['status']) == 2:
            WARN("modian newOrder error", "获取订单错误", orderDict['message'])
            print(orderDict['message'])
            return msgDict_array
        # 20180319,防止空订单，循环查询五次
        retry = 0
        while not len(orderDict['data']):
            INFO("modian newOrder info", "疑似空订单")
            orderDict = sorted_orders(pro_id_dict['pro_id'], 1)
            retry += 1
            if retry > 5:
                INFO("modian newOrder info", "订单5次为空，判断为无人集资")
                break

        # 不具备本地order.josn的写法  查询成功，遍历摩点库
        # for data in orderDict['data']:
        #     pay_success_time = data['pay_success_time']
        #     # 将字符串时间转换为unix时间戳
        #     data['pay_success_time'] = int(time.mktime(time.strptime(pay_success_time, '%Y-%m-%d %H:%M:%S')))
        #     # 筛选订单时间在查询时间前的设定时间段之间的订单
        #     if data['pay_success_time'] >= stamp10 - secondsDelay and data['pay_success_time'] < stamp10:
        #         newOrders.append(data)

        # ------ 20180723具备本地order.json的写法 ------
        # 获得本地库
        data = setting.openjson("order/"+str(pro_id_dict['pro_id']))
        # 判断本地库是都为空
        if data == []:
            newOrders = orderDict["data"]
        else:
            # 获得摩点库
            alldata = orderDict["data"]
            # 对摩点库进行排序
            alldata = setting.sortOrder(alldata)
            # 与本地库对比
            if alldata[0]["pay_success_time"] == data[0]["pay_success_time"]:
                pass
            else:
                print("发现遗漏订单" + str(pro_id_dict['pro_id']))
                # 获取本地库第一个订单的时间转换为时间戳
                oneTime = int(time.mktime(time.strptime(
                    data[0]["pay_success_time"], '%Y-%m-%d %H:%M:%S')))
                # 循环摩点接口所有订单
                for i in range(len(alldata)):
                    # 将摩点订单时间转换为时间戳
                    iTime = int(time.mktime(time.strptime(
                        alldata[i]["pay_success_time"], '%Y-%m-%d %H:%M:%S')))
                    # 在摩点库中找到本地最新的那一个订单
                    if iTime == oneTime:
                        for j in range(i):
                            newOrders.append(alldata[j])
        data = newOrders + data
        setting.writejson(data, "order/"+str(pro_id_dict['pro_id']))

        # 有新订单
        msgDict = []
        if newOrders:
            # 获取项目信息
            detail = getDetail(pro_id_dict['pro_id'])
            # 查询失败则返回错误信息
            if int(detail['status']) == 2:
                WARN("modian newOrder error", "获取项目信息错误", detail['message'])
                # return detail['message']
            # 查询成功，初始化消息
            msg = ''
            for newOrder in newOrders:
                msg = "ID：" + newOrder['nickname'] + "\n" +\
                    "金额：¥ " + str(newOrder['backer_money']) + '\n' +\
                    "项目：" + pro_id_dict['name'] + "\n" +\
                    "链接：" + pro_id_dict['url_short'] + "\n" +\
                    "感谢"+newOrder['nickname']+"对" + setting.idol_name() + "的支持呦~\n" + \
                    tool.relay(newOrder['backer_money']) +\
                    card.DrawCard(newOrder["user_id"],newOrder["nickname"],newOrder["backer_money"])
                if str(pro_id_dict['pro_id']) == str(setting.openjson('ini')['modian']['pk']) or (setting.openjson('ini')['pk']['status'] and not(setting.openjson('ini')['modian']['pk'])):
                    msg += tool.showPk("\n\npk实况：")

                msgDict.append(msg)
        msgDict_array.append(msgDict)
    return msgDict_array
