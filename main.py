# -*- coding: utf-8 -*-
from cqhttp import CQHttp
# import _thread
import time
import tool
from setting import groupid, md_interval, wb_interval, openjson
from modian import newOrder
from CQLog import INFO, WARN
# 引入时间调度器 apscheduler 的 BlockingScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

# 与group.py设置一样
bot = CQHttp(api_root='http://127.0.0.1:5700/')
# 实例化 BlockingScheduler
sched = BlockingScheduler()

global weibo_id_array
global firstcheck_weibo

weibo_id_array = []
firstcheck_weibo = True

# 查询时间间隔初始化
interval_md = md_interval()

# 获取酷q版本
version_dict = bot.get_version_info()
version = version_dict['coolq_edition']


def getModian():
    # try:
    #     INFO('check modian')
    stampTime = int(time.time())
    msgDict_arr = newOrder(stampTime, int(interval_md))
    for msgDict in msgDict_arr:
        if msgDict:
            for msg in msgDict:
                for grpid in groupid():
                    bot.send_group_msg_async(
                        group_id=grpid, message=msg, auto_escape=False)
                    time.sleep(0.1)
    # except Exception:
    #     WARN('error when getModian')
    # finally:
    #     INFO('modian check completed')

# 定时函数
def on_time():
    todayType = openjson('ini')['todayType']
    if todayType:
        msg = ["每日集资记录~\n\n"]
        msgAll = msg[0] + tool.today("定时播报")
        for grpid in groupid():
            bot.send_group_msg_async(group_id=grpid, message=msgAll, auto_escape=False)
            time.sleep(0.5)
    else:
        print('每日播报未开启')

# 开始定时任务
sched.add_job(on_time, 'cron', hour = 23,minute = 59,second = 58)

# 添加调度任务， 间隔为 0 则不添加
if interval_md != 0:
    print('摩点间隔：'+str(interval_md))
    # 20180409
    # 增加misfire_grace_time参数：任务错过时间大于一个周期则放弃
    # 增加coalesce参数：多个错过任务合并执行一次
    # 增加max_instances参数：允许5个实例同时运行
    sched.add_job(
        getModian, 'interval', seconds=interval_md,
        misfire_grace_time=interval_md, coalesce=True, max_instances=5)

# 开始调度任务
sched.start()
