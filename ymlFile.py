import json


#覆盖json文件写入
def write_json(data):
    with open('./id.json', 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False)

#读取json文件
def read_json():
    return json.load(open('id.json', 'r', encoding="utf-8"))

