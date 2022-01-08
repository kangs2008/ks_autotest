# -*- coding: utf-8 -*-
import pytest
from Common.handle_logger import logger
from Common.handle_config import ReadWriteConfFile
from Common.utils import mDate, mDateTime
from Common.handle_excel3 import excel_to_case
from pathlib import Path

@pytest.fixture(scope="function", autouse=False)
def set_report_folder_api(request):
    """set_report_folder_api
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


# def pytest_generate_tests(metafunc):
#     """for TestCasesApi data"""
#
#     excel_file_path = metafunc.config.getoption("--path").strip()
#     excel_file_name = metafunc.config.getoption("--name").strip()
#     sheet_names = metafunc.config.getoption("--sheet").strip()
#     sheet_rule = metafunc.config.getoption("--rule").strip()
#     sheet_kvconfig = metafunc.config.getoption("--conf").strip()
#     if excel_file_path.lower() != 'no_set_path':
#         ReadWriteConfFile().set_option('test_data', 'excel_file_path', excel_file_path)
#         ReadWriteConfFile().set_option('test_data', 'excel_file_name', excel_file_name)
#         ReadWriteConfFile().set_option('test_data', 'sheet_names', sheet_names)
#         ReadWriteConfFile().set_option('test_data', 'sheet_rule', sheet_rule)
#         ReadWriteConfFile().set_option('test_data', 'sheet_kvconfig', sheet_kvconfig)
#     else:
#         ReadWriteConfFile().get_option('test_data', 'excel_file_path')
#         ReadWriteConfFile().get_option('test_data', 'excel_file_name')
#         ReadWriteConfFile().get_option('test_data', 'sheet_names')
#         ReadWriteConfFile().get_option('test_data', 'sheet_rule')
#         ReadWriteConfFile().get_option('test_data', 'sheet_kvconfig')
#     if ',' in sheet_names:
#          sheet_names = sheet_names.split(',')
#     if ',' in sheet_kvconfig:
#         sheet_kvconfig = sheet_kvconfig.split(',')
#     logger.info(f'----pytest_generate_tests---{metafunc.config.getoption("--path")}--------')
#
#
#     path = Path().joinpath(excel_file_path, excel_file_name)
#     logger.info(f'----pytest_generate_tests---{path}--------')
#     logger.info(f'----pytest_generate_tests---path2--------')
#     api_data = excel_to_case(path, sheet_names, sheet_rule, sheet_kvconfig)
#     logger.info('----pytest_generate_tests---api_data--------')
#     metafunc.parametrize('data', api_data)
