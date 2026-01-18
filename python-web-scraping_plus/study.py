import json
import os

import requests
import dotenv
dotenv.load_dotenv()
headers = {"User-Agent": "Mozilla/5.0","Cookie":os.getenv("COOKIE"),"Referer": "https://www.bilibili.com/"}
def get_bilibili_info(bvid):
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


def get_play_urls(bvid, cid):
    url = f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&fnval=16"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def pick_best_video(dash_video_list):
    # 优先顺序：80 > 64 > 32 > 16
    prefer_ids = [80, 64, 32, 16]
    # print(view_json(dash_video_list))

    for pid in prefer_ids:

        for item in dash_video_list:
            # print(type(item))
            if item["id"] == pid:
                return item

    return dash_video_list[0]  # fallback

def download(url, filename):
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)



def view_json(data):
    return json.dumps(data, indent=4, ensure_ascii=False)
if __name__ == "__main__":
    bvid = "BV19f24BSErY"
    info = get_bilibili_info(bvid)
    cid = info["data"]["pages"][0]["cid"]

    # print("cid=", cid)
    #
    data = get_play_urls(bvid, cid)["data"]["dash"]
    # print(view_json(data))
    # print(json.dumps(data, indent=4, ensure_ascii=False))
    # print(json.dumps(data["data"]["dash"]["video"],indent=4,ensure_ascii=False))
    audio = data["audio"][0]
    video = data["video"]
    # print(view_json(video))
    items=pick_best_video(video)

    video_df=items["baseUrl"]
    audio_df=audio["baseUrl"]

    download(video_df, "video.m4s")
    download(audio_df, "audio.m4s")
