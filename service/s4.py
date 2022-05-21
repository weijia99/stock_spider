import time

from utils.spider import Spider

if __name__ == '__main__':
    start = time.time()
    threads = []
    # 创建爬虫进程
    link_range_list = [(40, 99), (100, 199), (200, 299), (300, 400)]
    s1 = Spider("thread-3",link_range_list[3])
    time.sleep(20)

    s1.run()
