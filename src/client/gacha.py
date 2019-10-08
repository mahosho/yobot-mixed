# coding=utf-8
import os.path
import random
import sqlite3
import sys

import json5
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
                self.__pool = json5.loads(res.text)
            except:
                self.txt_list.append("服务器响应错误")
                return 1
        else:
            with open(os.path.join(self.__path, "pool.json5"), "r", encoding="utf-8") as f:
                try:
                    self.__pool = json5.load(f)
                except:
                    self.txt_list.append("卡池文件解析错误，请检查卡池文件语法，或者删除卡池文件")
                    return 2
        return 0

    def result(self):
        prop = 0.
        result_list = []
        for p in self.__pool["pool"].values():
            prop += p["prop"]
        resu = random.random() * prop
        for _ in range(10):
            resu_i = resu
            for p in self.__pool["pool"].values():
                resu_i -= p["prop"]
                if resu_i < 0:
                    result_list.append(p["prefix"]+random.choice(p["pool"]))
                    break
        return result_list

    def gacha(self):
        db_exists = os.path.exists(os.path.join(self.__path, "collections.db"))
        db_conn = sqlite3.connect(os.path.join(self.__path, "collections.db"))
        db = db_conn.cursor()
        if not db_exists:
            db.execute(
                '''CREAT TABLE Colle(
                qqid INT PRIMARY KEY
                nickname TEXT
                colle BLOB
                times SMALLINT)''')
        # todo
        db_conn.commit()
        db_conn.close()
