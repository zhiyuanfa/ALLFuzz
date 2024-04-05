#颜色模块
def colored(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "purple": "\033[35m",
        "white": "\033[97m"
    }
    return colors.get(color, colors["white"]) + text + "\033[0m"