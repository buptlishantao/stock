import sys
import glob
import util


action_sum = {
"correct" : 0,
"error" : 0,
"even" : 0
}


today_buy = {}
buy_action_everday = {}
sale_action_everyday = {}

class BuySaleAction(object):
    """docstring for BuySaleAction"""
    def __init__(self, buy_price,buy_day,sale_price,sale_day,stockid):
        super(BuySaleAction, self).__init__()
        self.buy_price = float(buy_price)
        self.buy_day = buy_day
        self.sale_price = float(sale_price)
        self.sale_day = sale_day
        self.stockid = stockid
        self.profit = self.get_profit()

    def get_profit(self):
        return float(self.sale_price / self.buy_price) - 1
        
class BackProbe(object):
    """docstring for BackProbe"""
    def __init__(self):
        super(BackProbe, self).__init__()
        self.stockid  = ""
        self.start_day = "2015-01-01"
        self.end_day = "2015-12-01"
        self.action_info = []
        self.start_money = float(10000)
        
        self.buy_already = 0
        self.buy_method = "Today_Close"
        self.sale_method = "Today_Close"
        
        self.buy_price  = 0
        self.sale_price = 0


    def buy(self,i, stock_info):

        ma5 = float(stock_info[i][1]["ma5"])
        ma10 = float(stock_info[i][1]["ma10"])
        ma5_yes = float(stock_info[i-1][1]["ma5"])
        ma10_yes = float(stock_info[i-1][1]["ma10"])

        if ma5 > ma10 and ma5_yes < ma10_yes:
            self.buy_day = stock_info[i][0]
            self.buy_price = float(stock_info[i][1]["close"])
            return True
        else:
            return False

            
    def sale(self,i,stock_info):

        ma5 = float(stock_info[i][1]["ma5"])
        ma10 = float(stock_info[i][1]["ma10"])
        ma5_yes = float(stock_info[i-1][1]["ma5"])
        ma10_yes = float(stock_info[i-1][1]["ma10"])

        if ma5 < ma10 and ma5_yes > ma10_yes:
            self.sale_day  = stock_info[i][0]
            self.sale_price = float(stock_info[i][1]["close"])
            return True
        else:
            return False
            

    def get_stock_id(self):
        return glob.glob("./data/calculate/*")

    def print_buy_sale_trail(self):

        end_money = self.start_money
        print self.stockid
        for action in self.action_info:
            print "buy at %s with price %s, sale at %s with price %s, profit: %s%%" % \
                    (action.buy_day,action.buy_price, \
                        action.sale_day,action.sale_price, \
                        100*action.get_profit())

            if action.get_profit()>0:
                action_sum["correct"] += 1
            elif action.get_profit()<0:
                action_sum["error"] += 1
            else:
                action_sum["even"] += 1

            end_money *= (action.get_profit()+1)
        

        print self.stockid,"end_money",end_money
        print
        print
        self.action_info = []
        self.buy_already = 0

        return end_money

    def calculate_advance_info(self, i, stock_info):
        pass

    def parser_every_day(self, buy_action_everday):
        day_action = {}
        for action_info in  buy_action_everday.values():
            for action in action_info:
                day_action.setdefault(action.buy_day,[])
                day_action[action.buy_day].append(action)
                #print action.stockid,action.buy_day,action.sale_day,action.profit

        for k in sorted(day_action.keys()):
            for action in day_action[k]:
                print k, action.stockid,action.buy_day,action.sale_day,action.profit
            print
            print

    def run(self):
        stock_list = self.get_stock_id()
        #print stock_list
        begin_money_list = []
        end_money_list = []
        base_money_list = [] 

        
        for filepath in stock_list:
            base_buy = -1
            base_sale = -1
            stockid = filepath.split("/")[-1][:-4]
            self.stockid = stockid

            """
            if not self.stockid.startswith("300"):
                continue
            """
            """
            if not self.stockid.startswith("600315"):
                continue
            """

            stock_info = util.read_basic_info(filepath)[::-1]
            buy_flag  = False
            for i, info in enumerate(stock_info):
                self.calculate_advance_info(i, stock_info)
                if stock_info[i][0] < self.start_day:
                    continue
                if stock_info[i][0] > self.end_day:
                    continue

                if base_buy == -1:
                    base_buy = float(stock_info[i][1]["close"])
                
                base_sale = float(stock_info[i][1]["close"])

                if self.buy_already == 0 and stock_info[i][1]["can_buy"] == "1":
                    buy_res = self.buy(i, stock_info)
                    if buy_res == True:
                        self.buy_poi = i
                        self.buy_already = 1
                        if i == (len(stock_info) -1):
                            print "buy_today:", stock_info[i][0],self.stockid
                        continue

                if self.buy_already == 1:
                    sale_res = self.sale(i,stock_info)
                    if sale_res == True and stock_info[i][1]["can_sale"] == "1":
                        self.buy_already = 0
                        action = BuySaleAction(self.buy_price,self.buy_day,self.sale_price,self.sale_day,self.stockid)
                        self.action_info.append(action)
                        buy_flag = True

                        
            self.buy_already = 0
            if buy_flag:
                begin_money_list.append(self.start_money)
                end_money = self.print_buy_sale_trail()
                end_money_list.append(end_money)

                buy_action_everday[self.stockid] = self.action_info

            base_money_list.append(10000*base_sale/base_buy)
            #break

        begin = sum(begin_money_list)
        end = sum(end_money_list)
        print "%s\t%s\t%6.2f%%" % (begin,end, (float(end)/float(begin) - 1) * 100)
        print action_sum, float(action_sum['correct']) / sum(action_sum.values())

        print "base: %6.2f%%" % (((sum(base_money_list) / (len(base_money_list) * 10000)) -1 ) * 100)
        #self.parser_every_day(buy_action_everday)

if __name__ == '__main__':
    bp = BackProbe()
    bp.run()
