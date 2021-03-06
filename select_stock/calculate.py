#!coding-utf-8
import os
import sys
import glob
import logging


COLUMS = ["date","open","high","close","low","volume","amount"]

class CalMoreInfo(object):
    """docstring for CalMoreInfo
    """
    
    def __init__(self):
        self.stockid = ""
        self.current_day = ""
        self.outcolums = ""

    def calculate_advance_info(self, stock_advance_info):
        for i,item in enumerate(stock_advance_info):
            if item[0] > self.current_day:
                self.get_ma(i,stock_advance_info)
                self.get_vol_increase(i, stock_advance_info)
                self.get_close_increase(i, stock_advance_info)
                self.cal_can_buy(i,stock_advance_info)
                self.cal_can_sale(i,stock_advance_info)

    def calculate_feature_info(self,stock_advance_info):
        for i,item in enumerate(stock_advance_info):
            if item[0] > self.current_day:
                self.get_if_yangxian(i,stock_advance_info)
                self.get_zhengli(i,stock_advance_info)
                self.get_junxiannianlian(i,stock_advance_info)
                self.get_if_fangliang(i,stock_advance_info)

    def get_stock_id(self):
        return glob.glob("./data/info/*")


    def run(self):
        stock_list = self.get_stock_id()
        for filepath in stock_list:
            self.outcolums = COLUMS
            self.stockid = filepath.split("/")[-1][:-4]
            stock_basic_info = self.read_basic_info(filepath)
            stock_advance_info = self.merge_advance_info(stock_basic_info)
            self.calculate_advance_info(stock_advance_info)
            self.write_all_data(stock_advance_info)

            #self.if_can_buy(stock_advance_info)
            #break


    def read_basic_info(self, filepath):
        stock_basic_info = []
        f = open(filepath)
        colums = f.next().strip().split(",")
        for line in f:
            items = line.strip().split(",")
            date = items[0]
            info = dict(zip(colums,items))
            stock_basic_info.append((date, info))

        return stock_basic_info


    def merge_advance_info(self, stock_basic_info):
        stock_advance_info = []

        try:
            f = open("./data/calculate/%s.csv" % (self.stockid))
            colums = f.next().strip().split(",")
            #print colums
            for line in f:
                items = line.strip().split(",")
                date = items[0]
                info = dict(zip(colums,items))
                stock_advance_info.append((date,info))
        except IOError as e:
            logging.error(e)
        try:
            advance_current_day = stock_advance_info[0][0]
        except:
            advance_current_day = "2000-00-00"

        self.current_day = advance_current_day
        
        tmp = []
        for item in stock_basic_info:
            if item[0] > advance_current_day:
                tmp.append(item)

        tmp.extend(stock_advance_info)
        stock_advance_info = tmp

        return stock_advance_info



    def get_close_increase(self, i, stock_advance_info):
        mlist = [1,2,3,4,5,10,15,20,30,60,100,200,300]
        for span in mlist:
            key = "close_inc" + str(span)
            if key not in set(self.outcolums):
                self.outcolums.append(key)
            
            if i + span >= len(stock_advance_info):
                stock_advance_info[i][1][key] = "Nan"
                continue
            
            j = i + span
            x = float(stock_advance_info[i][1]["close"])
            y = float(stock_advance_info[j][1]["close"])

            stock_advance_info[i][1][key] =  round((x-y)*100/y,2)


    def get_ma(self, i, stock_advance_info):
        mlist = [5,10,15,20,30,60,100,200,300]
        for span in mlist:
            key = "ma" + str(span)
            if key not in set(self.outcolums):
                self.outcolums.append(key)
            if i + span > len(stock_advance_info):
                stock_advance_info[i][1][key] = "Nan"
                continue

            sum_p = 0.0
            for j in range(i,i+span):
                sum_p += float(stock_advance_info[j][1]["close"])
            #print stock_advance_info[i][0]
            stock_advance_info[i][1][key] = sum_p/ span


    def get_vol_increase(self, i, stock_advance_info):
        mlist = [1,2,3]
        for span in mlist:
            key = "vol_inc_" + str(span)
            if key not in set(self.outcolums):
                self.outcolums.append(key)
            if i + span >= len(stock_advance_info):
                stock_advance_info[i][1][key] = "Nan"
                continue

            j = i + span

            x = float(stock_advance_info[i][1]["volume"])
            y = float(stock_advance_info[j][1]["volume"])

            stock_advance_info[i][1][key] =  round((x-y)*100/y,2)

    def cal_can_buy(self,i,stock_advance_info):
        key = "can_buy"
        if key not in set(self.outcolums):
            self.outcolums.append(key)
        if stock_advance_info[i][1]["low"] == stock_advance_info[i][1]["high"] and \
           stock_advance_info[i][1]["high"] == stock_advance_info[i][1]["close"]:
            stock_advance_info[i][1][key] = 0
        else:
            stock_advance_info[i][1][key] = 1
     
    def cal_can_sale(self,i,stock_advance_info):
        key = "can_sale"
        if key not in set(self.outcolums):
            self.outcolums.append(key)
        if stock_advance_info[i][1]["low"] == stock_advance_info[i][1]["high"] and \
           stock_advance_info[i][1]["low"] == stock_advance_info[i][1]["close"]:
            stock_advance_info[i][1][key] = 0
        else:
            stock_advance_info[i][1][key] = 1

    def write_all_data(self,stock_advance_info):
        f = open("./data/calculate/%s.csv" % (self.stockid), "w")
        #print ",".join(self.outcolums)
        f.write(",".join(self.outcolums)+"\n")
        for x in stock_advance_info:
            printlist = []
            for key in self.outcolums:
                printlist.append(str(x[1][key]))
            f.write( ",".join(printlist) +"\n")


if __name__ == '__main__':
    cm = CalMoreInfo()
    cm.run()
    #x = cm.read_basic_info()
    #y = cm.read_advance_info(x)
    #print y
    #print y["600051"]


