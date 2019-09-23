import threading
import time
from urllib import request  # 导入模块
import json
import requests
import ssl

# 自定义请求头
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"}

exec_count = 0
stage_cache = ""
open_number_cache = ""


def get_open(url):
    try:
        print("------------------- get_open start.")
        ssl._create_default_https_context = ssl._create_unverified_context
        # 进行网络请求数据
        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        html = response.read()
        json_text = json.loads(html.decode('utf-8'))
        content = json_text['content']
        last_open = content['lastOpen']
        stage = last_open['seasonId']
        open_number = last_open['nums']
        open_number_str = open_number[0] + "," + open_number[1] + "," + open_number[2] + "," + open_number[3] + "," + open_number[4]
        print(stage + "   " + open_number[0] + "," + open_number[1] + "," + open_number[2] + "," + open_number[3] + "," + open_number[4])
    except Exception as e:
        print(e)
    finally:
        print("------------------- get_open complete.")
    return stage, open_number_str


def f1_11x5(stage, open_number, lottery_type):
    params = {'openList[0].stage': stage,
              'openList[0].openNumber': open_number,
              'openList[0].lotteryType': lottery_type
              }
    try:
        r = requests.post("http://localhost:1080/openNumber/open", data=params)
    except Exception as e:
        print(e)
    finally:
        print("------------------- request open complete.")
        r.close()


def heart_beat():
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    global stage_cache, open_number_cache

    url = "https://web.ryipt77.com/lotts/f1_11x5/info"
    stage, open_number = get_open(url)

    if stage != stage_cache and open_number != open_number_cache:
        f1_11x5(stage, open_number, "f1_11x5")

    stage_cache = stage
    open_number_cache = open_number

    global exec_count
    exec_count += 1
    # 15秒后停止定时器
    # if exec_count < 15:
    # 5秒触发一次
    threading.Timer(10, heart_beat).start()


heart_beat()
