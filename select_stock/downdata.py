import sys
sys.path.append("..")

import tushare as ts
import util
import pandas as pd
import logging
import os

class DownloadData(object):
    """docstring for DownloadData"""
    def __init__(self):
        self.today = util.get_today_str()
        #self.begin_day = util.get_begin_day_str()

    def get_stocks_id(self):
        sd = pd.read_csv("data/stocks_id.csv")
        stock_id_list = []
        for code in list(sd["code"]):
            stock_id_list.append(util.transid(code))

        return stock_id_list


    def _get_stock_info_save(self, sid, begin_day, stock_info):
        logging.error(begin_day+"\t" + sid)
        if begin_day == self.today:
            return
        sinfo = ts.get_h_data(sid,start = begin_day, end=self.today)
        if sinfo is None:
            return
        if stock_info is None:
            sinfo.to_csv("data/info/%s" %(sid))
        else:
            sinfo.to_csv("tmp")
            sinfo = pd.read_csv("tmp")
            os.remove("tmp")
            #merge stock_info and sinfo
            sinfo = pd.concat([sinfo,stock_info])
            #print sinfo
            #print stock_info
            sinfo.to_csv("data/info/%s" %(sid),index = False)
        



    def _get_history_data(self, sid):
        begin_day = "2011-01-01"
        try:
            stock_info = pd.read_csv("data/info/%s" %  (sid))
        except IOError as e:
            logging.error(e)
            return begin_day, None

        begin_day = util.get_date_from(list(stock_info["date"])[0],1)
        return begin_day, stock_info


    def _merge_to_history(self, sid):
        begin_day,  stock_info = self._get_history_data(sid)
        self._get_stock_info_save(sid, begin_day, stock_info)


    def download(self):
        stocks_id = self.get_stocks_id()
        i = 1
        for sid in stocks_id:
            logging.info("downloading code %s" % (sid)) 
            self._merge_to_history(sid)            
            if i >1000:
                break
            i = i+1



if __name__ == '__main__':
    DL = DownloadData()
    DL.download()
