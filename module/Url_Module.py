urls = []
def get_url(path):
    url_file = open(f'{path}','r')
    for line in url_file:
        urls.append(line)
    return urls