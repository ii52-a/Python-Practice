"""请求"""
import re

import requests
#lxml
from lxml import etree
import os
from fake_useragent import UserAgent

class Tools:

    @classmethod
    def fg(cls,num=15):
        print("="*num)

    @classmethod
    def clean_filename(cls,filename):
        illegal_chars = r'[\\/*?:"<>|]'
        if isinstance(filename, list):
            filename = filename[0] if filename else "未知标题"
        return re.sub(illegal_chars, ',', filename)

class Scraper:


    def __init__(self):
        self.url = None
        self.url = ""
        self.headers = {
            "User-Agent": UserAgent().random,
        }
        self.response = None
        self.etr = None
        self.novel_folder = ""
        self.frame_url = None
        self.book_title = ""

    def get(self):
        self.response = requests.get(self.url, headers=self.headers)
        self.response.encoding = "utf-8"
        self.etr = etree.HTML(self.response.text)
    def scrape_init(self):
        try:
            self.url = input("输入第一章url:")
            Tools.fg()
            self.get()
            print("url添加成功")
        except Exception as e:
            print("响应失败:"+str(e))
            return False

        try:
            self.etr = etree.HTML(self.response.text)
            self.book_title = Tools.clean_filename(self.etr.xpath('//ol[@class="breadcrumb"]/li[2]/a/text()'))
            self.frame_url=self.etr.xpath('//ol[@class="breadcrumb"]/li[1]/a/@href')[0]
            if not self.frame_url or not self.book_title:
                 raise Exception("书名或首页获取失败")
            print("书名:《" + self.book_title + "》")
        except Exception as e:
            print("书名添加失败:"+str(e))
            self.book_title = "未知标题"
            return False

        try:
            self.novel_folder = self.book_title
            os.makedirs(self.novel_folder, exist_ok=True)
            print("初始化成功")
            Tools.fg(30)
            return True
        except Exception as e:
            print("初始化失败:"+str(e))
            return False

    def scrape_loop(self):
        while self.url !=self.frame_url and self.url:
            self.get()
            info = '\n\n'.join(self.etr.xpath('//div[@id="content"]/p/text()')[2:])
            title = Tools.clean_filename(self.etr.xpath('string(//div[contains(@class,"m-title")])').strip())
            next_url = self.etr.xpath('//div[@class="m-zpage"]/ul/li[2]/a/@href')
            file_path = os.path.join(self.novel_folder, f'{title}.txt')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(title + '\n\n')
                f.write(info)
            print("成功添加:"+title)
            self.url = next_url[0]

    def debug(self):
        print(self.frame_url)
        print(self.url)
        print(self.novel_folder)

def main():
    scraper = Scraper()
    if scraper.scrape_init():
        if input("任意键开始爬取")=="debug":
            scraper.debug()
        else:
            scraper.scrape_loop()


if __name__ == '__main__':
    main()