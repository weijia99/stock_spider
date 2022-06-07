import random
import threading
import time

import requests
from lxml import etree
import re

from bean.item import item
from utils.get_proxy import getHtml
from utils.mysql_connextor import get_connector_mongo0, get_connector_mongo1


# 加入多线程，只需要进行继承类
class Spider:
    def __init__(self, name):
        """

        :param url:
        """

        self.name = name

        self.url = "http://vip.stock.finance.sina.com.cn/corp/view/vCB_BulletinGather.php?ftype=ndbg&page_index="
        self.domain = "http://vip.stock.finance.sina.com.cn/"
        self.end = 700
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                          Chrome/70.0.3538.110 \
                          Safari/537.36 "
        }
        self.sleep = 1000
        self.key1 = '党'
        self.key2 = '初心'
        self.key3 = '使命'
        self.key4 = '国家导向'
        self.key11 = '信息'
        self.key22 = '技术'
        self.key33 = '创新'
        self.page = 0
        self.ip = ""
        self.port = ""

    def get_proxy(self):
        # s = requests.get(
        #     "http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD2022667253tE4pzu/3cea1fd9b48411eb9a8f7cd30abda612?returnType=2").json()[
        #     'RESULT']
        s = requests.get(
            "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=2236d115e3ef4353bf82cedc27f8f172&orderno=YZ2022662690KsQNjf&returnType=2&count=1").json()[
            'RESULT']
        print(s)
        self.ip = s[0]["ip"]
        self.port = s[0]["port"]

    def proxy_get_data(self, url):
        """
        通用代理发送器
        :param url:
        :return:
        """
        html = getHtml(url, self.header, self.ip, self.port)
        return html

    def parse_data(self, url):
        """
        通用文章解释器
        :return:
        """
        data = self.proxy_get_data(url)
        # 编码
        flag = False
        html = None
        try:
            htmls = data.content
            flag = True
            # 代表html'不是空的
            html = htmls.decode('gbk')

        except Exception:
            try:
                if flag:
                    html = htmls.decode('gb18030')

            except:
                if flag:
                    html = htmls
                else:
                    html = None

        # 内容读取
        x_data = html
        if html is not None:
            x_data = etree.HTML(html)
        return x_data

    def get_page_url(self, url):
        """
        //*[@id="wrap"]/div[5]/table/tbody/tr[1]/th/a[1]
        :param url:
        :param :
        :return:
        """
        x_data = self.parse_data(url)
        # todo:进行修正，如果得不到就是ip被禁止了，进行更换ip
        times = 1
        while x_data is None and times < 5:
            print(f"we tried {times} times to get page {self.page},")

            # ip 被禁止了，就更新
            times += 1
            x_data = self.parse_data(url)

        if times >= 5:
            self.get_proxy()
            x_data = self.parse_data(url)

        a_list = x_data.xpath('//*[@id="wrap"]/div[5]/table/tbody//a')
        index = 0
        url_list = []
        for a in a_list:
            href = a.xpath('@href')
            if '.PDF' not in href[0]:
                href = self.domain + href[0]
                url_list.append(href)

        print(f"page {self.page} finished get_page_url")
        return url_list
        # print(url_list)

    def get_url_data(self, url_list):
        result = []
        result1 = []
        for url in url_list:
            print(url)
            x_data = self.parse_data(url)
            times = 0
            while x_data is None and times < 3:
                # 更新ip
                x_data = self.parse_data(url)
                times += 1
                print(f"we tried {times} times to get {url} ")

            if times >= 3:
                # 超过5次就更新
                self.get_proxy()
                x_data = self.parse_data(url)
                if x_data is None:
                    continue

            # //*[@id="quote_area"]/table[1]/tbody/tr/th/text()
            print(x_data.xpath('/html/head/title/text()'))
            info = x_data.xpath('/html/head/title/text()')[0]
            re_str = r'\d+'
            r = re.findall(re_str, info)
            if r:
                sid = r[0]
                print(f"{info} start to process&{sid}")

                year = r[-1]
                # print(sid, year)
            else:
                ip = self.ip
                port = self.port
                self.ip = "127.0.0.1"
                self.port = "7890"
                x_data = self.proxy_get_data(url).content.decode('gbk')
                if x_data is None:
                    continue
                else:
                    x_data = etree.HTML(x_data)
                    info = x_data.xpath('/html/head/title/text()')[0]
                    r = re.findall(re_str, info)
                    self.ip = ip
                    self.port = port
                    # print(r)
                    if not r:
                        continue
                    sid = r[0]
                    # print(f"{info} start to process&{sid}")

                    year = r[-1]
            # print(etree.tostring(x_data,encoding='gbk').decode('gbk').count("创新"))
            # content = x_data.xpath('//*[@id="content"]/p/text()')
            # print(content)进行统计
            key1 = key2 = key3 = key4 = 0
            key11 = key22 = key33 = 0
            cont = etree.tostring(x_data, encoding='gbk').decode('gbk')
            key1 += cont.count(self.key1)
            key11 += cont.count(self.key11)
            key2 += cont.count(self.key2)
            key22 += cont.count(self.key22)

            key3 += cont.count(self.key3)
            key33 += cont.count(self.key33)
            key4 += cont.count(self.key4)
            # for i in content:
            #     i = str(i)
            #     c1 = i.count(self.key1)
            #     c2 = i.count(self.key2)
            #     c3 = i.count(self.key3)
            #     c4 = i.count(self.key4)
            #     c11 = i.count(self.key11)
            #     c22 = i.count(self.key22)
            #     c33 = i.count(self.key33)
            #     if c1 > 0:
            #         key1 += c1
            #     if c2 > 0:
            #         key2 += c2
            #     if c3 > 0:
            #         key3 += c3
            #     if c4 > 0:
            #         key3 += c4
            #     if c11 > 0:
            #         key11 += c11
            #     if c22 > 0:
            #         key22 += c22
            #     if c33 > 0:
            #         key33 += c33
            if key1 != 0 or key2 != 0 or key3 != 0 or key4 != 0:
                it = dict(zip(["sid", "year", "key1", "key2", "key3", "key4"], [sid, year, key1, key2, key3, key4]))
                print("ok")
                result.append(it)
            if key11 != 0 or key22 != 0 or key33 != 0:
                it = dict(zip(["sid", "year", "key1", "key2", "key3"], [sid, year, key11, key22, key33]))

                result1.append(it)
            # t = random.uniform(0,2)
            # time.sleep(t)
        print(f"page {self.page} finished get_url_data")

        return result, result1

    def insert_list(self, result, result1):
        connector = get_connector_mongo0()
        # connector.insert_many(result)
        for i in result:
            myquery = {"sid": i["sid"], "year": i["year"]}
            connector.update_one(
                myquery,
                {'$setOnInsert': i},
                upsert=True
            )

        connector = get_connector_mongo1()
        # connector.insert_many(result)
        for i in result1:
            myquery = {"sid": i["sid"], "year": i["year"]}
            connector.update_one(
                myquery,
                {'$setOnInsert': i},
                upsert=True
            )

        print(f"page {self.page} finished insert_list")

    def test(self):
        self.ip = "127.0.0.1"
        self.port = "7890"
        url = [
            "http://vip.stock.finance.sina.com.cn//corp/view/vCB_AllBulletinDetail.php?CompanyCode=80198934&gather=1&id=8113764"]
        self.get_url_data(url)

    def run(self):
        # first : get proxy

        self.get_proxy()
        # self.ip = "127.0.0.1"
        # self.port = "7890"
        # next foreach
        for i in range(0, self.end):
            uri = self.url + str(i)
            self.page = str(i)
            url_list = self.get_page_url(uri)
            result, result1 = self.get_url_data(url_list)
            self.insert_list(result, result1)
            t = random.uniform(0, 3)  # 随机一个大于0小于9的小数
            time.sleep(t)
            print(f"page {self.page} process successfully\
                  and it will sleep {t}s")


# if __name__ == '__main__':
#     start = time.time()
#     threads = []
#     # 创建爬虫进程
#     link_range_list = [(40, 99), (100, 199), (200, 299), (300, 400)]
#


t = Spider("thread")
t.run()

# t.test()
