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
        #print self.stockid,self.current_day
        for i,item in enumerate(stock_advance_info):
            if item[0] > self.current_day:
                self.get_ma(i,stock_advance_info)
                self.get_vol_increase(i, stock_advance_info)
                self.get_close_increase(i, stock_advance_info)

    def calculate_feature_info(self,stock_advance_info):
        for i,item in enumerate(stock_advance_info):
            if item[0] > self.current_day:
                self.get_if_yangxian(i,stock_advance_info)
                self.get_zhengli(i,stock_advance_info)
                self.get_junxiannianlian(i,stock_advance_info)
                self.get_if_fangliang(i,stock_advance_info)

    def get_stock_id(self):
        return glob.glob("./data/info/*")



    def if_can_buy(self,stock_advance_info):
        for i,item in enumerate(stock_advance_info):
            if stock_advance_info[i][1]["if_yangxian"]=="True" \
               and stock_advance_info[i][1]["shiti_bili"] > 0.7 \
               and stock_advance_info[i][1]["zhengli"] < 0.03 \
               and stock_advance_info[i][1]["vol_inc_1"] > 30 \
               and stock_advance_info[i][1]["jxnl"] == "True" \
               and stock_advance_info[i][1]["if_fangliang"] == "True":

               print "buy next","\t".join([stock_advance_info[i][0],self.stockid])

                

    def if_can_sale(self):
        pass


    def run(self):
        stock_list = self.get_stock_id()
        for filepath in stock_list:
            self.outcolums = COLUMS
            self.stockid = filepath.split("/")[-1][:-4]
            stock_basic_info = self.read_basic_info(filepath)
            stock_advance_info = self.merge_advance_info(stock_basic_info)
            self.calculate_advance_info(stock_advance_info)
            self.calculate_feature_info(stock_advance_info)
            self.write_all_data(stock_advance_info)

            self.if_can_buy(stock_advance_info)
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


    def get_if_fangliang(self,i,stock_advance_info):

        key = "if_fangliang"
        if key not in set(self.outcolums):
            self.outcolums.append(key)

        span = 10
        if i + span >= len(stock_advance_info):
            stock_advance_info[i][1][key] = "Nan"
            return

        volume_list = []
        for j in range(i,i+span):
            volume_list.append(float(stock_advance_info[j][1]["volume"]))
            
        if (max(volume_list) == float(stock_advance_info[i][1]["volume"])):
            stock_advance_info[i][1][key] = "True"
        else:
            stock_advance_info[i][1][key] = "False"

        

    def get_zhengli(self, i, stock_advance_info):
        
        key = "zhengli"
        if key not in set(self.outcolums):
            self.outcolums.append(key)
        
        if i + 20 >= len(stock_advance_info):
            stock_advance_info[i][1][key] = "Nan"
            return
        
        close = float(stock_advance_info[i][1]["close"])
        open = float(stock_advance_info[i][1]["open"])
        high = float(stock_advance_info[i][1]["high"])
        low = float(stock_advance_info[i][1]["low"])
        #print stock_advance_info[i+1][0]
        #print stock_advance_info[i+1][1].keys()
        
        yesteday_ma20 = float(stock_advance_info[i+1][1]["ma20"])


        change = (open - yesteday_ma20) / yesteday_ma20
        stock_advance_info[i][1][key] = float(change)


    def get_junxiannianlian(self, i, stock_advance_info):

        key = "jxnl"
        if key not in set(self.outcolums):
            self.outcolums.append(key)

        ma5 = float(stock_advance_info[i][1]["ma5"])
        ma10 = float(stock_advance_info[i][1]["ma10"])
        ma20 = float(stock_advance_info[i][1]["ma20"])
            
        if abs(ma10 - ma5)/ ma5 > 0.05 :
            stock_advance_info[i][1][key] = "False"
        if abs(ma10 - ma20)/ ma10 > 0.05:
            stock_advance_info[i][1][key] = "False"

        stock_advance_info[i][1][key] = "True"


    def get_if_yangxian(self, i, stock_advance_info):
        key1 = "if_yangxian"
        key2 = "shiti_bili"
        if key1 not in set(self.outcolums):
            self.outcolums.append(key1)
        if key2 not in set(self.outcolums):
            self.outcolums.append(key2)
        
        
        close = float(stock_advance_info[i][1]["close"])
        _open = float(stock_advance_info[i][1]["open"])
        high = float(stock_advance_info[i][1]["high"])
        low = float(stock_advance_info[i][1]["low"])

        if close > _open:
            stock_advance_info[i][1][key1] = "True"
        else:
            stock_advance_info[i][1][key1] = "False"

        stock_advance_info[i][1][key2] = (close - _open ) / (high - low + 0.0000001)



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


