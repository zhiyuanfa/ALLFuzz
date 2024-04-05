import argparse
from module import Poc_Module
from module import Icp_Module
from module import Str_Module
from globals.Global import colored


def main():
    parser = argparse.ArgumentParser(description='[ALLFUZZ]-----[++一款全方位FUZZ工具++]-----[zhengint]')
    parser.add_argument('--str','-s', help='目标输入点，如："python AllFuzz.py --str str"', type=str)
    parser.add_argument('--file','-f', help='引入文件，如："python AllFuzz.py --file path/file.txt"', type=str)
    parser.add_argument('--icp', help='执行ICP备案信息检测，需要配合--url/--file目前支持传入公司名查询',action='store_true')
    parser.add_argument('--poc', help='执行POC验证，需要配合--url/--filePOC验证默认关闭', action='store_true')

    args = parser.parse_args()

    # 如果引用url参数
    if args.str:
        print(colored('[*]FUZZ开始了，喝口茶等等吧~~~' + '\n', 'yellow'))
        print(colored(f"Scanning targe: {args.str}",'yellow'))
        if args.icp:
            Icp_Module.icp(args.str)
        if args.poc:
            Poc_Module.poc(args.str)
            print(colored('\n[+++]扫描结果存放在日志文件中，FUZZ测试，结果可能有所偏差，还需要手工验证-----log.txt','green'))


    # 如果引用file参数
    if args.file:
        print(colored('[*]FUZZ开始了，喝口茶等等吧~~~' + '\n', 'yellow'))
        strs = Str_Module.file(args.file)
        urls = []
        if args.icp:
            for i in range(len(strs)):
                urls.append(Icp_Module.icp(strs[i-1]))
            print(colored(f'{urls}','green'))
            if args.poc:
                for i in range(len(urls)):
                    Poc_Module.poc(urls[i-1])
                print(colored('\n[+++]扫描结果存放在日志文件中，FUZZ测试，结果可能有所偏差，还需要手工验证-----log.txt','green'))
        elif args.poc:
            for i in range(len(strs)):
                Poc_Module.poc(strs[i-1])
            print(colored('\n[+++]扫描结果存放在日志文件中，FUZZ测试，结果可能有所偏差，还需要手工验证-----log.txt','green'))

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
