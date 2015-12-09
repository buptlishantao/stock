import sys
import glob
import util

class BackProbe(object):
    """docstring for BackProbe"""
    def __init__(self):
        super(BackProbe, self).__init__()
        self.buy_info = {}
        self.sale_info = {}

    def buy(self,i, stock_info):
        ma5 = stock_info[i][1]["ma5"]
        ma10 = stock_info[i][1]["ma10"]
        ma5_yes = stock_info[i+1][1]["ma5"]
        ma10_yes = stock_info[i+1][1]["ma10"]

        if ma5 > ma10 and ma5_yes < ma10_yes:
            res = True
            self.buy_info["price"] = stock_info[i-1][1]["open"]
            self.buy_info["time"] = stock_info[i-1][0]
        else:
            res = False

        return True
    
    def sale(self,i,stock_info):
        ma5 = stock_info[i][1]["ma5"]
        ma10 = stock_info[i][1]["ma10"]
        ma5_yes = stock_info[i+1][1]["ma5"]
        ma10_yes = stock_info[i+1][1]["ma10"]

        if ma5 < ma10 and ma5_yes > ma10_yes:
            res = True
            self.sale_info["price"] = stock_info[i][1]["close"]
            self.sale_info["time"] = stock_info[i][0]
        else:
            res = False



    def get_stock_id(self):
        return glob.glob("./data/calculate/*")

    def print_buy_sale_trail(self):

        self.buy_info.clear()
        self.sale_info.clear()

    def run(self):
        stock_list = self.get_stock_id()
        #print stock_list
        for filepath in stock_list:
            stockid = filepath.split("/")[-1][:-4]
            stock_info = util.read_basic_info(filepath)
            stock_info =  stock_info[::-1]
            for i, info in enumerate(stock_info):
                ifbuy = self.buy(i, stock_info)
                if ifbuy:
                    self.sale(i,stock_info)

            self.print_buy_sale_trail()


if __name__ == '__main__':
    bp = BackProbe()
    bp.run()
