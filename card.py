# -*- coding: utf-8 -*-
import random
import setting
import os

# 缓存一个绑定的对应表
binds = setting.openjson('user/bind')
ini = setting.openjson('ini')
cardPath = ini['cardPath']
idolPath = ini['idolPath']
childPath = ini['childPath']
oneCard = ini['oneCard']
# print(bind)
# 最终调用的抽卡函数
def DrawCard(user_id, nick_name, backer_money):
    msg = ''
    # 不管金额多少都要入库，首先判断是否入库
    userAll = setting.openjson('user/user')  # 打开本地user缓存到 userAll
    user = list(
        filter(lambda item: item['user_id'] == int(user_id), userAll))  # 过滤出含有 user_id的对象数组
    # 计算抽卡次数
    DrawNum = int(backer_money / oneCard)
    # 查看一下抽卡系统的状态
    DrawType = setting.openjson('ini')["DrawType"]
    if len(user):  # 判断是否存在对象 长度为0则不存在
        # 用户存在
        user = user[0]
        # 打开用户抽卡文件并过滤出当前用户
        user = list(
            filter(lambda item: item['user_id'] == int(user_id), userAll))[0]
        # 修改用户基本信息
        user['nick_name'] = nick_name
        user['all_money'] = round(backer_money + user['all_money'], 2)
        user['nick_name'] = nick_name
        if DrawNum and DrawType:
            # 开始抽卡
            arr = card(DrawNum, user)
            # arr = [user,msg]
            # userCard 用户抽卡信息
            # msg 返回的文案
            user = arr[0]
            msg = arr[1]

    else:
        # 用户不存在
        # 新建用户 DrawNum 为可抽卡次数
        dataList = addUser(user_id, nick_name, backer_money, DrawNum, DrawType)
        # dataList = [user,userCard,msg]
        # user 用户基本信息
        # userCard 用户抽卡信息
        # msg 返回的文案
        user = dataList[0]
        msg += dataList[1]
        # 新用户添加到缓存的数据里去
        userAll.append(user)
    # 按集资总额排序
    userAll = sorted(userAll, key=lambda item: item["all_money"], reverse=True)
    setting.writejson(userAll, 'user/user')
    return msg

# 添加新用户
def addUser(user_id, nick_name, backer_money, DrawNum, DrawType):
    msg = ''
    user = {
        "user_id": user_id,
        "nick_name": nick_name,
        "all_money": backer_money,
        "integral": 0,
        "card_num": 0,
        "card_list": {}
    }
    # 根据配置文件配置card_list
    for lv in childPath:
        user['card_list'][lv] = []
    # 判断是否抽卡
    if DrawNum and DrawType:
        arr = card(DrawNum, user)
        # arr = [user,msg]
        # user 用户抽卡信息
        # msg 返回的文案
        user = arr[0]
        msg += arr[1]
    dataList = [user, msg]
    return dataList

# 纯抽卡函数 
def card(DrawNum, user):
    msg = ''
    nList = setting.openjson('ini')['CardLevel']  # 获取概率数组
    # 定义一个返回msg的数组
    msgList = [0, {}, 0]
    for i in range(DrawNum):
        # 获取一个随机概率 n
        n = random.uniform(1, 100)
        for j in range(len(nList)):
            if n <= nList[j]:
                Samll = cardSamll(user, msgList, j)
        # Samll = [user,msgList]
        user = Samll[0]
        msgList = Samll[1]
    # 定义一个初始卡牌等级
    msgCard = ''
    cardSrc = '无'

    # msgList[1] 抽到卡的数组
    for item in msgList[1]:
        if len(msgList[1][item]):  # 如果该项抽到了卡
            msgCard += "\n" + item + "：| "
            # 循环配置该登记下的文案
            for name in msgList[1][item]:
                msgCard += name + " | "
                cardSrc = "\n本次抽到最好的卡为：\n[CQ:image,file=%s/%s/%s.jpg]" % (idolPath,item,name)
                
    msgCard += cardSrc
    cardIntegral = ""

    # 计算总积分
    user["integral"] += msgList[2]
    if msgList[0]:
        cardIntegral = str(msgList[0]) + '张重复卡转为' + str(msgList[2]) + \
            "积分。当前积分" + str(user["integral"]) + "。"

    msg = '共抽卡' + str(DrawNum) + '次，\n'+cardIntegral+'\n抽得新卡' + msgCard
    msgArr = [user, msg]
    return msgArr
    
# 简化抽卡函数代码量的函数
def cardSamll(user, msgList, level):
    # 遍历路径下的所有文件
    # 抽一张
    # 获得cardName
    # 根绝level获取文件子路径 /r /sr /ssr 这种
    childPath = setting.openjson('ini')["childPath"][level]
    file_dir = cardPath + idolPath + "/" + childPath
    # print(file_dir)
    # print(list(os.walk(file_dir)))
    files = list(os.walk(file_dir))[0][2]
    cardName = os.path.splitext(random.choices(files)[0])[0]

    # 判断重复
    if cardName in user['card_list'][childPath]:
        # 转换积分
        msgList[2] += 30 + 10 * level
        msgList[0] += 1
    else:
        user["card_num"] += 1
        user['card_list'][childPath].append(cardName)
        if childPath not in msgList[1]:
            msgList[1][childPath] = []
        msgList[1][childPath].append(cardName)
    arr = [user, msgList]
    return arr

