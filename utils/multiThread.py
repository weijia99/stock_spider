import requests
import threading
import time

start = time.time()


# 为线程定义一个函数
class myThread(threading.Thread):
    def __init__(self, name, link_range):
        threading.Thread.__init__(self)
        self.name = name
        self.link_range = link_range

    def run(self):
        print("Starting " + self.name)
        crawl(self.name, self.link_range)
        print("Exiting " + self.name)


def crawl(threadNmae, link_range):
    for i in range(link_range[0], link_range[1] + 1):
        try:
            r = requests.get(URLs[i], timeout=1.5)
            print(threadNmae, r.status_code, URLs[i])
        except Exception as e:
            print(threadNmae, "Error: ", e)


threads = []
link_range_list = [(40,99 ), (100, 199), (200, 299), (300, 400)]

for i in range(1, 5):
    # 创建4个新线程
    thread = myThread("Thread-" + str(i), link_range=link_range_list[i - 1])
    # 开启新线程
    thread.start()
    # 添加新线程到线程列表
    threads.append(thread)

# 等待所有线程完成
for thread in threads:
    thread.join()

end = time.time()
print("简单多线程爬虫耗时：{} s".format(end - start))
print("Exiting Main Thread")
