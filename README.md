# modian_tl

[TOC]

## 简介

基于[CQBot_hzx](https://github.com/chinshin/CQBot_hzx) 二次开发的摩点机器人，使用方法同CQBot_hzx的[使用方法](https://github.com/chinshin/CQBot_hzx/blob/master/README.md#使用方法)
<br>此程序仅保留了摩点的相关信息，并在其基础上增加了抽卡，pk，接力等相关内容
<br>感谢师祖[ChenZhen](https://github.com/chinshin)开发了CQBot_hzx和师父[ChengChao Fu](https://github.com/ultraxia)教我python基础，鞠躬

## 补充说明
这是一个不具备数据库的程序，所有数据存储均以json文件的形式存放
* 使用前请将 `jsons` 下的 `ini.json.bak` 文件名改为 `ini.json` 并配置
* 使用前请在 `jsons/user` 下建立 `user.json` 文件，内容为 `[]`
* 使用前请在 `jsons/user` 下建立 `bind.json` 文件，内容为 `{}`
* **注意：** 手动添加监听项目时，请务必在`jsons/order`下建立对应的json，例如：手动添加了`0000`项目，则需要建立`0000.json`


## 指令

**1、一般指令：** 唤出集资之类的指令

| 名称 | 权限 | 描述 |
|:-:|:-:|:-:|:-:|
集资、jz、打卡、摩点、Jz | all | 集资链接/ 含有集资链接分享标签
Rank、rank、集资榜 | all | 集资榜前20(全部监听项目)
dkb、打卡榜 | all | 打卡榜前20(全部监听项目)
项目进度、进度 | all | 项目进度(全部监听项目)
今日集资 | all | 今天的所有集资和累计总数
昨日集资 | all | 昨天的所有集资和累计总数
机器人在么 | all | 随机回复一条消息<br>在`tool/answer.json`中设置<br>主要用来查看机器人是否在线

**2、管理员指令：** 追加管理员之类的

` 理论上上admin的指令administrator都可以操作 `

名称 | 权限 | 描述
:-:|:-:|:-:|:-:
添加管理 @群成员 | administrator | 添加群成员到admin
撤销管理 @群成员 | administrator | 从admin撤销群成员
开启每日播报 | administrator | 每天23:59:59会自动播报当天集资
关闭每日播报 | administrator | 关闭每日播报
更换项目 pro_id | admin | 更换监听的项目<br>仅在监听单个项目的时候可用

**3、接力指令：**

` 同时只能记录一个接力flag `

名称 | 权限 | 描述
:-:|:-:|:-:|:-:
开启接力/接力开启 | admin | 根据机器人的提示操作就可以
关闭接力 | admin | 关闭接力
接力 10 | admin | 手动追加10棒，数量可改
棒数/查看棒数 | all | 当前已接力的棒数

**3、PK指令：**

```
备注：
1、pk内容较多，可能存在各种bug
2、pkid最好设置一下，否则可能会出问题
3、设置pkid后一般指令将只会呼出关闭pk项目的信息，但不影响集资抽卡播报
```

名称 | 权限 | 描述
:-:|:-:|:-:|:-:
开启pk | admin | 根据机器人的提示操作就可以
pkid 00000 | admin | 参与pk的项目id
pk项目 项目1(1),项目1(2) 项目2(1),项目2(2) ...| admin | 设置参与pk的项目，支持小队pk<br>小队之间空格隔开<br>同队之间英文半角逗号隔开
查看pk/pk | all | 查看pk详情

**4、抽卡指令：**

```
注意！！：开启抽卡前请先配置ini.json的以下内容
//以r卡文件夹路径 C:/Users/Administrator/Downloads/CQP-xiaoi/酷Q Pro/data/image/tl/r 为例
1、cardPath：这是抽卡的问文件下路径，在例子中为 C:/Users/Administrator/Downloads/CQP-xiaoi/酷Q Pro/data/image/
2、idolPath：在例子中为 tl，在tl这个文件夹下可以设置抽卡的等级文件夹r,sr,ssr等
3、childPath：是个list，配置可以抽到的等级的卡，！！！高级卡在前，低级卡在后！！！
4、CardLevel：是个list，和childPath一一对应，没种卡的等级，！！！必须是从小到大的概率，最后一个必须是100！！！
5、cardAllNum：每个等级 卡的总数
6、oneCard：抽一张卡所需的集资，

关于转换率，转换率最低为30积分，等级每高一级加10积分
关于概率，数字越小概率越低
```

名称 | 权限 | 描述
:-:|:-:|:-:
开启抽卡 | admin | 开启抽卡
关闭抽卡 | admin | 关闭抽卡
绑定 @群成员 摩点id | admin | 绑定QQ号和摩点id
补偿 @群成员 数量 | admin | 手动补偿积分，100的倍数
我的信息 | all | 查看自己的信息，需绑定
积分抽卡 | all | 使用积分进行抽卡，100积分抽一次
查 摩点昵称 | all | 查看别人的信息
查卡 卡片名称 | all | 查看卡片

以上<br>
有问题加Q群：691963133<br>
或者微博私信[-青春的小尾巴-](https://weibo.com/amber0401)
