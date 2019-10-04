#coding: utf-8

import csv
import json
import os
import time
import requests


class Consult():
    def __init__(self):
        path=sys.arg[0]
        self.nickname = {}
        self.number = {}
        self.def_lst = []
        nickfile = os.path.join(path, "nickname.csv")
        if not os.path.exists(nickfile):
            print("nickname.csv文件不存在")
        with open(nickfile, encoding="utf-8-sig")as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                for col in row[1:]:
                    self.nickname[col] = row[0]
                self.number[int(row[0])] = row[1]

    def user_input(self, cmd):
        in_list = cmd.split()
        if len(in_list) > 5:
            return "error: more than 5"
        for index in in_list:
            item = self.nickname.get(index.lower(), "error")
            if item == "error":
                return "error: "+index+" not found"
            self.def_lst.append(item)
        return ""

    def jjcsearch(self):
        query = ".".join(self.def_lst)
        data = requests.get("http://api.yobot.xyz/jjc_search?def=" + query)
        print(data.text)
        res = json.loads(data.text)
        text = ""
        if(res["code"] == 0):
            text += "找到{}条记录".format(len(res["data"]["result"]))
            for result in res["data"]["result"]:
                text += "\n"
                for atker in result["atk"]:
                    text += self.number[atker["id"]]
                    if atker["equip"] or atker["star"]:
                        cmt = ""
                        if atker["star"]:
                            cmt += str(atker["star"])+"星"
                        if atker["equip"]:
                            cmt += "专"
                        text += "("+cmt+")"
                    text += " "
                text += "({},{}赞{}踩)；".format(
                    result["updated"]
                    [2:10], result["up"],
                    result["down"])
        else:
            text = "error code: {}\nmessage : {}".format(
                res["code"], res["message"])
        return text


if __name__ == "__main__":
    # cus_list = user_input(["布丁", "kkr", "镜子", "448"], nickname)
    # if isinstance(cus_list, str):
    #     print(cus_list)
    # else:
    #     result = jjcsearch(cus_list, number)
    #     print(result)
    c = Consult(r"E:\tangmt\Documents\工作台\programming\yobot_2")
    r = c.user_input("布丁 水子龙 448 水魅魔")
    if r == "":
        r = c.jjcsearch()
    print(r)
