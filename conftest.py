# -*- coding: utf-8 -*-
import pytest, os, time, subprocess, sys
import requests
from py._xmlgen import html
from Common.handle_logger import logger
from Common.handle_config import ReadWriteConfFile
from Common.utils import start_time_format, use_time, report_date_folder
from Common.handle_file import file_zip_path, file_del, file_copy, file_and_folder_copy, current_folder_file_copy
from Common.setting import BASE_DIR, REPORT_DIR, REPORT_CURRENT_DIR
from Common.newbasepage import PageObject, Element
from selenium import webdriver
import datetime
_session = None
_date = report_date_folder()
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


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(3, html.th('Time', class_='sortable time', col='time'))
    # cells.insert(1,html.th("Test_nodeid"))
    cells.pop()


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(3, html.td(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), class_='col-time'))
    # cells.insert(1,html.td(report.nodeid))
    cells.pop()













































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
    # driver.quit()
    logger.info("========== close browser ===========")













#
# def pytest_addoption(parser):
#     """add --report"""
#     parser.addoption(
#         "--report",
#         action="store",
#         default=_date,  # 'Report_allure'
#         help="current report directory"
#     )
#
#
# @pytest.fixture(scope="session", autouse=True)
# def report(request):
#     """get command line parameters
#     :param request: --report
#     """
#     starttime = time.time()
#     if str(request.config.getoption("--report")).upper() == 'REPORT_ALLURE':
#         report_dir_format = start_time_format(starttime) + '_allure'
#         set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
#         mk_report_dir = os.path.join(REPORT_CURRENT_DIR, report_dir_format)
#         os.mkdir(mk_report_dir)
#         logger.info(
#             f"custom addopts for the report folder:fixture name[{sys._getframe().f_code.co_name}], param[--report], value[{request.config.getoption('--report')}]")
#         logger.info(f"the report folder:{mk_report_dir}")
#     else:
#         report_dir_format = request.config.getoption("--report") + '_allure'
#         set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
#         mk_report_dir = os.path.join(REPORT_CURRENT_DIR, report_dir_format)
#         if not os.path.exists(mk_report_dir):
#             os.mkdir(mk_report_dir)
#         logger.info(
#             f"custom addopts for the report folder:[{sys._getframe().f_code.co_name}],param[--report],value[{request.config.getoption('--report')}]")
#         logger.info(f"the report folder:{mk_report_dir}")
#     yield request.config.getoption("--report")
#
#     # cmd = 'allure generate ./temp -o ./Report --clean'
#     # os.system(cmd)
#
#     # logger.info(f"os.system :{cmd}")
#     report_dir = ReadWriteConfFile().get_option('report_dir', 'report_dir_folder')
#     copy_to = os.path.join(REPORT_CURRENT_DIR, report_dir)
#     file_del(copy_to)
#     file_and_folder_copy(REPORT_DIR, f'{copy_to}', [], '')
#     logger.info(f"file_and_folder_copy:{copy_to}")
#     set_exec_ini('report_dir', 'report_dir_folder', '')
#
#     endtime = time.time()
#     logger.info(f"------------------------")
#     logger.info(use_time(starttime, endtime))
#     logger.info(f"------------------------")


def set_exec_ini(section, option, value):
    ReadWriteConfFile().add_section(section)
    ReadWriteConfFile().set_option(section, option, value)


@pytest.fixture(scope="function", autouse=False)
def requests_session():
    """
    init requests.session()
    """
    logger.info('*' * 100)
    logger.info('*' * 20 + '测试执行开始' + '*' * 20)
    global _session
    _session = requests.session()
    logger.info(f'----------requests_session setup----------')
    logger.info(f'获取session：{_session}')
    yield _session
    _session.close()
    logger.info(f'销毁session：{_session}')
    logger.info(f'----------requests_session teardown----------')
    logger.info('*' * 20 + '测试执行结束' + '*' * 20)
    logger.info('*' * 100)
