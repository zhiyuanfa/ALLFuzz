import argparse
import asyncio
from module import Poc_Module
from module import Icp_Module
from module import Str_Module
from globals.Global import colored
from module.Brute_Module import subdomain_brute


def main():
    parser = argparse.ArgumentParser(description='[ALLFUZZ]-----[++一款全方位FUZZ工具++]-----[zhengint]')
    parser.add_argument('--str','-s', help='目标输入点，如："python AllFuzz.py --str str"', type=str)
    parser.add_argument('--file','-f', help='引入文件，如："python AllFuzz.py --file path/file.txt"', type=str)
    parser.add_argument('--icp', help='执行ICP备案信息检测，需要配合--url/--file目前支持传入公司名查询',action='store_true')
    parser.add_argument('--poc', help='执行POC验证，需要配合--url/--file POC验证默认关闭', action='store_true')
    parser.add_argument('--sub',help='执行子域名爆破操作，需要配合--url/--file POC验证默认关闭',type=str)
    parser.add_argument('--time',help='时间参数，可以用来调整爆破延迟时间,各爆破模块默认为5',type=str)

    args = parser.parse_args()

    # 引用url参数模块
    if args.str:
        print(colored('[*]FUZZ开始了，喝口茶等等吧~~~' + '\n', 'yellow'))
        print(colored(f"Scanning targe: {args.str}",'yellow'))
        if args.icp:
            Icp_Module.icp(args.str)
        if args.poc:
            Poc_Module.poc(args.str)
            print(colored('\n[+++]扫描结果存放在日志文件中，FUZZ测试，结果可能有所偏差，还需要手工验证-----log.txt','green'))


    # 引入目标模块
    if args.file:
        print(colored('[*]FUZZ开始了，喝口茶等等吧~~~' + '\n', 'yellow'))
        strs = Str_Module.file(args.file)
        urls = []
        if args.icp:
            for i in range(len(strs)):
                urls.append(Icp_Module.icp(strs[i]))
            print(colored(f'{urls}','green'))
            if args.poc:
                for i in range(len(urls)):
                    Poc_Module.poc(urls[i])
                print(colored('\n[+++]扫描结果存放在日志文件中，FUZZ测试，结果可能有所偏差，还需要手工验证-----log.txt','green'))
        elif args.poc:
            for i in range(len(strs)):
                Poc_Module.poc(strs[i])
            print(colored('\n[+++]扫描结果存放在日志文件中，FUZZ测试，结果可能有所偏差，还需要手工验证-----log.txt','green'))

    # 子域名爆破模块
    if args.sub:  # 根据参数名称调整
        found_subdomains = asyncio.run(subdomain_brute(args.sub,args.time))  # 调用子域名爆破函数
        for url, (current_time, status) in found_subdomains.items():
            print(colored(f"[{current_time}]------ {url} ------[Status: {status}]", 'green'))

    elif not args:
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
    print(colored(art, 'purple'))
    print(colored('https://github.com/zhiyuanfa/AllFuzz 欢迎指点\n','yellow'))
    main()
