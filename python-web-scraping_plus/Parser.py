import re

from bs4 import BeautifulSoup
class Parser:


    @staticmethod
    def extract_bvid(url):
        patten=r"BV[0-9A-Za-z]+"
        match=re.search(patten,url)
        if match:
            return match.group(0)
        return None



    def parse_video_links(self,html):
        soup=BeautifulSoup(html,'lxml')
        video_tags=soup.find_all("video")

        result=[]
        for video_tag in video_tags:
            video_link=video_tag.get("src")
            if video_link:
                result.append(video_link)

        return result


if __name__=="__main__":
    url=input("Enter the url: ")
    print(Parser().extract_bvid(url))