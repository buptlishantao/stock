import sys
import glob
import util

class BackProbe(object):
    """docstring for BackProbe"""
    def __init__(self):
        super(BackProbe, self).__init__()
        self.buy_sale = []

    def buy(self,i, stock_info):
        pass
    
    def sale(self,i,stock_info):
        pass

    def get_stock_id(self):
        return glob.glob("./data/calculate/*")

    def print_buy_sale_trail(self):
        pass

    def run(self):
        stock_list = self.get_stock_id()
        print stock_list
        for filepath in stock_list:
            stockid = filepath.split("/")[-1][:-4]
            stock_info = util.read_basic_info(filepath)
            for i, info in enumerate(stock_info):
                ifbuy = self.buy(i, stock_info)
                if ifbuy:
                    self.sale(i,stock_info)

                

            self.print_buy_sale_trail()



if __name__ == '__main__':
    bp = BackProbe()
    bp.run()
