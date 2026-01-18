from VideoCrawler import VideoCrawler


if __name__ == '__main__':
    url=input()
    crawler=VideoCrawler(url)
    crawler.run()