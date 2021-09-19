import datetime
import time


def mTime():
    return str(datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3])


def formatTime():
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
