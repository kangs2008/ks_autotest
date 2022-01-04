# -*- coding: utf-8 -*-

import pytest
import allure
import requests
from Common.handle_logger import logger
from Common.handle_config import ReadWriteConfFile
from Common.utils import mDate, mDateTime


_session = None

@pytest.fixture(scope="function", autouse=False)
def set_report_folder_api(request):
    """get command line parameters
    :param request: --report
    """
    report_dir = ReadWriteConfFile().get_option('report', 'report_dir_folder')
    logger.info('----set_report_folder_api---report_dir--------')
    if report_dir == '':
        _set_exec_ini('report', 'report_dir_folder', mDate()+'_html_api')
        _set_exec_ini('report', 'report_file_name', f'report_{mDateTime()}.html')
    yield
    _set_exec_ini('report', 'report_dir_folder', '')
    _set_exec_ini('report', 'report_file_name', '')

    _set_exec_ini('test_data', 'excel_file_path', '')
    _set_exec_ini('test_data', 'excel_file_name', '')
    _set_exec_ini('test_data', 'sheet_names', '')
    _set_exec_ini('test_data', 'sheet_rule', '')
    _set_exec_ini('test_data', 'sheet_kvconfig', '')

def _set_exec_ini(section, option, value):
    ReadWriteConfFile().add_section(section)
    ReadWriteConfFile().set_option(section, option, value)