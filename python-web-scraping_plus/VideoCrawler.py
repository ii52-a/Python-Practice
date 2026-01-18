from Downloader import Downloader
from Parser import Parser
from Fetcher import Fetcher

class VideoCrawler:
    def __init__(self,start_url):
        self.start_url= start_url
        self.fetcher=Fetcher()
        self.parser=Parser()
        self.downloader=Downloader()

    def run(self):
        """
            fetcher-> parser-> downloader
        :return:
        """
        print("Getting video links...")
        html=self.fetcher.get(self.start_url)

        print("Parsing video links...")

        links=self.parser.parse_video_links(html)

        if not links:
            print("No video links found.")
            return

        print("Downloading video links...")
        for link in links:
            self.downloader.download(link)
        print("Done.")

if __name__ == '__main__':
    url=input("Enter the url: ")
    video=VideoCrawler(url)
    video.run()