# coding=utf-8
import json
import os.path
import sqlite3
import sys

import requests


class Gacha():
    URL = "http://api.yobot.xyz/v2/pool/?type=json"

    def __init__(self, baseinfo):
        """
        baseinfo=[群号，QQ号, 群名片]（字符串）
        """
        self.__groupid = baseinfo[0]
        self.__qqid = baseinfo[1]
        self.__nickname = baseinfo[2]
        self.__path = os.path.dirname(sys.argv[0])
        self.txt_list = []
        if os.path.exists(os.path.join(self.__path, "pool.json")):
            with open(os.path.join(self.__path, "pool.json"), "r", encoding="utf-8") as f:
                self.__data = json.load(f)
        else:
            res = requests.get(self.URL)
            assert res.status_code == 200, "服务器不可用"
            try:
                self.__data = json.loads(res.text)
            except:
                print("服务器错误")
                exit()

    def __del__(self):
        pass
