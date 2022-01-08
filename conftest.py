# -*- coding: utf-8 -*-
import pytest, os, time, subprocess, sys
from py._xmlgen import html
from Common.handle_logger import logger
from Common.handle_config import ReadWriteConfFile
from Common.utils import report_date_folder
from pathlib import Path
from Common.handle_excel3 import excel_to_case

# _date = report_date_folder()

def pytest_addoption(parser):
    """add --report"""
    parser.addoption("--path", action="store", default='no_set_path', help="current report directory")
    parser.addoption("--name", action="store", default='no_set_path', help="current report directory")
    parser.addoption("--sheet", action="store", default='no_set_path', help="current report directory")
    parser.addoption("--rule", action="store", default='no_set_path', help="current report directory")
    parser.addoption("--conf", action="store", default='no_set_path', help="current report directory")


def _set_exec_ini(section, option, value):
    ReadWriteConfFile().add_section(section)
    ReadWriteConfFile().set_option(section, option, value)










#
# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     """当测试失败的时候，自动截图，展示到html报告中"""
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#
#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             _driver = item.funcargs['start_session']
#             fn = PageObject(_driver).save_capture_ob('ERROR')
#
#             extra.append(pytest_html.extras.image(fn))
#         report.extra = extra
#     report.description = str(item.function.__doc__)
#     report.nodeid = report.nodeid.encode('utf-8').decode('unicode_escape')
#
# @pytest.mark.optionalhook
# def pytest_html_results_summary(prefix, summary, postfix):
#     prefix.extend([html.p("测试人: xqc")])


# def pytest_configure(config):
#     config._metadata['测试地址'] = 'https://www.baidu.com'


# @pytest.mark.optionalhook
# def pytest_html_results_table_header(cells):
#     cells.insert(2, html.th('Description'))
#     cells.insert(3, html.th('Time', class_='sortable time', col='time'))
#     # cells.insert(1,html.th("Test_nodeid"))
#     cells.pop()
#
#
# @pytest.mark.optionalhook
# def pytest_html_results_table_row(report, cells):
#     cells.insert(2, html.td(report.description))
#     cells.insert(3, html.td(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), class_='col-time'))
#     # cells.insert(1,html.td(report.nodeid))
#     cells.pop()












































#
# @pytest.fixture(scope='class', autouse=False)
# def start_session():
#     """
#     所有CLASS只打开一次浏览器
#     :return: driver
#     """
#     logger.info("========== open browser ===========")
#     global driver
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     driver.get('https://www.baidu.com/')
#     yield driver
#     # driver.quit()
#     logger.info("========== close browser ===========")














# @pytest.fixture(scope="function", autouse=False)
# def requests_session():
#     """
#     init requests.session()
#     """
#     logger.info('*' * 100)
#     logger.info('*' * 20 + '测试执行开始' + '*' * 20)
#     global _session
#     _session = requests.session()
#     logger.info(f'----------requests_session setup----------')
#     logger.info(f'获取session：{_session}')
#     yield _session
#     _session.close()
#     logger.info(f'销毁session：{_session}')
#     logger.info(f'----------requests_session teardown----------')
#     logger.info('*' * 20 + '测试执行结束' + '*' * 20)
#     logger.info('*' * 100)
