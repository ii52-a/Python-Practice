import re
from lxml import etree
import requests
from fake_useragent import UserAgent
import time
import chardet  #处理网页编码问题
from urllib.parse import urljoin,urlparse #安全续urls
class Tools:

    headers = {
        "User-Agent": UserAgent().random,
    }

    @staticmethod
    def fg(num=15):
        print("="*num)

    """文件名称过滤"""
    @staticmethod
    def clean_filename(filename:list | str) -> str:
        illegal_chars = r'[\\/*?:"<>|]'
        if isinstance(filename, list):
            filename = filename[0] if filename else "未知标题"
        return re.sub(illegal_chars, ',', filename)

    @staticmethod
    def get(url,retry_count:int=3)-> any:
        for attempt in range(retry_count):
            try:
                response = requests.get(url, headers=Tools.headers, timeout=10)
                response.encoding = "utf-8"
                response.raise_for_status()
                detect_result = chardet.detect(response.content)  # 检测编码自动处理
                actual_encoding = detect_result['encoding'] or 'utf-8'  # 获得自动编码后的编码形式
                html_text = response.content.decode(actual_encoding, errors='replace')

                html = etree.HTML(html_text)
                return html
            except requests.RequestException as e:
                print(f"请求失败 (尝试 {attempt + 1}/{retry_count}): {e}")
                if attempt < retry_count - 1:
                    time.sleep(2)
        return None
    @staticmethod
    def try_to_get(url:str)-> bool:
        if requests.get(url, headers=Tools.headers, timeout=10).status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def scrape_content(etr:any)-> any:
        secrets =[
            '//div[contains(@class,"content") or contains(@id,"content") and count(.//p) > 10]/p/text()',
            '//div[contains(@class,"neirong") or contains(@id,"neirong") and count(.//p) > 10]/p/text()',
            '//div[count(.//p > 12)]/p/count'  #最宽泛搜寻

        ]
        content=""
        try:
            for secret in secrets:
                content=etr.xpath(secret)
                if content:
                    return content
            else:
                return None
        except Exception as e:
            Tools.fg(20)
            print("文章截错误>>"+str(e))
            return None

    @staticmethod
    def scrape_title(etr:any)-> any:
        secrets = [
            '//h1[contains(@class,"title") or contains(@id,"title") and contains(text(),"第")]/p/text()',
            '//h1[contains(@class,"biaoti") or contains(@id,"biaoti") and contains(text(),"第"]/p/text()',
            '//dev[contains(text(),"第") and contains(text(),"章")]/text()',  # 最宽泛搜寻
            '//h1[contains(text(),"第") and contains(text(),"章")]/text()',  # 最宽泛搜寻
            '//dev[contains(text(),"第") and contains(text(),"卷")]/text()',  # 最宽泛搜寻
            '//h1[contains(text(),"第") and contains(text(),"卷")]/text()',  # 最宽泛搜寻
        ]
        try:
            for secret in secrets:
                title=etr.xpath(secret)
                if title:
                    return title[0]
            return None
        except Exception as e:
            Tools.fg(20)
            print("章节名获取失败:"+str(e))
            return None

