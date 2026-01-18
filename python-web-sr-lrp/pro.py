import os
import subprocess
import requests
from playwright.sync_api import sync_playwright

import dotenv
dotenv.load_dotenv()
# --- 配置区 ---
START_ID = os.getenv("START_ID")
END_ID = os.getenv("END_ID")
BASE_URL = os.getenv("BASE_URL")
SAVE_DIR =os.getenv("SAVE_DIR")

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


def get_m3u8_by_sniffing(target_url):
    """负责解析单个页面中的 m3u8"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0...")
        page = context.new_page()

        m3u8_list = []
        # 修改拦截逻辑：支持多视频（收集所有找到的 m3u8）
        page.on("request", lambda req: m3u8_list.append(req.url) if ".m3u8" in req.url else None)

        try:
            print(f"🔍 正在扫描: {target_url}")
            page.goto(target_url, wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(3000)  # 给异步加载留点时间
        except Exception as e:
            print(f"⚠️ 访问超时或出错: {target_url}")

        browser.close()
        return list(set(m3u8_list))  # 去重


def download_with_ffmpeg(m3u8_url, filename):
    """调用 FFmpeg 汇总"""
    save_path = os.path.join(SAVE_DIR, f"{filename}.mp4")
    cmd = [
        'ffmpeg', '-headers', 'User-Agent: Mozilla/5.0...\r\n',
        '-i', m3u8_url,
        '-c', 'copy', '-y', save_path
    ]
    # 隐藏详细日志，只看汇总进度
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)



    # 暂时不要使用 stdout=subprocess.DEVNULL，我们要看报错信息！


# --- 主逻辑 ---
def batch_work():
    for i in range(START_ID, END_ID + 1):
        full_url = f"{BASE_URL}{i}/"

        # 1. 快速检测页面是否存在（处理空缺）
        try:
            res = requests.head(full_url, timeout=5)
            if res.status_code == 404:
                print(f"⏩ 跳过空缺 ID: {i}")
                continue
        except:
            pass

        # 2. 嗅探链接
        m3u8_urls = get_m3u8_by_sniffing(full_url)

        # 3. 处理多视频情况
        if not m3u8_urls:
            print(f"❓ ID {i} 页面存在但未找到视频")
            continue

        for index, m3u8 in enumerate(m3u8_urls):
            suffix = f"_{index}" if len(m3u8_urls) > 1 else ""
            file_name = f"video_{i}{suffix}"
            print(f"🚀 开始下载汇总: {file_name}")
            download_with_ffmpeg(m3u8, file_name)


if __name__ == "__main__":
    batch_work()