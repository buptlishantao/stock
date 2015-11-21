import sys
import time
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


if __name__ == '__main__':
    #print get_today_str()
    print get_date_from("2015-11-11",1)


