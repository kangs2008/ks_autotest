# -*- coding: utf-8 -*-
import pytest, os, time, subprocess, sys
import requests
from py._xmlgen import html
from Common.handle_logger import logger
from Common.handle_config import ReadWriteConfFile
from Common.utils import start_time_format, use_time, report_date_folder
from Common.handle_file import file_zip_path, file_del, file_copy, file_and_folder_copy, current_folder_file_copy
from Common.setting import BASE_DIR, REPORT_DIR, REPORT_CURRENT_DIR, DATAS_DIR
from Common.newbasepage import PageObject, Element
from selenium import webdriver
import datetime
from pathlib import Path
from Common.handle_excel3 import excel_to_case

_session = None
_date = report_date_folder()



def pytest_addoption(parser):
    """add --report"""
    parser.addoption("--path", action="store", default='no_set_path', help="current report directory")
    parser.addoption("--name", action="store", default='no_set_path', help="current report directory")
    parser.addoption("--sheet", action="store", default='no_set_path', help="current report directory")
    parser.addoption("--rule", action="store", default='no_set_path', help="current report directory")
    parser.addoption("--conf", action="store", default='no_set_path', help="current report directory")

# @pytest.fixture(scope="function", autouse=False)
# def set_test_data_api(request):
#     """get command line parameters
#     :param request: --report
#     """
#     excel_file_path = ReadWriteConfFile().get_option('test_data', 'excel_file_path')
#     excel_file_name = ReadWriteConfFile().get_option('test_data', 'excel_file_name')
#     sheet_names = ReadWriteConfFile().get_option('test_data', 'sheet_names')
#     sheet_rule = ReadWriteConfFile().get_option('test_data', 'sheet_rule')
#     sheet_kvconfig = ReadWriteConfFile().get_option('test_data', 'sheet_kvconfig')
#
#
#     if str(request.config.getoption("--path")).lower() == 'no_set_path':
#         _set_exec_ini('test_data', 'excel_file_path', '')
#         _set_exec_ini('test_data', 'excel_file_name', '')
#         _set_exec_ini('test_data', 'sheet_names', '')
#         _set_exec_ini('test_data', 'sheet_rule', '')
#         _set_exec_ini('test_data', 'sheet_kvconfig', '')
#     else:
#         _set_exec_ini('test_data', 'excel_file_path', request.config.getoption("--path"))
#         _set_exec_ini('test_data', 'excel_file_name', request.config.getoption("--name"))
#         _set_exec_ini('test_data', 'sheet_names', request.config.getoption("--sheet"))
#         _set_exec_ini('test_data', 'sheet_rule', request.config.getoption("--rule"))
#         _set_exec_ini('test_data', 'sheet_kvconfig', request.config.getoption("--conf"))
#     yield request.config.getoption("--path")


def _set_exec_ini(section, option, value):
    ReadWriteConfFile().add_section(section)
    ReadWriteConfFile().set_option(section, option, value)


def pytest_generate_tests(metafunc):
    # excel_file_path = ReadWriteConfFile().get_option('test_data', 'excel_file_path')
    # excel_file_name = ReadWriteConfFile().get_option('test_data', 'excel_file_name')
    # sheet_names = ReadWriteConfFile().get_option('test_data', 'sheet_names')
    # sheet_rule = ReadWriteConfFile().get_option('test_data', 'sheet_rule')
    # sheet_kvconfig = ReadWriteConfFile().get_option('test_data', 'sheet_kvconfig')


    excel_file_path = metafunc.config.getoption("--path").strip()
    excel_file_name = metafunc.config.getoption("--name").strip()
    sheet_names = metafunc.config.getoption("--sheet").strip()
    sheet_rule = metafunc.config.getoption("--rule").strip()
    sheet_kvconfig = metafunc.config.getoption("--conf").strip()
    if excel_file_path.lower() != 'no_set_path':
        ReadWriteConfFile().set_option('test_data', 'excel_file_path', excel_file_path)
        ReadWriteConfFile().set_option('test_data', 'excel_file_name', excel_file_name)
        # if ',' in sheet_names:
        #      sheet_names = sheet_names.split(',')
        ReadWriteConfFile().set_option('test_data', 'sheet_names', sheet_names)
        ReadWriteConfFile().set_option('test_data', 'sheet_rule', sheet_rule)
        # if ',' in sheet_kvconfig:
        #     sheet_kvconfig = sheet_kvconfig.split(',')
        ReadWriteConfFile().set_option('test_data', 'sheet_kvconfig', sheet_kvconfig)
    # else:
    #     ReadWriteConfFile().set_option('test_data', 'excel_file_path', excel_file_path)
    #     ReadWriteConfFile().set_option('test_data', 'excel_file_name', excel_file_name)
    #     ReadWriteConfFile().set_option('test_data', 'sheet_names', sheet_names)
    #     ReadWriteConfFile().set_option('test_data', 'sheet_rule', sheet_rule)
    #     ReadWriteConfFile().set_option('test_data', 'sheet_kvconfig', sheet_kvconfig)
        # if ',' in sheet_names:
        #      sheet_names = sheet_names.split(',')
        # if ',' in sheet_kvconfig:
        #     sheet_kvconfig = sheet_kvconfig.split(',')
    logger.info(f'----pytest_generate_tests---{metafunc.config.getoption("--path")}--------')
    # if excel_file_path == '':
    #     excel_file_path = Path(DATAS_DIR)
    #     excel_file_name = 'test_apidata.xlsx'
    #     sheet_names = 't_接'
    #     sheet_rule = 't_'
    #     sheet_kvconfig = 'config'



    path = Path().joinpath(excel_file_path, excel_file_name)
    logger.info(f'----pytest_generate_tests---{path}--------')
    logger.info(f'----pytest_generate_tests---path2--------')
    api_data = excel_to_case(path, sheet_names, sheet_rule, sheet_kvconfig)
    logger.info('----pytest_generate_tests---api_data--------')
    metafunc.parametrize('data', api_data)
    # metafunc








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
