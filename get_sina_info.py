import json
import time

from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import markdownify
from ymlFile import read_json,write_json
import re

userenum = {
    "薅羊毛的大队长": "5069029750",
    "蘑菇小牙牙":"1987241375",
    "小屁屁挖白菜":"3194506490",
    "披着羊毛的魔鬼":"1917872472",
}

uid_list = [
    userenum["薅羊毛的大队长"],
    userenum["蘑菇小牙牙"],
    userenum["小屁屁挖白菜"],
    userenum["披着羊毛的魔鬼"],
]
base_url = "https://weibo.com/ajax/statuses/mymblog?uid={}&page=1&feature=0"
keywords = {
    #"19157707002": ["洗衣机","电视机","电冰箱"],
    "13210745239": ["卫生巾"],
    "17751793119": ["牛肉干"],
    #"17816874619": ["显卡"],
}
#["瑞幸"] 关键字
header = {
    "cookie": "XSRF-TOKEN=Yvum9imXlVvXblTDwHt0EzYL; SUB=_2AkMVAgQ7dcPxrAVQm_ASzW7jaY9H-jym123NAn7uJhMyAxhu7msjqSVutBF-XAFfxzN3IbKWzoaInffUay8gZBa8;",
}


def send_message(message,atMobiles):
    #我公司的群
    token1 = "https://oapi.dingtalk.com/robot/send?access_token=a56088b1a17f1378d808f365a7d91c81414b9abc9722a7605c3f18f3c0b11e8a"
    #洛哥的群
    #token2 = "https://oapi.dingtalk.com/robot/send?access_token=614186589451c0dc0a4583168f23cfc0e9da9768039b77eff8dfc4350c88d00c"
    # 发送Markdown类型的机器人消息
    """发送Markdown类型的机器人消息
        :param message:发送的消息
        :param is_at_all: 是否@所有人
        :param target_mobiles: @对象的钉钉绑定的手机号列表
    """

    param = {
        "msgtype": "markdown",
        # "text": {"content":"通知"+message},
        "markdown": {
            "title": "通知",
            "text": message
        },
        "at": {
            #"atUserIds":atUserIds
            "atMobiles":atMobiles,
            #"isAtAll": isAtAll,
        }
    }

    requests.post(token1, json=param)
    #requests.post(token2, json=param)


def parse_message(message):
    #格式处理
    # print(html.remove_tags(message, which_ones=('img')))
    image_tag = re.compile(r'(<img.*?/>)').findall(message)
    if image_tag:
        for item in image_tag:
            message = message.replace(item, '')
    msg = markdownify.markdownify(message, heading_style="ATX")
    return msg

def get_sheep():
    """获得羊毛信息并发钉钉通知"""
    phone_list = []
    for uid in uid_list:
        url = base_url.format(uid)
        res = requests.get(url, headers=header).json()
        if res.get("ok") == None and res["ok"] != 1:
            break
        data_list = res.get("data").get("list")
        # 判断博主的置顶微博,不是最新的,放在循环外
        if len(data_list)!=0 and data_list != []:
            if data_list[0].get("isTop") != None:
                is_top = data_list[0].get("isTop")
                if (is_top is not None) or is_top == 1:
                    del data_list[0]
        else:
            break
        # 比较返回中最新的一条 跟上次请求保存在本地最大的一条
        id_json = read_json()
        if data_list[0]["id"] != id_json[uid]:
            for item in data_list:
                #依次从大到小，跟保存本地的那条数据做校验
                if  item["id"] > id_json[uid]:
                    message = parse_message(item.get("user").get("screen_name") + '\\\n' + '\\\n' + item.get("text"))
                    if item["pic_num"] == 1:
                        pic = item["pic_infos"][item["pic_ids"][0]]["bmiddle"]["url"]
                        message = parse_message(item.get("user").get("screen_name")+'\\\n'+'\\\n'+item.get("text")+'\\\n'+"![]"+"("+pic+")")
                    if len(keywords) == 0:
                        send_message(message,None)
                    for key in keywords:
                        # 如果关键字在博主发的消息和链接的文字中含有,就发送请求
                        keylist = keywords[key]
                        for word in keylist:
                            if item.get("url_struct") != None:
                                if word in str(str(message)+str(item["url_struct"][0]["url_title"])):
                                    phone_list.append(key)
                                    message = message + "@"+key
                                    send_message(message,phone_list)
                    send_message(message,None)
                if item["id"] == id_json[uid]:
                    break
        # 获取到本次请求最大的id，最新的一条存到本地
            id = data_list[0]["id"]
            id_json[uid] = id
            write_json(id_json)

# if __name__ == '__main__':
#     get_sheep()
def dojob():
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    #添加任务,时间间隔2S
    scheduler.add_job(get_sheep, 'interval', seconds=8,max_instances=5)
    scheduler.start()
dojob()