# 积分抽卡
def intDraw(QQnum):
    DrawType = setting.openjson('ini')["DrawType"]
    msg = ""
    if not DrawType:
        msg = "抽卡系统未开启"
        return msg
    # 判断用户是否绑定
    QQnum = str(QQnum)
    if QQnum in binds:
        user_id = binds[QQnum]
        userAll = setting.openjson("user/user")
        userCard = list(filter(lambda item: item["user_id"] == user_id, userAll))
        if len(userCard):
            userCard = userCard[0]
            # 计算抽奖次数
            DrawNum = int(userCard["integral"] / 100)
            # 积分够不够
            if DrawNum:
                userCard["integral"] -= DrawNum * 100
                arr = card(DrawNum, userCard)
                # userCard 用户抽卡信息
                # msg 返回的文案
                userCard = arr[0]
                msg = arr[1]
                setting.writejson(userAll, 'user/user')
            else:
                msg = '积分不足'
        else:
            msg = '发生错误，请检查绑定的user_id'

    else:
        msg = "未查到" + str(QQnum) + "信息"
    return msg

# 绑定QQ号
def bind(QQnum, user_id):
    binds[QQnum] = int(user_id)
    setting.writejson(binds, 'user/bind')
    msg = "绑定成功"
    return msg

# 查看个人信息 idType True 查询 nick_name False 查询 QQnum
def seachMy(idType, Id):
    DrawType = setting.openjson('ini')["DrawType"]
    if not DrawType:
        msg = "抽卡系统未开启"
        return msg
    msg = ""
    user_id = 0
    userAll = setting.openjson('user/user')  # 打开本地user缓存到 userAll
    if idType:
        # 过滤出含有 nick_name的对象数组
        user = list(filter(lambda item: item["nick_name"] == Id, userAll))
        if not(len(user) == 1):
            msg = "未查到信息或昵称重名了"
            return msg
        else:
            user = user[0]
            user_id = user["user_id"]
    else:
        Id = str(Id)
        # 判断用户是否绑定了
        if Id in binds:
            user_id = binds[Id]
            # 过滤出含有 QQnum 的用户
            user = list(filter(lambda item: item["user_id"] == user_id, userAll))
            if len(user):
                user = user[0]
                user_id = user["user_id"]
            else:
                msg = '发生错误，请检查绑定的user_id'
                return msg
        else:
            msg = "未查到" + str(Id) + "信息"
            return msg
    userCard = user['card_list']
    cardmsg = ""
    # 部署已抽到的卡的文案
    cardAllNum = setting.openjson('ini')['cardAllNum']
    sysAllNum = 0
    userAllNum = 0
    for item in userCard:
        try:
            sysAllNum += cardAllNum[item]
        except:
            pass
        userAllNum += len(userCard[item])
        if len(userCard[item]):
            cardmsg += '\n【' + item + "】"+ str(len(userCard[item]))+'/'+ str(cardAllNum[item]) + '\n| '
            for name in userCard[item]:
                cardmsg += name + " | "
    msg = "ID：" + str(user["nick_name"]) + "\n" + \
          "可用积分：" + str(user["integral"]) + "\n" + \
          "收集进度: " + str(userAllNum) + "/" + str(sysAllNum) + "\n" + \
          "抽卡信息：" + cardmsg
    return msg

# 积分补偿
def addDraw(QQnum, num):
    DrawType = setting.openjson('ini')["DrawType"]
    msg = ""
    if not DrawType:
        msg = "抽卡系统未开启"
        return msg
    # 判断用户是否绑定了
    if QQnum in binds:
        user_id = binds[QQnum]
        cardAll = setting.openjson('user/user')  # 打开本地userCard缓存到 cardAll
        # 过滤出含有 QQnum 的用户
        user = list(filter(lambda item: item["user_id"] == user_id, cardAll))
        if len(user):
            try:
                user = user[0]
                user["integral"] += int(num)
                setting.writejson(cardAll, 'user/user')
                msg = "补偿成功"
            except:
                msg = "积分错误"
        else:
            msg = '发生错误，请检查绑定的user_id'
    else:
        msg = "未查到" + str(QQnum) + "信息"
    return msg

# 开启关闭抽卡 0 执行关闭抽卡 1 执行开启抽卡
def changeDraw(types):
    msg = ""
    iniData = setting.openjson("ini")
    if types:
        if iniData["DrawType"]:
            msg = "不可重复开启"
        else:
            iniData["DrawType"] = True
            msg = "开启成功"
    else:
        if iniData["DrawType"]:
            iniData["DrawType"] = False
            msg = "关闭成功"
        else:
            msg = "不可重复关闭"
    setting.writejson(iniData, "ini")
    return msg

# 查看卡面
def showCard(cardName):
    msg = "未查到【" + cardName + "】"
    files = list(os.walk(cardPath+idolPath))
    has = False
    i = -1
    for item in files:
        if has:
            break
        for name in item[2]:
            if os.path.splitext(name)[0] == cardName:
                msg = "[CQ:image,file=%s/%s/%s]" % (idolPath,files[0][1][i],name)
                has = True
                break
        i += 1
    return msg
