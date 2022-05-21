import requests



def get_proxy():
    return requests.get("http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD20225218812zLcpoL/f2fe8224e53411eb9a8f7cd30abda612?returnType=2").json()

    # return requests.get("http://45.82.153.4:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://45.82.153.4:5010/delete/?proxy={}".format(proxy))


# your spider code

def getHtml(url, headers,ip,port):
    # ....
    retry_count = 5
    # s = get_proxy()['RESULT']
    # ip = s["wanIp"]
    # port = s["proxyport"]
    proxy = ip+":"+port
    while retry_count > 0:
        try:
            html = requests.get(url, proxies={"http": "http://{}".format(proxy)}, headers=headers)
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    # delete_proxy(proxy)
    return None

# s = get_proxy()['RESULT']
# print(s)
# ip = s["wanIp"]
# port = s["proxyport"]
# print(ip,port)