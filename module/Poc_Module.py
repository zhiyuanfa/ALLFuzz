import requests
import yaml
import re
from urllib.parse import urljoin
import random
import os
from concurrent.futures import ThreadPoolExecutor
import warnings
from globals.Global import colored 

# 忽略FutureWaring
warnings.simplefilter(action='ignore', category=FutureWarning)

POCS_DIR = 'test'

# 递归扫描POC文件中的键值对
def find_key_value(data, key):
    if isinstance(data, dict):
        if key in data:
            return data[key]
        for k, v in data.items():
            result = find_key_value(v, key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key_value(item, key)
            if result is not None:
                return result
    return None

# 日志存放
def log_message(message, file_name):
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(message + "\n")

# 读取POC文件
def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# 随机值
def random_int(min_val, max_val):
    return random.randint(min_val, max_val)

session = requests.Session()  # 使用 Session 优化网络请求

# 取值
def escape_body_text(body_text):
    return body_text.replace("{", "{{").replace("}", "}}")


# POC验证的主要方法
def verify_poc(url, yaml_file):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    try:
        poc_data = load_yaml(yaml_file)

        full_url = urljoin(url, find_key_value(poc_data, 'path') or '')
        method = find_key_value(poc_data, 'method') or 'GET'
        headers = find_key_value(poc_data, 'headers') or {}
        body = escape_body_text(find_key_value(poc_data, 'body') or '')
        expression = find_key_value(poc_data, 'expression') or ''

        # 检查是否有任何有效的验证规则字段
        if not any([full_url, method, headers, body, expression]):
            error_message = f"[-] Error rule in POC {yaml_file}: {e}"
            log_message(error_message, "log\\errorlog.txt")
            print(colored('[!!!]部分POC文件出现问题，具体问题请查看POC是否正确------errorlog.txt','red'))
            return

        # 验证POC
        try:
            response = None
            if method.upper() == 'POST':
                response = session.post(full_url, headers=headers, data=body)
            elif method.upper() == 'GET':
                response = session.get(full_url, headers=headers)

            if response and re.search(expression, response.text):
                success_message = f"[+] Success: {yaml_file} detected a vulnerability at {url}"
                print(colored(success_message, 'green'))
                log_message(success_message, "log\\log.txt")

        except Exception as e:
            return
    except Exception as e:
        pass


# 读取POC文件
def verify_all_pocs(url):
    results = []
    processed_files = set()  # 用于跟踪已处理的文件
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for filename in os.listdir(POCS_DIR):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                poc_file = os.path.join(POCS_DIR, filename)
                if poc_file not in processed_files:  # 检查是否已处理该文件
                    future = executor.submit(verify_poc, url, poc_file)
                    futures.append(future)
                    processed_files.add(poc_file)  # 标记为已处理

        for future in futures:
            try:
                result = future.result()
                if result:  # 确保返回的结果是元组
                    results.append(result)
            except Exception as exc:
                pass

    return results

# poc验证调用方法
def poc(str):
    results = verify_all_pocs(str)
    for filename, result in results:
        print(colored(f"Result for {filename}: {'Success' if result else 'Fail'}", 'green'))

