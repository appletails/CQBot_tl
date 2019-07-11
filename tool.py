# -*- coding: utf-8 -*-
import datetime
import json
import codecs
import setting
from modian import getDetail

# 打开json文件


def openjson(path):
    fb = open('jsons/'+path+'.json', 'rb')
    data = json.load(fb)
    fb.close()
    return data

# 写入json文件


def writejson(data, path):
    fb = codecs.open('jsons/'+path+'.json', 'w', 'utf-8')
    fb.write(json.dumps(data, indent=4, ensure_ascii=False))
    fb.close()

# ----------------------------------今日集资-------------------------------

# 今日集资


def today(seatime):
    top = '今日目前集资情况：\n\n'
    msg = ''  # 定义返回信息
    money = 0  # 定义总集资
    end = "\n今日累计集资"  # 定义结束语
    proId = openjson('ini')['modian']['pro_id'][0]
    # 获取集资起始时间（今天0点）和结束时间（明天0点）
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    # 获取当前时间的日期
    if seatime == "昨日集资":
        tomorrow = today
        today = today - datetime.timedelta(days=1)
        end = "\n昨日累计集资"
        top = '昨日集资情况：\n\n'
    elif seatime == "定时播报":
        top = ''
    # 讲两个日期转换为时间戳
    today = setting.timeStamp(str(today)+" 00:00:00")
    tomorrow = setting.timeStamp(str(tomorrow)+" 00:00:00")
    # 打开本地库
    alldata = openjson("order/"+str(proId))
    # 开始循环本地库
    for j in alldata:
        # 转换订单的时间为时间戳
        timess = setting.timeStamp(j["pay_success_time"])
        # 判断订单时间是否在区域时间内
        if timess >= today and timess <= tomorrow:
            msg = msg + j["pay_success_time"] + "  " + \
                j["nickname"] + "  ￥" + str(j["backer_money"]) + "\n"
            money = money + j["backer_money"]
    # 配置文案   注释部分为带有倒计时的播报
    # msg = top + msg + end + " ￥" + str(round(money,2)) + "\n" + setting.timeCount()
    msg = top + msg + end + " ￥" + str(round(money, 2))
    return msg

# ----------------------------------今日集资-------------------------------


# ----------------------------------接力部分-------------------------------
def relay(relay):  # relay 参数为集资金额
    # 打开数据缓存到data
    data = openjson('tool/tool')
    msg = ""
    if not(data["relay"]["state"]):
        return msg
    else:
        money = data["relay"]["money"]
        relay = int(relay/money)
        data["relay"]["stick"] = data["relay"]["stick"] + relay
        msg = "\n\n此次追加了" + str(relay) + "棒，目前已有" + \
            str(data["relay"]["stick"]) + "棒"

        writejson(data, "tool/tool")
        return msg

# 开启接力


def relayOpen(context):
    data = openjson('tool/tool')
    msg = ""
    # 判断当前接力是否开启
    if data["relay"]["state"]:
        if context == "开启接力":
            msg = "接力当前已开启，不能重复开启"

        elif context == "关闭接力":
            data["relay"]["num"] = data["relay"]["stick"]
            data["relay"]["state"] = False
            data["relay"]["stick"] = 0
            data["relay"]["money"] = 0
            data["relay"]["nickname"] = "匿名聚聚"
            msg = "接力已关闭，棒数与金额已清空"

        elif "接力金额" in context and context[0:5] == "接力金额 ":
            money = context.split()
            money = money[1]
            data["relay"]["money"] = round(float(money), 2)
            msg = "接力金额设置成功，当前" + str(money) + "元一棒"

    # 接力未开启状态下的对应
    else:
        if context == "开启接力":
            data["relay"]["state"] = True
            msg = "接力当前已开启，可通过【接力金额 money】指令来设置每一棒的金额"

        elif context == "关闭接力":
            msg = "接力已关闭，不可重复关闭"

        elif "接力金额" in context and context[0:5] == "接力金额 ":
            msg = "接力关闭状态不可操作"

    writejson(data, "tool/tool")
    return msg


def relayNum():
    data = openjson('tool/tool')
    if data["relay"]["state"]:
        msg = "当前已接力" + str(data["relay"]["stick"]) + "棒"
    else:
        msg = "接力尚未开启"
    return msg


