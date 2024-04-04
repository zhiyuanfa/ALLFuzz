import argparse
from module import Poc_Module
from module import Icp_Module

def colored(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "white": "\033[97m"
    }
    return colors.get(color, colors["white"]) + text + "\033[0m"

def main():
    parser = argparse.ArgumentParser(description='网络安全漏洞扫描工具')
    parser.add_argument('--url','-u', help='要扫描的单个URL，如："python AllFuzz.py --url url"', type=str)
    parser.add_argument('--icp', help='执行ICP备案信息检测，目前支持传入公司名查询，并进行POC验证', type=str)
    parser.add_argument('--poc', help='执行POC验证，POC验证默认关闭', action='store_true')

    args = parser.parse_args()

    if args.icp:
        icp_info = Icp_Module.icp_get(args.icp)
        print(icp_info)
        results = Poc_Module.verify_all_pocs(icp_info)
        print(results)

    elif args.url:
        print(f"Scanning URL: {args.url}")

        if args.poc:
            results = Poc_Module.verify_all_pocs(args.url)
            for filename, result in results:
                print(f"Result for {filename}: {'Success' if result else 'Fail'}")
    else:
        print(colored("Error: 请检查参数是否输入错误", "red"))


if __name__ == "__main__":
    art = """       
            _                              _           _   
           | |                            (_)         | |  
      ____ | |__     ___   _ __     __ _   _   _ __   | |_ 
     |_  / | '_ \   / _ \ | '_ \   / _` | | | | '_ \  | __|
      / /  | | | | |  __/ | | | | | (_| | | | | | | | | |_ 
     /___| |_| |_|  \___| |_| |_|  \__, | |_| |_| |_|  \__|
                                    __/ |                  
                                   |___/                   
        """  # 艺术字
    print(colored(art + '\n', 'yellow'))
    print(colored('https://github.com/zhiyuanfa/AllFuzz 欢迎指点\n','yellow'))
    print(colored('[*]FUZZ开始了，喝口茶等等吧~~~' + '\n', 'yellow'))
    main()
