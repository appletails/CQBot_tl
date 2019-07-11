# -*- coding: utf-8 -*-
from cqhttp import CQHttp
import setting
import modian
import answer
import tool
import card
import time


bot = CQHttp(api_root='http://127.0.0.1:5700/')
# 也可以添加access_token和secret，更加安全
# bot = CQHttp(api_root='http://127.0.0.1:5700/',
#              access_token='your-token',
#              secret='your-secret')
# 如果设置了access_token和secret，请修改http-API插件的配置文件中对应的部分

robot = "机器人"
# 群消息操作
@bot.on_message('group')
def handle_msg(context):
    # 获取管理员
    adminArr = answer.Admin()
    # 获取超级管理员
    administrator = answer.Administrator()

    # 开始进行关键字触发
    if context['group_id'] in setting.groupid() and context['user_id'] != context['self_id']:
        # 关键词禁言
        if setting.shutup():
            for word in setting.shutup():
                if word in context['message']:
                    bot.set_group_ban(group_id=context['group_id'], user_id=context['user_id'], duration=5*60)
        # 关键词回复
        if context['message'] in ['集资','jz','打卡','摩点','Jz']:
            jz_array = modian.md_init(setting.pro_id())
            for item in jz_array:
                jz = [
                    {'type': 'share', 'data': {
                        "url": item['url_short'],
                        "title": item['name'],
                        "content": "谢谢大家的支持~比心心~",
                        # "image": "https://s.moimg.net/activity/images/modian_icon.png"
                        "image": "https://p.moimg.net/ico/2019/04/09/20190409_1554800123_9103.jpg?imageMogr2/auto-orient/strip"
                    }}
                ]
                bot.send(context, jz)
                time.sleep(.1)
        elif context['message'] in ['Rank','rank','集资榜']:
            rank1_array = modian.rank(1)
            for rank1_msg in rank1_array:
                bot.send(context, rank1_msg)
        elif context['message'] in ['dkb','打卡榜']:
            rank2_array = modian.rank(2)
            for rank2_msg in rank2_array:
                bot.send(context, rank2_msg)
        elif context['message'] in ['项目进度','进度']:
            jd_array = modian.result(setting.pro_id())
            jd = ''
            for jd_msg in jd_array:
                jd += jd_msg + '\n'
            bot.send(context, jd)
# ------------------------------------------------------------------------
     
# --------------------- 全部人指令 -----------------------------   
        elif context['message'] in ['今日集资','昨日集资']:
            msg = tool.today(context['message'])
            bot.send(context, msg)

# --------------------- 追加管理员指令，修改ini.json -----------------------------
        elif '更换项目 ' in context['message'] or '更换id ' in context['message']:
            msg = ''
            if context['user_id'] in adminArr or context['user_id'] in administrator:
                msg = answer.changeProid(context['message'])
            else:
                msg = '你没有权限'
            bot.send(context, msg)
  
        # 超级管理员指令 26440 26262
        elif '添加管理 ' in context['message']:
            msg = ''
            if context['user_id'] in administrator:
                QQnum = context['message'][15:-1]
                msg = answer.addAdmin(QQnum)
            else:
                msg = '你没有权限'
            bot.send(context, msg)
        elif '撤销管理 ' in context['message'] or '删除管理 ' in context['message']:
            msg = ''
            if context['user_id'] in administrator:
                QQnum = context['message'][15:-1]
                msg = answer.delAdmin(QQnum)
            else:
                msg = '你没有权限'
            bot.send(context, msg)

        elif '开启每日播报' in context['message'] or '关闭每日播报' in context['message']:
            msg = ''
            if context['user_id'] in administrator:
                msg = answer.todayShow(context['message'])
            else:
                msg = '你没有权限'
            bot.send(context, msg)
     
# --------------------- 娱乐指令，调用answer.json -----------------------------   
        elif context['message'] in [robot+'在么',robot+'在吗',robot+'在不在']:
            msg = answer.roundMsg()
            bot.send(context, msg)

