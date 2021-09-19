import allure
import sys, inspect
from Locators.baidu_locators import locs
from Common.basepage import BasePage
from Common.utils import mTime
from functools import wraps
page = 'baidu_page'


class BaiduPage(BasePage):

    # 登录
    def return_value(self, value):
        with allure.step(f"返回值是：[{value}]"):
            pass




    # 登录
    @allure.step("登录Method")
    def search(self, text):
        func = self.__class__.__name__ + '.' + sys._getframe().f_code.co_name
        with allure.step(f"[{mTime()}][{func}]"):
            pass
        self.text_input(text, 1)
        self.search_btn()

    def text_input(self, text, pic=''):
        loc_name = 'search_text_loc'
        loc, loc_info = locs(page, loc_name)
        func = self.__class__.__name__ + '.' + sys._getframe().f_code.co_name
        self.input_text(loc_name, loc, loc_info, func, pic, text)

    def search_btn(self, pic=''):
        loc_name = 'search_btn_loc'
        func = self.__class__.__name__ + '.' + sys._getframe().f_code.co_name
        loc, loc_info = locs(page, loc_name)
        self.click_ele(loc_name, loc, loc_info, func, pic)
        # with allure.step(f"[{mTime()}][{func}][{loc_name + '|' + loc_info}]{loc}"):
        #     self.click_ele(loc, loc_name + '|' + loc_info, loc_name, f'{func}')

    def get_news_text(self, pic=''):
        loc_name = 'news_link_loc'
        loc, loc_info = locs(page, loc_name)
        func = self.__class__.__name__ + '.' + sys._getframe().f_code.co_name
        value = self.get_ele_text(loc_name, loc, loc_info, func, pic)
        return value
        # with allure.step(f"[{mTime()}][{func}][{loc_name + '|' + loc_info}]{loc}"):
        #     value = self.get_ele_text(loc, loc_name + '|' + loc_info, loc_name, f'{func}')
        #     self.return_value(value)
        #     return value

    # def get_user_errMsg(self):
    #     m = sys._getframe().f_code.co_name
    #     locs = loc('login_page', 'user_msg_loc')
    #     with allure.step(f"[{mTime()}][{m}][{locs[-1]}]{locs[:-1]}"):
    #         value = self.get_ele_text(locs[:-1], m)
    #         # allure.attach(f'返回值:[{value}]')
    #         print('这里是返回值显示')
    #         # allure.attach(f'返回值:[{value}]')
    #         self.return_value(value)
    #
    #         return value
    #
    # page = 'login_page'
    #
    # def input_pwd(self, pwd):
    #     m = sys._getframe().f_code.co_name
    #     locs = loc('login_page', 'password_loc')
    #     with allure.step(f"[{mTime()}][{m}][{locs[-1]}][{pwd}]{locs[:-1]}"):
    #         self.input_text(locs[:-1], pwd, m)
    #
    # def get_pwd_errMsg(self):
    #     m = sys._getframe().f_code.co_name
    #     locs = loc('login_page', 'pwd_msg_loc')
    #     with allure.step(f"[{mTime()}][{m}][{locs[-1]}]{locs[:-1]}"):
    #         value = self.get_ele_text(locs[:-1], m)
    #         # allure.attach(f'返回值:[{value}]')
    #         self.return_value(value)
    #         return value
    #
    # def login_btn(self):
    #     m = sys._getframe().f_code.co_name
    #     locs = loc('login_page', 'login_btn_loc')
    #     with allure.step(f"[{mTime()}][{m}][{locs[-1]}]{locs[:-1]}"):
    #         self.click_ele(locs[:-1], m)