def addNum(num):
    data = openjson('tool/tool')
    if data["relay"]["state"]:
        nums = data["relay"]["stick"]
        data["relay"]["stick"] = nums + int(num[3:])
        writejson(data, "tool/tool")
        msg = '手动追加成功，当前' + str(data["relay"]["stick"]) + '棒'
    else:
        msg = "接力尚未开启"
    return msg

# ----------------------------------接力部分-------------------------------

# ----------------------------------pk部分-------------------------------

# 23515 23514 23513 23517


def showPk(val=""):
    msg = ""
    data = setting.openjson("ini")
    status = data["pk"]["status"]
    # 获取pk的pid数组
    pkList = data["pk"]["list"]
    if not(status) or pkList == []:
        return msg
    elif not(data['modian']['pk']):
        return '请先设置pkid【pkid pro_id】'
    else:  # 开始pk部分
        # 设置title
        msg = val
        # 初始化名次
        n = 1
        ind = 1
        pkIdlist = []
        # 获取全部的pid配置成可查询的结构
        for item in pkList:
            pkIdlist.extend(item)
        pkIdlist = ",".join(str(item) for item in pkIdlist)
        # 查询全部的pid项目进度
        pkData = getDetail(pkIdlist)["data"]
        # 新建项目内容
        newPk = []
        # 首先循环分组
        for itemList in pkList:
            itemCont = {
                "money": 0,
                "list": []
            }
            for item in itemList:
                # 过滤出当先id的项目信息
                cont = list(
                    filter(lambda x: x["pro_id"] == str(item), pkData))[0]
                # 设置当前的内容
                idolCont = {
                    "name": reduce(cont['pro_name'], cont["pro_id"]),  # 简化成员id
                    "money": cont["already_raised"]
                }
                itemCont["money"] = round(
                    cont["already_raised"]+itemCont["money"], 2)
                itemCont["list"].append(idolCont)
            newPk.append(itemCont)

        # 对现有的数据进行排序
        newPk = sorted(newPk, key=lambda ready: ready["money"], reverse=True)
        for item in newPk:
            item["list"] = sorted(
                item["list"], key=lambda ready: ready["money"], reverse=True)

        # 配置文案
        for j, item in enumerate(newPk):
            if j > 0:
                # print(newPk[j-1]["money"],newPk[j]["money"])
                cha1 = round((newPk[j-1]["money"] - newPk[j]["money"]), 2)
                msg += "\n\n第%s小队：￥%s 与上一小队相差 ￥%s" % ( str(ind), str(item["money"]), str(cha1))
            else:
                msg += "\n\n第%s小队：￥%s" % (str(ind), str(item["money"]))
            for i, idol in enumerate(item["list"]):
                if i > 0:
                    cha2 = round( (item["list"][i-1]["money"] - item["list"][i]["money"]), 2)
                    msg += "\nNo.%s %s ￥%s 与上一名相差 ￥%s" % ( str(n), idol["name"], str(idol["money"]), str(cha2))
                else:
                    msg += "\nNo.%s %s ￥%s" % (str(n), idol["name"], str(idol["money"]))
                n += 1
            n = 1
            ind += 1
        return msg

# 简化昵称


def reduce(name, pid):
    idol = setting.openjson("tool/idol")
    for item in idol:
        if item in name:
            return item
    return name

# 开启关闭pk


def changePK(cont):
    msg = ""
    data = setting.openjson("ini")
    if data["pk"]["status"]:
        if cont == "开启pk":
            msg = "开启状态不可重复开启"
        elif cont == "关闭pk":
            data["pk"]["status"] = False
            data["pk"]["list"] = []
            data["modian"]["pk"] = ''
            msg = "已关闭并清除pk项目列表"
    else:
        if cont == "开启pk":
            data["pk"]["status"] = True
            msg = "开启成功，通过【pkid Pro_id】设置pkid\n通过【pk项目 Pro_id,Pro_id Pro_id,Pro_id Pro_id,Pro_id ...】设置pk列表"
        elif cont == "关闭pk":
            msg = "关闭状态不可关闭"
    setting.writejson(data, "ini")
    return msg


def addPk(cont):
    msg = "添加pk项目成功"
    pkList = cont[5:].split(" ")
    # 将pidlist合并成可执行变量
    hasList = ",".join(pkList)
    pkData = getDetail(hasList)
    if pkData["status"] == "2":
        msg = pkData['message']
    else:
        data = setting.openjson("ini")
        data["pk"]["list"] = []
        for item in pkList:
            data["pk"]["list"].append(item.split(","))
        setting.writejson(data, "ini")
    return msg