# --------------------- 接力指令 -----------------------------   
        elif context['message'] in ["开启接力","接力开启","关闭接力"] or "接力金额 " in context['message']:
            msg = ''
            if context['user_id'] in adminArr or context['user_id'] in administrator:
                msg = tool.relayOpen(context['message'])
            else:
                msg = "你没有操作权限哦"
            bot.send(context, msg)
        elif context['message'] in ['棒数','查看棒数']:
            bot.send(context, tool.relayNum())
        elif '接力 ' in context['message']:
            msg = ''
            if context['user_id'] in adminArr or context['user_id'] in administrator:
                msg = tool.addNum(context['message'])
            else:
                msg = "你没有操作权限哦"
            bot.send(context, msg)
# --------------------- pk指令 -----------------------------   
        elif  context['message'] in ["开启pk","关闭pk"]:
            msg = ''
            if context['user_id'] in adminArr or context['user_id'] in administrator:
                msg = tool.changePK(context['message'])
            else:
                msg = "你没有操作权限哦"
            bot.send(context, msg)
        elif 'pk项目 ' in context['message']:
            msg = ''
            if context['user_id'] in adminArr or context['user_id'] in administrator:
                msg = tool.addPk(context['message'])
            else:
                msg = "你没有操作权限哦"
            bot.send(context, msg)
        elif 'pkid ' in context['message']:
            msg = ''
            if context['user_id'] in adminArr or context['user_id'] in administrator:
                msg = answer.changeProid(context['message'],True)
            else:
                msg = '你没有权限'
            bot.send(context, msg)
        elif context['message'] in ['查看pk','pk']:
            bot.send(context, tool.showPk("pk实况")) if tool.showPk("pk实况") else ''

# --------------------- 抽卡指令 -----------------------------   
        elif context['message'] == '我的信息':
            bot.send(context, card.seachMy(False,context['user_id']))

        elif context['message'] == '积分抽卡':
            bot.send(context, card.intDraw(context['user_id']))

        elif "查卡 " in context['message']:
            name = context['message'][3:]
            bot.send(context, card.showCard(name))

        elif "查 " in context['message']:
            name = context['message'][2:]
            bot.send(context, card.seachMy(True,name))

        elif "绑定 " in context['message']: # 绑定 @QQnum nick_name
            msg = ''
            if context['user_id'] in adminArr or context['user_id'] in administrator:
                arr = context['message'][3:].split(" ", 1)
                nick_name = arr[1]
                QQnum = arr[0][10:-1]
                msg = card.bind(QQnum,nick_name)
            else:
                msg = "你没有操作权限哦"
            bot.send(context, msg)

        elif "补偿 " in context['message']: # 补偿 @QQnum 分数
            msg = ''
            if context['user_id'] in adminArr or context['user_id'] in administrator:
                arr = context['message'][3:].split(" ", 1)
                QQnum = arr[0][10:-1]
                num = arr[1]
                msg = card.addDraw(QQnum,num)
            else:
                msg = "你没有操作权限哦"
            bot.send(context, msg)

        elif context['message'] in ["开启抽卡","关闭抽卡"]:
            msg = ''
            if context['user_id'] in adminArr or context['user_id'] in administrator:
                if context['message'] == "开启抽卡":
                    msg = card.changeDraw(1)
                else:
                    msg = card.changeDraw(0)
            else:
                msg = "你没有操作权限哦"
            bot.send(context, msg)



# 新人加群提醒
@bot.on_event('group_increase')
def handle_group_increase(context):
    if context['group_id'] == setting.groupid()[0]:
        welcome = [{'type': 'text', 'data': {'text': '欢迎新聚聚：'}},
        {'type': 'at', 'data': {'qq': str(context['user_id'])}},
        {'type': 'text', 'data': {'text': ' 加入本群\n\n%s' % setting.welcome()}}
        ]
        bot.send(context, message=welcome, is_raw=True)  # 发送欢迎新人


# 如果修改了端口，请修改http-API插件的配置文件中对应的post_url
bot.run(host='127.0.0.1', port=8080)
