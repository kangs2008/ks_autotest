# -*- coding: utf-8 -*-
import pytest, os, time
import requests
from Common.handle_logger import logger
from Common.handle_config import ReadWriteConfFile
from Common.utils import start_time_format, use_time, report_date_folder
from Common.handle_file import file_zip_path, file_del, file_copy, file_and_folder_copy, current_folder_file_copy
from Common.setting import BASE_DIR, REPORT_DIR, REPORT_CURRENT_DIR
_session = None

_date = report_date_folder()

def pytest_addoption(parser):
    """add --report"""
    parser.addoption(
        "--report",
        action="store",
        default=_date,  #'Report_allure'
        help="current report directory"
    )

@pytest.fixture(autouse=True)  # setup
def report(request):
    """获取命令行参数，给到环境变量"""
    starttime = time.time()
    print(request.config.getoption("--report"))
    if str(request.config.getoption("--report")).upper() == 'REPORT_ALLURE':
        report_dir_format = start_time_format(starttime) + '_allure'
        print(report_dir_format)
        logger.info(f" --------1111-----------{report_dir_format} 测试用例Case ")
        set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
        file_del(os.path.join(BASE_DIR, 'temp'))
        mk_report_dir = os.path.join(REPORT_CURRENT_DIR, report_dir_format)
        logger.info(f" -----------11--------{mk_report_dir} ")
        os.mkdir(mk_report_dir)
    else:
        report_dir_format = request.config.getoption("--report") + '_allure'
        print(report_dir_format)
        logger.info(f" -----------222--------{report_dir_format} 测试用例Case ")
        set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
        file_del(os.path.join(BASE_DIR, 'temp'))
        mk_report_dir = os.path.join(REPORT_CURRENT_DIR, report_dir_format)
        logger.info(f" -----------222--------{mk_report_dir} ")
        if not os.path.exists(mk_report_dir):
            os.mkdir(mk_report_dir)

    yield request.config.getoption("--report")

    logger.info(f" -----------我是 tear down22-------- ")

def set_exec_ini(section, option, value):
    ReadWriteConfFile().add_section(section)
    ReadWriteConfFile().set_option(section, option, value)
















@pytest.fixture(scope="function", autouse=False)
def requests_session():
    """
    init requests.session()
    """
    logger.info('*'*100)
    logger.info('*'*20 + '测试执行开始' + '*'*20)
    global _session
    _session = requests.session()
    logger.info(f'----------requests_session setup----------')
    logger.info(f'获取session：{_session}')
    yield _session
    _session.close()
    logger.info(f'销毁session：{_session}')
    logger.info(f'----------requests_session teardown----------')
    logger.info('*'*20 + '测试执行结束' + '*'*20)
    logger.info('*' * 100)

