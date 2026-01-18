import requests


class Fetcher:
    def __init__(self,headers=None):
        self.session = requests.Session()
        self.session.headers.update(headers or {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
        })

    def get(self,url):
        response = self.session.get(url,timeout=20)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text