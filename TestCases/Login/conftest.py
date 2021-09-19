import pytest
import os
import sys
from time import sleep
from selenium import webdriver
# from Datas.global_datas import base_usl
from Pages import BaiduPage
from Common.basepage import BasePage
from Common.handle_logger import logger

driver = None

# @pytest.fixture(scope='class')
# def start_module(project_module_start):
#     '''
#     每个模块单独打开一次浏览器，此时 driver.quit() 需要单独加上
#     :param project_module_start:  每个模块单独打开一次浏览器
#     :return: driver lg
#     '''
#     logger.info("==========开始执行测试用例集===========")
#     global driver
#     driver = project_module_start
#     driver.get('http://120.78.128.25:8765/Index/login.html')
#     lg = BaiduPage(driver)
#     yield (driver, lg)
#     yield driver
#     logger.info("==========结束执行测试用例集===========")
#     # driver.quit()


@pytest.fixture(scope='class', autouse=False)
def start_session():
    """
    所有CLASS只打开一次浏览器
    :return: driver
    """
    logger.info("========== open browser ===========")
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.baidu.com/')
    yield driver
    driver.quit()
    logger.info("========== close browser ===========")


# @pytest.fixture()
# def refresh_page():
#     yield
#     driver.refresh()
#     sleep(3)
