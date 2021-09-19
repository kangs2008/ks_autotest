# -*- coding: utf-8 -*-
import pytest, os, time, subprocess, sys
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
        default=_date,  # 'Report_allure'
        help="current report directory"
    )


@pytest.fixture(scope="session", autouse=True)
def report(request):
    """get command line parameters
    :param request: --report
    """
    starttime = time.time()
    if str(request.config.getoption("--report")).upper() == 'REPORT_ALLURE':
        report_dir_format = start_time_format(starttime) + '_allure'
        set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
        mk_report_dir = os.path.join(REPORT_CURRENT_DIR, report_dir_format)
        os.mkdir(mk_report_dir)
        logger.info(
            f"custom addopts for the report folder:fixture name[{sys._getframe().f_code.co_name}], param[--report], value[{request.config.getoption('--report')}]")
        logger.info(f"the report folder:{mk_report_dir}")
    else:
        report_dir_format = request.config.getoption("--report") + '_allure'
        set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
        mk_report_dir = os.path.join(REPORT_CURRENT_DIR, report_dir_format)
        if not os.path.exists(mk_report_dir):
            os.mkdir(mk_report_dir)
        logger.info(
            f"custom addopts for the report folder:[{sys._getframe().f_code.co_name}],param[--report],value[{request.config.getoption('--report')}]")
        logger.info(f"the report folder:{mk_report_dir}")
    yield request.config.getoption("--report")

    cmd = 'allure generate ./temp -o ./Report --clean'
    os.system(cmd)

    logger.info(f"os.system :{cmd}")
    report_dir = ReadWriteConfFile().get_option('report_dir', 'report_dir_folder')
    copy_to = os.path.join(REPORT_CURRENT_DIR, report_dir)
    file_del(copy_to)
    file_and_folder_copy(REPORT_DIR, f'{copy_to}', [], '')
    logger.info(f"file_and_folder_copy:{copy_to}")
    set_exec_ini('report_dir', 'report_dir_folder', '')

    endtime = time.time()
    logger.info(f"------------------------")
    logger.info(use_time(starttime, endtime))
    logger.info(f"------------------------")


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
