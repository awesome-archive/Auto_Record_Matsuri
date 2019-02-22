import json
from urllib import request
from time import strftime, localtime, time
from os import getcwd, mkdir


def gethtml(url, enable_proxy, proxy):
    if enable_proxy == 1:
        proxy_support = request.ProxyHandler({'http': '%s' % proxy, 'https': '%s' % proxy})
        opener = request.build_opener(proxy_support)
        request.install_opener(opener)
    # 此处一定要注明Language, 见commit cda7031
    fake_headers = {
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
    }
    req = request.Request(url, headers=fake_headers)
    response = request.urlopen(req)
    html = response.read()
    html = html.decode('utf-8', 'ignore')
    return html


def echo_log(log):
    today = strftime('%m-%d', localtime(time()))
    print(log)
    while True:
        try:
            with open(getcwd() + rf"\log\log-{today}.log", 'a') as logs:
                logs.write(log + "\n")
            break
        # 没有log文件夹的话就新建一个
        except FileNotFoundError:
            mkdir("log")


# 关于机器人HTTP API https://cqhttp.cc/docs/4.7/#/API
def bot(host, group_id, message):
    # 传入JSON时，应使用这个UA
    headers = {'Content-Type': 'application/json'}
    # 将消息输入dict再转为json
    # 此处不应该直接使用HTTP GET的方式传入数据
    _msg = {
        'group_id': group_id,
        'message': message
    }
    msg = json.dumps(_msg).encode('utf-8')
    req = request.Request(f'http://{host}/send_group_msg', headers=headers, data=msg)
    request.urlopen(req)

