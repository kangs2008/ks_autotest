import datetime
import time
from Common.setting import BASE_DIR
from functools import wraps
from Common.handle_logger import logger as case_logger
import allure

def basePath(*args):
    return BASE_DIR

def mTime(*args):
    return str(datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3])
def mDate(*args):
    return str(datetime.datetime.now().strftime('%Y%m%d'))

def mDate2(*args):
    aa = tuple(*args)[0]
    bb = tuple(*args)[1]
    return str(datetime.datetime.now().strftime('%Y%m%d'))

def mDateTime(*args):
    return str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))

def formatTime(*args):
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())


def timeStamp(timeNum):
    timeStamp = float(timeNum / 1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def use_time(starttime, endtime):
    # starttime = time.time()
    # endtime = time.time()
    m, s = divmod(int(endtime - starttime), 60)
    h, m = divmod(m, 60)
    return "Usage time %d:%02d:%02d" % (h, m, s)


def start_time_format(starttime):
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(starttime))  # time.localtime(time.time())


def report_date_folder():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))


def usageTime(endtime, starttime):
    return str(starttime.strftime('%Y%m%d %H:%M:%S.%f'))[:-3] + '/' + str((endtime - starttime))[5:11]
    # return starttime.strftime('%H:%M:%S.%f')




if __name__ == '__main__':
    pass
    # a = datetime.datetime.now()
    # time.sleep(2.1)
    # b = datetime.datetime.now()
    # print(usageTime(b, a))

    # print(report_date_folder())
    # print(mTime())
    # print(start_time_format(time.time()))
