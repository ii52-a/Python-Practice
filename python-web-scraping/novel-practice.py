"""请求"""
import re

import requests
#lxml
from lxml import etree
import os
from fake_useragent import UserAgent

import threading
import queue
import time

class WorkerThread(threading.Thread):
    def __init__(self,thread_id,novel_folder,work_queue,stop_event):
        super().__init__()
        self.thread_id = thread_id
        self.work_queue = work_queue
        self.stop_event = stop_event


        self.novel_folder=novel_folder



    def run(self):
        print(f"进程 {self.thread_id} 启动成功")
        while not self.stop_event.is_set():
            try:
                #获取任务url
                url=self.work_queue.get(timeout=1)
                #标定任务etree
                etr=Tools.get(url)
                info = '\n\n'.join(etr.xpath('//div[@id="content"]/p/text()')[2:])
                title = Tools.clean_filename(etr.xpath('string(//div[contains(@class,"m-title")])').strip())
                file_path = os.path.join(self.novel_folder, f'{title}.txt')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(title + '\n\n')
                    f.write(info)
                print(f"进程{self.thread_id}>>成功添加:"+title)
                self.work_queue.task_done()
            except queue.Empty:
                time.sleep(0.5)
                continue
        print(f"退出进程 {self.thread_id}")

class Tools:
    headers = {
        "User-Agent": UserAgent().random,
    }
    @classmethod
    def fg(cls,num=15):
        print("="*num)

    @classmethod
    def clean_filename(cls,filename):
        illegal_chars = r'[\\/*?:"<>|]'
        if isinstance(filename, list):
            filename = filename[0] if filename else "未知标题"
        return re.sub(illegal_chars, ',', filename)
    @classmethod
    def get(cls,url,retry_count=3):
        for attempt in range(retry_count):
            try:
                response = requests.get(url, headers=cls.headers, timeout=10)
                response.encoding = "utf-8"
                response.raise_for_status()
                return etree.HTML(response.text)
            except requests.RequestException as e:
                print(f"请求失败 (尝试 {attempt + 1}/{retry_count}): {e}")
                if attempt < retry_count - 1:
                    time.sleep(2)
        return None
class Scraper:


    def __init__(self):
        self.url = None
        self.url = ""

        self.etr = None
        self.book_title = ""

        self.threads = []
        self.stop_event = threading.Event()
        self.work_queue = queue.Queue()



    def thread_create(self,t=5,novel_folder=""):
        self.threads = []
        try:
            for i in range(t):
                thread = WorkerThread(i + 1,novel_folder, self.work_queue,self.stop_event)
                thread.start()
                self.threads.append(thread)
        except Exception as e:
            print("进程创建失败:"+str(e))
        print(f"\n{t}进程创建成功")
        Tools.fg()

    def scrape_init(self):
        try:
            self.url = input("输入首页url:")
            Tools.fg()
            self.etr=Tools.get(self.url)
            print("url添加成功")
        except Exception as e:
            print("响应失败:"+str(e))
            return False

        try:
            self.book_title = Tools.clean_filename(self.etr.xpath('//div[@class="m-infos"]/h1/text()')[0])
            if not self.book_title:
                 raise Exception("书名获取失败")
            print("书名:《" + self.book_title + "》")
            self.thread_create(5,self.book_title)
        except Exception as e:
            print("书名添加失败:"+str(e))
            self.book_title = "未知标题"
            return False

        try:
            os.makedirs(self.book_title, exist_ok=True)
            print("初始化成功")
            Tools.fg(30)
            return True
        except Exception as e:
            print("初始化失败:"+str(e))
            return False

    def scrape_url_loop(self):
        urls=self.etr.xpath('//div[@id="play_0"]/ul/li/a/@href')
        Tools.fg(20)
        for i in urls:
            self.work_queue.put(i)
        print("进程分配完成")
        Tools.fg(10)

    def debug(self):
        print(self.url)
        print(self.book_title)

def main():
    scraper = Scraper()
    if scraper.scrape_init():
        if input("任意键开始爬取")=="debug":
            scraper.debug()
        else:
            scraper.scrape_url_loop()
            scraper.work_queue.join()
            scraper.stop_event.set()
            for t in scraper.threads:
                t.join()

            print("success")



if __name__ == '__main__':
    main()