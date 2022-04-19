import os
import yaml


#读取extract文件
def read_extract_file(key):
    with open(
        os.getcwd() + "/idlist.yml", encoding="utf-8"
    ) as f:  # os.getcwd 打开项目根路径
        value = yaml.load(f.read(),Loader=yaml.FullLoader) # 加载yaml文件的内容
        return value[key]


# 写入yaml文件
def write_yaml(data):
    with open(
        os.getcwd() + "/idlist.yml",
        encoding="utf-8",
        mode="a",
    ) as f:  # a是追加的方式写入
        [f.write("{}: {}\n".format(key, data[key])) for key in data]

# 清空yaml文件
def clear_yaml():
    with open(
        os.getcwd() + "/idlist.yml",
        encoding="utf-8",
        mode="w",
    ) as f:  # w 写入
        f.truncate()


