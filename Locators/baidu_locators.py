from Common.handle_logger import logger
from Common.utils import mTime
import sys, allure
XPATH = 'xpath'
ID = 'id'
var = {}


def _get_variables(page):
    if page == 'baidu_page':
        search_text_loc = {'loc': '//*[@id="kw"]', 't': XPATH, 'info': '首页输入框'}
        var['search_text_loc'] = search_text_loc

        search_btn_loc = {'loc': '//*[@id="su"]', 't': XPATH, 'info': '百度一下'}
        var['search_btn_loc'] = search_btn_loc

        news_link_loc = {'loc': '//*[@id="s-top-left"]/a[1]', 't': XPATH, 'info': '新闻'}
        var['news_link_loc'] = news_link_loc

        return var
    elif page == 'home_page':
        pass
        return var

def locs(page, loc_name):
    try:
        locs = _get_variables(page)
        return (locs[loc_name]['t'], locs[loc_name]['loc']), loc_name + '|' + locs[loc_name]['info']
    except Exception as e:
        with allure.step(f"[{mTime()}][{sys._getframe().f_code.co_name}][{page} OR {loc_name}] not define"):
            pass
        logger.info(f"LOCATOR OR PAGE ERROR：[{sys._getframe().f_code.co_name}] method,  [{loc_name}] not define")


if __name__ == '__main__':
    pass
# class LoginLocator:
#     username_loc = (By.XPATH, '//input[@name = "phone"]')
#     password_loc = (By.XPATH, '//input[@name = "password"]')
#     login_btn_loc = (By.XPATH, '//button[@class = "btn btn-special"]')
#     error_msg_loc = (By.XPATH, '//button[@class = "form-error-info"]')
#     user_msg_loc = (By.XPATH, '//*[@class = "login-form"]/form/div[1]/div')
#     pwd_msg_loc = (By.XPATH, '//*[@class = "login-form"]/form/div[2]/div')
