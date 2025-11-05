"""请求"""

#lxml

import os

import threading
import queue
import time


from tools import Tools, ChapterUrlExtractor


class WorkerThread(threading.Thread):
    def __init__(self,thread_id,novel_folder,work_queue,stop_event):
        super().__init__()
        self.thread_id = thread_id
        self.work_queue = work_queue
        self.stop_event = stop_event
        self.novel_folder=novel_folder



    def run(self) -> None:
        print(f"进程 {self.thread_id} 启动成功")
        while not self.stop_event.is_set():
            try:
                #获取任务url
                url=self.work_queue.get(timeout=1)
                #标定任务etree
                etr = Tools.get(url)
                """获取信息"""

                info = '\n\n'.join(Tools.scrape_content(etr))
                title = Tools.clean_filename(Tools.scrape_title(etr)).strip()
                file_path = os.path.join(self.novel_folder, f'{title}.txt')

                """保存章节"""
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(title + '\n\n')
                    f.write(info)
                """反馈"""
                print(f"进程{self.thread_id}>>成功添加:"+title)
                #标记任务结束
                self.work_queue.task_done()
            except queue.Empty:  #进程短暂休眠
                time.sleep(0.2)
                continue
        print(f"退出进程 {self.thread_id}")


class Scraper:


    def __init__(self):
        self.urls = None
        self.url = ""

        self.etr = None
        self.book_title = ""

        self.threads = []
        self.stop_event = threading.Event()
        self.work_queue = queue.Queue()



    def thread_create(self,t:int=5,novel_folder:str="") -> None:
        self.threads = []
        try:
            for i in range(t):
                thread = WorkerThread(i + 1,self.book_title, self.work_queue,self.stop_event)
                thread.start()
                self.threads.append(thread)
        except Exception as e:
            print("进程创建失败:"+str(e))
        print(f"\n{t}进程创建成功")
        Tools.fg()

    def scrape_init(self) -> bool:
        self.url=input("首页url:")




        try:
            extractor = ChapterUrlExtractor(self.url)
            extractor_result = extractor.main()
            self.book_title = extractor_result[0]
            self.urls = extractor_result[1]
            os.makedirs(self.book_title, exist_ok=True)
            print("初始化成功")
            Tools.fg(30)
            return True
        except Exception as e:
            print("初始化失败:"+str(e))
            return False

    def scrape_url_loop(self) -> None:
        self.thread_create(10)

        Tools.fg(20)
        for i in self.urls:
            self.work_queue.put(i)
        print("进程分配完成")

        Tools.fg(10)

    def debug(self) -> None:
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