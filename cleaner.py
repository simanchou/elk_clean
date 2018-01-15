#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time       : 2018/1/12 16:38
# @Author     : 周星星 Siman Chou
# @Site       : https://github.com/simanchou
# @File       : cleaner.py
# @Description: 
import requests
import time
import datetime


class ELKCleaner():

    def __init__(self, server, interval):
        self.server = server
        self.interval = interval

    def getDataList(self):
        elkDataList = requests.get("http://{}/_cat/indices/?v".format(self.server)).content.decode("utf-8")
        return elkDataList

    def getOldData(self):
        fileNames = []
        for i in self.getDataList().splitlines():
            if len(i) > 0:
                if "filebeat-" in i:
                    #print(i)
                    fileName = i.split()[2]
                    fileDate = fileName.split("-")[1]
                    d1 = datetime.datetime.strptime(time.strftime("%Y.%m.%d"), "%Y.%m.%d")
                    d2 = datetime.datetime.strptime(fileDate, "%Y.%m.%d")
                    #print((d1 - d2).days)
                    if (d1 - d2).days > self.interval:
                        fileNames.append(fileName)
        return fileNames

if __name__ == "__main__":
    elkServer = "10.200.44.31:9200"
    interval = 15
    ec = ELKCleaner(elkServer, interval)
    for oldFile in ec.getOldData():
        requests.delete("http://{}/{}".format(elkServer, oldFile))
        print("{} delete successful.".format(oldFile))
