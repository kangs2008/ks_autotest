import pytest
import allure
import os, sys
from pathlib import Path
from Common.handle_logger import logger
from api.apikeywords.apiKeyWords3 import Http
from Common.handle_excel3 import excel_to_case, load_excel, excel_to_save, Handle_excel, write_to_excel
from Common.handle_config import ReadWriteConfFile
from Common.setting import REPORT_DIR, BASE_DIR, REPORT_HTML_API_DIR
from Common.handle_file3 import current_folder_file_copy

excel_file_path = r'D:\desk20201127\ks_web_allure\Datas'
excel_file_name = 'test_apidata.xlsx'
path = Path().joinpath(excel_file_path, excel_file_name)
api_data = excel_to_case(path, 't_接', 't_', ['config'])

class TestAPI():
    def setup(self):
        self.proxies = {
            'https': 'https://127.0.0.1:8080',
            'http': 'http://127.0.0.1:8080'
        }
        logger.info('-----------setup-----------')

        report_excel = ReadWriteConfFile().get_option('report_dir', 'report_dir_folder')
        self.tmp_excel_path = Path().joinpath(REPORT_HTML_API_DIR, report_excel)

        if not Path(self.tmp_excel_path).exists():
            Path(self.tmp_excel_path).mkdir(parents=True, exist_ok=True)
        self.new_file_name = current_folder_file_copy(str(excel_file_path), str(self.tmp_excel_path), [excel_file_name],
                                                 os.path.splitext(excel_file_name)[0] + '_report')
        logger.info(f"The report file name is {self.new_file_name}")
        logger.info(f"The report file path is {self.tmp_excel_path}")
    def teardown(self):

        logger.info('-----------teardown-----------')
    @pytest.mark.parametrize('data', api_data)
    def test_all_api(self, data):

        http = Http()

        allure.dynamic.feature(f'API_interface_test')
        allure.dynamic.story(f'{list(data.values())[1]}<>{list(data.values())[0]}')
        allure.dynamic.description(f'FILE SHEET： {list(data.values())[0]}  \n\nFILE NAME： {list(data.values())[1]}  \n\nFILE PATH： {list(data.values())[2]}')
        logger.info(f'API_interface_test')
        logger.info(f'FILE SHEET： {list(data.values())[0]}  FILE NAME： {list(data.values())[1]}  FILE PATH： {list(data.values())[2]}')

        wb, sheet_obj, write_path = self.load_report_excel(list(data.values())[0])

        exec_c, col_pos_c = Handle_excel(write_path).get_column_values_by_title(sheet_obj, 'return_code')
        exec_v, col_pos_v = Handle_excel(write_path).get_column_values_by_title(sheet_obj, 'return_values')

        logger.info(f"Execute test suite: {self.__class__.__name__}")
        logger.info(f"Execute test case: {list(data.values())[0]}")

        for va in list(data.values())[3]:
            logger.info(va)
            row_pos = va['exec']
            func = getattr(http, va['method'], 'not_find')
            if va['method'].strip().lower().endswith('_api'):
                resp = func(va['input'], data=va['request_data'], proxies=None)
            else:
                resp = func(va['input'], data=va['request_data'])
            write_to_excel(sheet_obj, 'PASS', row_pos, col_pos_c)
            write_to_excel(sheet_obj, str(resp), row_pos, col_pos_v)
            logger.info(f'Function return value：{str(resp)}')

        self.save_excel_teardown(wb, write_path)

        logger.info(f"Write Excel：{'save_excel_teardown'}")

    def allurestep(self, va):
        if va['title'] != '':
            with allure.step(f"Test title：{va['title']}"):
                logger.info(f"Test title：{va['title']}")

    def __t_data(self, va):
        title = ''
        method = ''
        input = ''
        request_data = ''
        status = ''

        if va['title'] != '':
            title = va['title']
        if va['method'] != '':
            method = va['method']
        if va['input'] != '':
            input = va['input']
        if va['request_data'] != '':
            request_data = va['request_data']
        logger.info(f"Test datas:【title:[{title}], method:[{method}], input:[{input}], request_data:[{request_data}]】")

    def load_report_excel(self, sheet_name):
        write_file_path = Path().joinpath(self.tmp_excel_path, self.new_file_name)
        logger.info(self.new_file_name)
        wb, sheet = load_excel(write_file_path, sheet_name)
        logger.info(wb)
        logger.info(sheet)
        return wb, sheet, write_file_path


    def save_excel_teardown(self, wb, file_path):
        excel_to_save(wb, file_path)

    def __to_list(self, file_str, name):
        fileList = str(file_str).split(',')
        for one in fileList:
            pre = os.path.splitext(one)[0]
            if pre in name:
                return name
