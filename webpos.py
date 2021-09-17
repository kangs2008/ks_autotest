import os, sys
import time
from selenium import webdriver
import cv2


#
# d = webdriver.Chrome()
# d.get('httP://www.baidu.com')
# d.maximize_window()
# # wsize = d.get_window_size()
# # time.sleep(5)
# # print('wsize', wsize)
# # wh = wsize['height']
# # ww = wsize['width']
#
#
#
# def paint_on_screenshot(pos, filename):
#     screenvc = cv2.imread(filename)
#     sx = int(screenvc.shape[1])
#     sy = int(screenvc.shape[0])
#
#     wsize = d.get_window_size()
#     print('wsize', wsize)
#     wh = wsize['height']
#     ww = wsize['width']
#
#     ratex = sx / ww
#     ratey = sy / wh
#
#     pos = (int(int(pos[0]) * ratex), int(int(pos[1]) * ratey))
#     img_res = cv2.circle(screenvc, pos, 15, (0, 0, 225), 3)
#     cv2.imwrite(filename, img_res)
#
# def element_pos(pos, filename):
#     lo = d.find_element_by_id('su').location
#     print(lo)
#     lx = lo['x']
#     ly = lo['y']
#
#     input = d.find_element_by_id('su').size
#     print(input)
#     h = input['height']
#     hw = input['width']
#
#     p_x = int(int(h) / 2)
#     p_y = int(int(hw) / 2)
#
#
#     pos_xx = int(lx) + p_y
#     pos_yy = int(ly) + p_x
#
#     # pos_xx = int(lx)
#     # pos_yy = int(ly)
#
#
#     print(pos_xx, pos_yy)
#     time.sleep(1)
#     f = r'D:\desk20201127\a.png'
#     d.save_screenshot(f)
#
#     paint_on_screenshot((pos_xx, pos_yy + 35), f)
#
#
#     d.find_element_by_id('su')
#




def timeit(func):

    def run(*argv):
        print(func.__name__)
        if argv:
            ret = func(*argv)
            print('ret1')
            print(ret)
        else:
            ret = func()
            print('ret2')
            print(ret)
        return ret
    return run

@timeit
def t(a=''):
    print(a)

#####################################################

import inspect

def get_current_function_name():

    return inspect.stack()[1][3]

class MyClass:

    def function_one(self):
        # print("%s.%s invoked"%(self.__class__.__name__, get_current_function_name()))
        # return self.__class__.__name__ + '.' + get_current_function_name()
        return self.__class__.__name__ + '.' + get_current_function_name()

import time

class TimeRecorder:
    # def __init__(self, name):
    #     print(name + u"开始")
    #     self.name = name
    #     self.startTime = time.time()
    # def __del__(self):
    #     print(u"{0}结束，耗时：{1}".format(self.name, time.time() - self.startTime))
    def aaa(self):
        print(u"{0}结束，耗时：{1}".format(self.name, time.time() - self.startTime))

from functools import wraps
def decorator2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # t = func.__name__
        t = TimeRecorder(func.__name__)
        print(t)
        return func(*args, **kwargs)
    return wrapper

@decorator2
def scan3():
    """扫描APK的权限。。。。"""
    time.sleep(1)
    return 3


if __name__ == '__main__':
    print(scan3())

    # t()
    # myclass = MyClass()
    # print(myclass.function_one())

    pass
