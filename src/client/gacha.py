# coding=utf-8
import json5
import os.path
import sqlite3
import sys

import requests


class Gacha():
    URL = "http://api.yobot.xyz/v2/pool/?type=json5"

    def __init__(self, baseinfo):
        """
        baseinfo=[群号，QQ号, 群名片]（字符串）
        """
        self.__groupid = baseinfo[0]
        self.__qqid = baseinfo[1]
        self.__nickname = baseinfo[2]
        self.__path = os.path.dirname(sys.argv[0])
        self.txt_list = []

    def __del__(self):
        pass

    def load(self):
        if not os.path.exists(os.path.join(self.__path, "pool.json5")):
            res = requests.get(self.URL)
            assert res.status_code == 200, "服务器不可用"
            with open(os.path.join(self.__path, "pool.json5"), "w", encoding="utf-8") as f:
                f.write(res.text)
            try:
                self.__data = json5.loads(res.text)
            except:
                self.txt_list.append("服务器响应错误")
                return 1
        else:
            with open(os.path.join(self.__path, "pool.json5"), "r", encoding="utf-8") as f:
                try:
                    self.__data = json5.load(f)
                except:
                    self.txt_list("卡池文件解析错误，请检查卡池文件语法，或者删除卡池文件")
                    return 2