class ChapterUrlExtractor:
    def __init__(self,url:str):
        # 识别策略
        self.strategies = [self.strategy_first,self.strategy_second]

        # 书籍信息
        self.meta_title = ""
        self.meta_author = ""

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # url信息
        self.url = url
        self.etree = None
        self.meta_lastest_url = None

    """检验是否存在分路由url省略并尝试补全"""

    # 返回urls列表
    def check_and_add_url(self, urls: list) -> list:
        """检测非基础域名"""
        if urls and not urls[0].startswith(('http://', 'https://')):
            # 确定基础URL
            if self.meta_lastest_url and self.meta_lastest_url.startswith(('http://', 'https://')):
                # 从meta_latest_url提取基础域名
                parsed = urlparse(self.meta_lastest_url)
                base_url = f"{parsed.scheme}://{parsed.netloc}"
            else:
                # 使用首页URL作为基础
                base_url = self.url

            # 补全所有URL
            completed_urls = [urljoin(base_url, url) for url in urls]
            print(f"主域名锁定成功:  {base_url}")
            return completed_urls
        return urls

    """尝试初始化meta"""
    def get_meta_info(self) -> bool:
        """尝试获取网页的meta信息"""
        try:
            # 提取meta标签
            self.meta_author = self.etree.xpath('//meta[contains(@property, "author")]/@content')
            self.meta_title = self.etree.xpath('//meta[contains(@property, "title")]/@content')
            self.meta_lastest_url = self.etree.xpath(
                '//meta[contains(@property, "lastest") and contains(@property, "url")]/@content')

            #备用url获取
            if not self.meta_lastest_url:
                self.meta_lastest_url = self.etree.xpath(
                    '//meta[contains(@property, "latest") and contains(@property, "url")]/@content'
                )

            #安全获取meta信息
            if self.meta_lastest_url and self.meta_author and self.meta_title:
                self.meta_title = self.meta_title[0]
                self.meta_author = self.meta_author[0]
                self.meta_lastest_url = self.meta_lastest_url[0]
            else:
                raise Exception("获取到meta信息")

            Tools.fg()
            print("书名:《" + self.meta_title + "》")
            print(self.meta_author)
            Tools.fg(10)

            return True

        except Exception as e:
            print(f"获取meta信息失败: {e}")
            return False

    def main(self) -> tuple[str,list] | None:
        html = Tools.get(self.url)
        self.etree = html
        try:
            if self.etree is None:
                raise Exception("etree获取失败，无法识别内容")
            if not self.get_meta_info():
                raise Exception("meta信息初始化失败")
            for strategy in self.strategies:
                try:
                    urls = strategy()
                    if urls:
                        return self.meta_title, urls
                    else:
                        continue
                except Exception as e:
                    print(f"策略{self.strategies.index(strategy)+1}识别失败: {e}")
                    Tools.fg()
                    continue
            print("urls获取失败")
            return None
        except Exception as e:
            print(f"程序启动失败: {e}")
            return None

    """策略1:检索常用目录类名称或id名称"""

    def strategy_first(self) -> list | None:
        urls=[]
        secrets=[
            '//ul[@id="chapter-list" and count(.//a)>20]//a/@href',
            '//div[@id="play_0" and count(.//a)>20]//a/@href',
            '//ul[.//a[contains(text(),"第") or contains(text(),"卷") or contains(text(),"章")] and count(.//a)>20]//a/@href',
            '//dl[.//a[contains(text(),"第") or contains(text(),"卷") or contains(text(),"章")] and count(.//a)>20]//a/@href',
        ]
        for secret in secrets:
            urls=self.etree.xpath(secret)
            if urls:
                urls=self.check_and_add_url(urls)
                if Tools.try_to_get(urls[0]):
                    print("策略1:成功获取:" + str(len(urls)) + "章")
                    return urls
            else:
                continue
        print("策略1检索失败")
        return None

    """策略2:利用最后一章节url寻找包含所有章节url的父盒子"""

    # 返回urls列表或None
    def strategy_second(self) -> list | None:
        try:
            # print(self.meta_lastest_url)

            #安全获取后6位url保证模糊获取
            if len(self.meta_lastest_url) >= 6:
                url_suffix = self.meta_lastest_url[-6:]
            else:
                url_suffix = self.meta_lastest_url

            #尝试获取url盒子
            secrets=[
                f'//ul[.//li/a[contains(@href,"{url_suffix}")] and count(.//a) >15]/li/a/@href',
                f'//div[.//a[@href="{url_suffix}"]]',
                f'//dl[.//li/a[contains(@href,"{url_suffix}")] and count(.//a) >15]/li/a/@href'
            ]
            urls=[]
            for secret in secrets:
                urls=self.etree.xpath(secret)
                if not urls:
                    continue
                else:
                    raise Exception("获取url失败")

            urls = self.check_and_add_url(urls)
            # 过滤错误urls列表
            if Tools.try_to_get(urls[0]):
                print("策略2:成功获取:" + str(len(urls)) + "章")
                return urls
            else:
                raise Exception("无效的url列表")

        except Exception as e:
            print(f"策略2-错误: {e}")
            return None




if __name__ == '__main__':
    extractor = ChapterUrlExtractor(input("url:"))  # 创建实例
    extractor.main()  # 调用实例方法