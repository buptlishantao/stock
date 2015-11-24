#!coding-utf-8
import os
import sys
import glob
import logging


class CalMoreInfo(object):
    """docstring for CalMoreInfo
    """
    def __init__(self):
        self.stockid = ""
        self.current_day = ""
        pass

    def calculate_advance_info(self, stock_advance_info):
        print self.stockid
        print self.current_day
        for i,item in enumerate(stock_advance_info):
            if item[0] > self.current_day:
                self.get_ma(i,stock_advance_info)
                self.get_vol_increase(i, stock_advance_info)


    def get_stock_id(self):
        return glob.glob("./data/info/*")


    def run(self):
        stock_list = self.get_stock_id()
        for filepath in stock_list:
            self.stockid = filepath.split("/")[-1]
            stock_basic_info = self.read_basic_info(filepath)
            stock_advance_info = self.merge_advance_info(stock_basic_info)
            self.calculate_advance_info(stock_advance_info)
            self.write_all_data(stock_advance_info)

    def get_advance_day(self):
        pass

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
            f = open("./data/calculate/%s" % (self.stockid))
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

    def get_ma(self, i, stock_advance_info):
        mlist = [5,10,15,20,30,60,100,200,300]
        for span in mlist:
            key = "ma" + str(span)
            if i + span > len(stock_advance_info):
                stock_advance_info[i][1][key] = "Nan"
                continue

            sum_p = 0.0
            for j in range(i,i+span):
                sum_p += float(stock_advance_info[j][1]["close"])
            stock_advance_info[i][1][key] = sum_p/ span


    def get_vol_increase(self, i, stock_advance_info):
        mlist = [1,2,3]
        for span in mlist:
            key = "vol_inc_" + str(span)
            if i + span >= len(stock_advance_info):
                stock_advance_info[i][1][key] = "Nan"
                continue

            j = i + span

            x = float(stock_advance_info[i][1]["volume"])
            y = float(stock_advance_info[j][1]["volume"])

            stock_advance_info[i][1][key] =  round((x-y)*100/y,2)


    def write_all_data(self,stock_advance_info):
        f = open("./data/calculate/%s" % (self.stockid), "w")
        colums = stock_advance_info[-1][1].keys()
        colums.sort()
        colums.remove("date")
        f.write("date,"+",".join(colums) +"\n")

        for x in stock_advance_info:
            printlist = []
            for key in colums:
                printlist.append(str(x[1][key]))
            f.write( x[0]+","+",".join(printlist) +"\n")


if __name__ == '__main__':
    cm = CalMoreInfo()
    cm.run()
    #x = cm.read_basic_info()
    #y = cm.read_advance_info(x)
    #print y
    #print y["600051"]


