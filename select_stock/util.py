import os
import sys
import time
import glob
import datetime

def get_today_str():
    today = datetime.date.today()
    return today.strftime("%Y-%m-%d")


def get_begin_day_str():
    return "2012-01-01"


def transid(code):
    return  "0" * (6 - len(str(code))) + str(code)


def get_date_from(c_day, delta_days):
    """ 
    Args:
        c_day:string like 'yyyy-mm-dd'
        delta:int
    Returns:
        date
    """
    year,month,day = c_day.split("-")
    d = datetime.date(int(year), int(month), int(day))
    day_ago = d + datetime.timedelta(delta_days)
    return day_ago.strftime("%Y-%m-%d")


def list_file(path):
    for filename in os.listdir(path):
        print filename

def list_file_path(path):
    filelist = glob.glob(path)
    print filelist
    """
    for f in filelist:
        print f
    """

def read_basic_info(filepath):
    stock_basic_info = []
    f = open(filepath)
    colums = f.next().strip().split(",")
    for line in f:
        items = line.strip().split(",")
        date = items[0]
        info = dict(zip(colums,items))
        stock_basic_info.append((date, info))

    return stock_basic_info

def read_csv(path):
    for filename in os.listdir("./data/info"):
        stock_ids.append(filename)
        f = open("/".join(["./data/info",filename]))
        colums = f.next().strip().split(",")
        stock_basic_info[filename] = []
        for line in f:
            items = line.strip().split(",")
            date = items[0]
            info = dict(zip(colums,items))
            stock_basic_info[filename].append((date, info))

if __name__ == '__main__':
    #print get_today_str()
    #print get_date_from("2015-11-11",1)
    #print list_file("./data/info/")
    print list_file_path("./data/info/")
