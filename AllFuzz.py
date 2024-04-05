import argparse
from module import Poc_Module
from module import Icp_Module
from module import Url_Module

def colored(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "purple": "\033[35m",
        "white": "\033[97m"
    }
    return colors.get(color, colors["white"]) + text + "\033[0m"

def main():
    parser = argparse.ArgumentParser(description='[ALLFUZZ]-----[++一款全方位FUZZ工具++]-----[zhengint]')
    parser.add_argument('--url','-u', help='要扫描的单个URL，如："python AllFuzz.py --url url"', type=str)
    parser.add_argument('--urls', help='扫描多个URL，引入URL文件，如："python AllFuzz.py --urls url.txt"', type=str)
    parser.add_argument('--icp', help='执行ICP备案信息检测，目前支持传入公司名查询，并直接进行POC验证', type=str)
    parser.add_argument('--poc', help='执行POC验证，POC验证默认关闭', action='store_true')

    args = parser.parse_args()

    if args.icp:
        print(colored('[*]FUZZ开始了，喝口茶等等吧~~~' + '\n', 'yellow'))
        icp_info = Icp_Module.icp_get(args.icp)
        print(icp_info)
        results = Poc_Module.verify_all_pocs(icp_info)
        print(results)

    elif args.url:
        print(colored('[*]FUZZ开始了，喝口茶等等吧~~~' + '\n', 'yellow'))
        print(colored(f"Scanning URL: {args.url}",'yellow'))

        if args.poc:
            results = Poc_Module.verify_all_pocs(args.url)
            for filename, result in results:
                print(colored(f"Result for {filename}: {'Success' if result else 'Fail'}",'green'))
    elif args.urls:
        print(colored('[*]FUZZ开始了，喝口茶等等吧~~~' + '\n', 'yellow'))
        urls = Url_Module.get_url(args.urls)
        if args.poc:
            for i in range(len(urls)):
                results = Poc_Module.verify_all_pocs(urls[i])
                print(results)

    else:
        print(colored("Error: 请检查参数是否输入错误", "red"))


if __name__ == "__main__":
    art = """
##########################################################################
#   ______   __        __        ________  __    __  ________  ________  #
#  /      \ /  |      /  |      /        |/  |  /  |/        |/        | #
# /$$$$$$  |$$ |      $$ |      $$$$$$$$/ $$ |  $$ |$$$$$$$$/ $$$$$$$$/  #
# $$ |__$$ |$$ |      $$ |      $$ |__    $$ |  $$ |    /$$/      /$$/   #
# $$    $$ |$$ |      $$ |      $$    |   $$ |  $$ |   /$$/      /$$/    #
# $$$$$$$$ |$$ |      $$ |      $$$$$/    $$ |  $$ |  /$$/      /$$/     #
# $$ |  $$ |$$ |_____ $$ |_____ $$ |      $$ \__$$ | /$$/____  /$$/____  #
# $$ |  $$ |$$       |$$       |$$ |      $$    $$/ /$$      |/$$      | #
# $$/   $$/ $$$$$$$$/ $$$$$$$$/ $$/        $$$$$$/  $$$$$$$$/ $$$$$$$$/  #
#                                                                        #
##########################################################################     
    """  # 艺术字
    print(colored(art , 'purple'))
    print(colored('https://github.com/zhiyuanfa/AllFuzz 欢迎指点\n','yellow'))
    main()
