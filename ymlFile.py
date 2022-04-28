import json


#覆盖json文件写入
def write_json(data,txt):
    with open(txt, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False)

#读取json文件
def read_json(txt):
    return json.load(open(txt, 'r', encoding="utf-8"))

