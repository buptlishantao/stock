import sys
import util
import glob
import buyandsale


def get_if_fangliang(i,stock_advance_info):

    key = "if_fangliang"
    span = 10
    if i - span < 0:
        stock_advance_info[i][1][key] = "Nan"
        return

    if_vol_inc_1 = (float(stock_advance_info[i][1]["vol_inc_1"]) > 40)
    if not if_vol_inc_1:
        stock_advance_info[i][1][key] = "False"
        return

    volume_list = []
    for j in range(i-span,i,):
        volume_list.append(float(stock_advance_info[j][1]["volume"]))
    
    today_volum = float(stock_advance_info[i][1]["volume"])
    mean_volum = float(sum(volume_list))/len(volume_list)
    
    if ( today_volum - mean_volum) / mean_volum > 0.4:
        stock_advance_info[i][1][key] = "True"
    else:
        stock_advance_info[i][1][key] = "False"

def get_zhengli(i, stock_advance_info):
    
    key = "zhengli"
    if i - 20 >= 0:
        stock_advance_info[i][1][key] = "Nan"
        return
    
    close = float(stock_advance_info[i][1]["close"])
    open = float(stock_advance_info[i][1]["open"])
    high = float(stock_advance_info[i][1]["high"])
    low = float(stock_advance_info[i][1]["low"])
    
    yesteday_ma20 = float(stock_advance_info[i-1][1]["ma20"])

    change = (open - yesteday_ma20) / yesteday_ma20
    stock_advance_info[i][1][key] = float(change)


def get_junxiannianlian(i, stock_advance_info):

    key = "jxnl"
    ma5 = float(stock_advance_info[i][1]["ma5"])
    ma10 = float(stock_advance_info[i][1]["ma10"])
    ma20 = float(stock_advance_info[i][1]["ma20"])

    if abs(ma10 - ma5)/ ma5 > 0.05 :
        stock_advance_info[i][1][key] = "False"
    if abs(ma10 - ma20)/ ma10 > 0.05:
        stock_advance_info[i][1][key] = "False"

    stock_advance_info[i][1][key] = "True"


def get_if_yangxian( i, stock_advance_info):
    key1 = "if_yangxian"
    key2 = "shiti_bili"
        
    close = float(stock_advance_info[i][1]["close"])
    _open = float(stock_advance_info[i][1]["open"])
    high = float(stock_advance_info[i][1]["high"])
    low = float(stock_advance_info[i][1]["low"])

    if close > _open:
        stock_advance_info[i][1][key1] = "True"
    else:
        stock_advance_info[i][1][key1] = "False"

    stock_advance_info[i][1][key2] = (close - _open ) / (high - low + 0.0000001)




class BreakThrough(buyandsale.BackProbe):
    """docstring for BreakThrough"""
    def __init__(self):
        super(BreakThrough, self).__init__()
        self.stockid  = ""
        self.start_day = "2015-01-01"
        self.end_day = "2015-12-32"
        self.action_info = []
        self.start_money = float(10000)
        
        self.buy_already = 0
        self.buy_method = "Today_Close"
        self.sale_method = "Today_Close"


    def calculate_advance_info(self, i, stock_info):
        get_if_fangliang(i, stock_info)
        get_zhengli(i, stock_info)
        get_junxiannianlian(i, stock_info)
        get_if_yangxian(i, stock_info)

    def sale(self,i,stock_info):

        high_list = []

        for j in range(self.buy_poi,i):
            high_list.append(float(stock_info[j][1]["high"]))

        high_price_days = max(high_list)
        
        p = (float(stock_info[i][1]["low"]) )/high_price_days
        
        zhisun = 0.85
        if p < zhisun:
            self.sale_day  = stock_info[i][0]
            self.sale_price = float(high_price_days * zhisun)
            return True
        else:
            return False


    def buy(self, i ,stock_info):
        if_yangxian = (stock_info[i][1]["if_yangxian"]=="True")
        if_shiti = (stock_info[i][1]["shiti_bili"] > 0.7)
        if_zhengli = stock_info[i][1]["zhengli"] < 0.03 
        if_jxnl = stock_info[i][1]["jxnl"] == "True" 
        if_fangliang = stock_info[i][1]["if_fangliang"] == "True"

        if_duotou = stock_info[i][1]["ma5"] >= stock_info[i][1]["ma10"]

        #print if_yangxian,if_shiti,if_zhengli,if_vol_inc_1,if_jxnl,if_fangliang
        if if_yangxian and if_shiti and if_jxnl \
            and if_fangliang:

            #print self.stockid,"buy at %s close with price %s" % (stock_info[i][0],stock_info[i][1]["close"])

            self.buy_day = stock_info[i][0]
            self.buy_price = float(stock_info[i][1]["close"])
            """
            try:
                self.buy_price = float(stock_info[i+1][1]["open"])
            except:
                return False
            """

            return True
        else:
            return False

if __name__ == '__main__':
    bt = BreakThrough()
    bt.run()
