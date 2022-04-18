import json
import requests
import markdownify
from apscheduler.schedulers.blocking import BlockingScheduler
from ymlFile import write_yaml,clear_yaml,read_extract_file


base_url = "https://www.weibo.com/ajax/feed/friendstimeline?list_id=110007301411556&refresh=4&since_id=0&count=25&fid=110007301411556"
keywords = ["史低","0元","不要钱","1元买"]
screen_name = ["薅羊毛的大队长"]
header = {
    "cookie": "SUB=_2A25PWU3tDeRhGeBP6FoW8SvNzj6IHXVsLzglrDV8PUNbmtB-LRL7kW9NRV3XpYg0B0_wkIVpYZtw-OvIWJ5A-Hzi",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",

}

def send_message(message,atall):
    token_list = []
    token1 = "https://oapi.dingtalk.com/robot/send?access_token=a56088b1a17f1378d808f365a7d91c81414b9abc9722a7605c3f18f3c0b11e8a"
    token2 = "https://oapi.dingtalk.com/robot/send?access_token=614186589451c0dc0a4583168f23cfc0e9da9768039b77eff8dfc4350c88d00c"
    token_list.append(token1)
    token_list.append(token2)
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

            "isAtAll": atall,
        }
    }
    for token in token_list:
        res = requests.post(token, json=param)
        #print(res.json())


def get_sheep():
    """获得羊毛信息并发钉钉通知"""
    # 微博请求
    data = requests.get(base_url, headers=header).text
    print(data)
    data = json.loads(data)
    # 获取请求的消息list
    data_list = data.get("statuses")
    # 读取本地保存下来的消息id
    idList = read_extract_file("idlist")
    idList.reverse()
    # 如果两条消息的最大id不一致,代表已有更新消息
    if data_list[0]["id"] != idList[0]:
        data_list.reverse()
        id_list = []
        # 循环出每条消息
        for item in data_list:
            #将新请求的id保存到新列表
            id = item.get("id")
            id_list.append(id)
            #判断请求获取到的id最小值是否大于本地保存的id最大值
            if item.get("id") > idList[0]:
                # 收到的每条消息进行处理
                message = parse_message(item.get("user").get("screen_name")+'\\\n'+'\\\n'+item.get("text"))
                # 字数小于5个字的描述,表示超级羊毛，0元购 没用
                #text_raw = item.get("text_raw").split("http")[0]
                # if len(text_raw) < 5:
                #     send_message(message, True)
                # 带有某关键字和关键博主 +@所有人
                if len(keywords) == 0:
                    if  item.get("user").get("screen_name") in screen_name:
                        send_message(message, False)
                    else:
                        send_message(message,False)
                else:
                    for word in keywords:
                        if item.get("user").get("screen_name") in screen_name and word in message:
                            send_message(message, False)
                            break
                    send_message(message, False)
            else:
                continue
        extract_data = {"idlist": id_list}
        clear_yaml()
        write_yaml(extract_data)


def parse_message(message):
    import re
    image_tag = re.compile(r'(<img.*?/>)').findall(message)
    if image_tag:
        for item in image_tag:
            message = message.replace(item, '')
    msg = markdownify.markdownify(message, heading_style="ATX")
    return msg



#
# if __name__ == '__main__':
#     get_sheep()
def dojob():
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    #添加任务,时间间隔2S
    scheduler.add_job(get_sheep, 'interval', seconds=2)
    scheduler.start()
dojob()