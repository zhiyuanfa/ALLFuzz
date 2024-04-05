import requests
import re
import urllib.parse
from globals.Global import colored



def icp_get(url):
    url = url.lstrip("http://").lstrip("https://").split("/")[0]
    print(colored(f"查询的目标:{url}", 'yellow'))
    get_url = "https://icp.chinaz.com/" + url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    }
    cookies = {

    }
    pattern1 = r'//data.chinaz.com/company/t0-p0-c0-i0-d0-s-([^"]+)'
    pattern2 = r'//whois.chinaz.com/([^"]+)'
    try:
        content = requests.get(url=get_url, headers=headers, cookies=cookies).text
        match1 = re.search(pattern1, content)
        match2 = re.search(pattern2, content)

        if match1:
            data = match1.group(1)
            print(colored("解析结果: " + urllib.parse.unquote(data), 'green'))
        else:
            print(colored(f"没有查询到[{url}]的ICP备案信息", 'red'))
            return None

        if match2:
            domain_url = match2.group(1)
            return colored('域名:'+domain_url,'green')
        else:
            return data

    except requests.exceptions.RequestException as e:
        print(colored("[Error] " + str(e), 'red'))

# icp查询调用方法
def icp(str):
    icp_info = icp_get(str)
    print(icp_info)
    return icp_info

