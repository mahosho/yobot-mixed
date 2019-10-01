# coding=utf-8

import json
import os
import sys
import time

import requests


class Update():

    def __init__(self):
        self.__path = os.path.dirname(sys.argv[0])

    def check(self):
        if os.path.exists(os.path.join(self.__path, "version.json")):
            f = open(os.path.join(self.__path, "version.json"),
                     "r+", encoding="utf-8")
            try:
                ver = json.load(f)
            except json.decoder.JSONDecodeError:
                ver = {"checktime": 0, "localver": 2000}
        else:
            f = open(os.path.join(self.__path, "version.json"),
                     "w", encoding="utf-8")
            ver = {"checktime": 0, "localver": 2000}
        now = int(time.time())
        if ver["checktime"] < now:  # 到检查时间
            url = 'https://yuudi.github.io/yobot/ver.json'
            response = requests.get(url)
            if response.status_code != 200:  # 网页返回错误
                f.close()
                return None
            latest = json.loads(response.text)
            if latest["version"] > ver["localver"]:
                f.close()
                return "有新的版本可用，发送“#更新”唤起更新程序"
            else:
                ver["checktime"] = now + 80000  # 每8万秒检查一次
                f.seek(0)
                f.truncate()
                json.dump(ver, f, indent=2)
                f.close()
                return None
        else:
            f.close()
            return None

    # def update(self):
    #     if os.path.exists(os.path.join(self.__path, "UpdateApp", "UpdateApp.exe")):
    #         return "方式错误，此方式不应当由本程序发起"
    #     else:
    #         return "更新程序丢失"
