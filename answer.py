# -*- coding: utf-8 -*-
import json
import modian
import random
import setting

# 获取管理员 获取超级管理员 修改pro_id 新增管理员 撤销管理员 随机回复


# 获取管理员
def Admin():
	adminArr = setting.openjson('ini')['admin']
	return adminArr

# 获取超级管理员


def Administrator():
	administratorArr = setting.openjson('ini')['administrator']
	return administratorArr

# 修改pro_id


def changeProid(cont, pk=False):
    msg = ''
    try:
        # 获取新的proid
        pro_id = int(cont[5:])
        # 获取项目信息
        orderDict = modian.getDetail(pro_id)
        # 判断proid是否是有误
        if int(orderDict['status']) == 2:
            msg = 'pro_id有误，请核实后重试'
        else:
            # 获取本地库配置
            ini = setting.openjson('ini')
            # 在这里判断是换了日常还是pk
            if pk:
              ini['modian']['pk'] = pro_id
            else:
              # 配置好新的proid
              ini['modian']['pro_id'] = [pro_id]
            # 获取摩点order数据
            orderData = modian.sorted_orders(pro_id, 1)
            # 判断当前项目是否存在数据
            if int(orderData['status']) == 2:
                # 不存在数据
                data = []
                # 保存本地order文件
                setting.writejson(data, "order/" + str(pro_id))
            else:
                page = 1
                data = []
                while True:
                    orderData = modian.sorted_orders(pro_id, page)
                    # print(orderData["data"])
                    if orderData["data"] == None:
                        break
                    page += 1
                    data += orderData["data"]

                # for item in data:
                #     card.DrawCard(item["user_id"],item["nickname"],item["backer_money"])
                # 保存本地order文件
                setting.writejson(data, "order/" + str(pro_id))
            # resetRank(pro_id)
            # 保存配置文件
            setting.writejson(ini, 'ini')
            # 设置返回文案
            # 在这里判断是换了日常还是pk
            if pk:
              msg = '更换成功，当前pk项目为: ' + orderDict['data'][0]['pro_name']
            else:
              msg = '更换成功，当前项目为: ' + orderDict['data'][0]['pro_name']
    except Exception:
        msg = '发生错误，请检查输入格式是否正确'
    return msg

# 新增管理员
def addAdmin(QQnum):
	msg = ''
	try:
		Admin_id = int(QQnum)
		data = setting.openjson('ini')
		if Admin_id in data['admin']:
			msg = '该管理员已经存在'
		else:
			data['admin'].append(int(Admin_id))
			setting.writejson(data,'ini')
			msg = '追加成功'
	except Exception:
		msg = '发生错误，请检查输入格式是否正确'
	return msg

# 撤销管理员
def delAdmin(QQnum):
	msg = ''
	try:
		Admin_id = int(QQnum)
		data = setting.openjson('ini')
		if Admin_id in data['admin']:
			data['admin'].remove(int(Admin_id))
			setting.writejson(data,'ini')
			msg = '删除成功'
		else:
			msg = '该管理员不存在'
	except Exception:
		msg = '发生错误，请检查输入格式是否正确'
	return msg

# 1.random.random()方法，这个方法返回一个随机的实数，范围在[0,1)之间
# 2.random.uniform(a,b)方法，生成a,b之间的一个随机浮点数
# 3.random.randint(a,b)方法，生成指定范围内的整数
# 4.random.randrange(a,b,n)方法，在a,b范围内，按n递增的集合中随机选择一个数
# 选择100-200之间的偶数：
# 5.random.choice('abcdeapejad')，从所给的字符串中随机选择字符
# 6.random.sample('abcdoeuaja;a', 3)，从所给的字符串中选取对应数量的字符
# 7.random.choice(['abc', 'apple', 'orange', 'banana'])随机选择字符串
# 8.随机排序 random.shuffle(list)

# 随机回复
def roundMsg():
	answer = setting.openjson('tool/answer')
	msg = random.choice(answer)
	return msg

# 开启每日播报
def todayShow(cont):
	msg = ''
	todayType = setting.openjson('ini')
	if cont == '开启每日播报':
		if todayType['todayType']:
			msg = '不可重复开启'
		else:
			todayType['todayType'] = True
			setting.writejson(todayType,'ini')
			msg = '开启成功'
	else:
		if todayType['todayType']:
			todayType['todayType'] = False
			setting.writejson(todayType,'ini')
			msg = '关闭成功'
		else:
			msg = '不可重复关闭'
	return msg
