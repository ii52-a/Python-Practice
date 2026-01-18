from pathlib import Path

import requests


class Downloader:
    def __init__(self,save_dir="videos"):
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        self.save_dir = save_dir

    def download(self,url):
        filename = url.split("/")[-1]
        path=self.save_dir/filename

        with requests.get(url, stream=True) as r:
            r.raise_for_status()

            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
        print(f"Downloaded {path}")
