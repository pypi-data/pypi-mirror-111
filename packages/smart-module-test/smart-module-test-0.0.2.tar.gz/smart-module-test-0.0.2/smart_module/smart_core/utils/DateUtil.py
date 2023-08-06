# -*- coding: UTF-8 -*-
import datetime
import time


class DateUtil:

    def __init__(self):
        self.begin = 0
        self.allCostTime = 0

    def getDateStr(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def getTime(self):
        return time.time()

    def start(self):
        self.begin = time.time();

    def getAndStart(self):
        currCost = time.time() - self.begin;
        self.begin = time.time();
        self.allCostTime = self.allCostTime + currCost;
        return currCost

    def getCostAndClear(self):
        allCostTime = self.allCostTime;
        self.allCostTime = 0;
        return allCostTime

    def deltaStr(self,delta):
        deltaObj = datetime.timedelta(seconds=delta)
        return str(deltaObj)



# dateUtil = DateUtil()
#
# print(dateUtil.getTime())