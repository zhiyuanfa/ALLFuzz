from globals.Global import colored

# 读取文件的方法
def get_str(path):
    lines = []  # 使用局部变量而不是全局变量
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())  # 去除每行末尾的换行符
    return lines

# 文件内容查询调用方法
def file(str):
    strs = get_str(str)
    return strs
