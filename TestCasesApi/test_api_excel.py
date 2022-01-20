import pytest
import allure
import os
from pathlib import Path
from Common.handle_logger import logger
from Common.api_keywords_excel import Http
from Common.handle_excel3 import load_excel, excel_to_save, Handle_excel, write_to_excel
from Common.handle_config import ReadWriteConfFile
from Common.setting import REPORT_HTML_API_DIR
from Common.handle_file3 import find_copy_current_folder

# sheet_names = ReadWriteConfFile().get_option('test_data', 'sheet_names')
# sheet_rule = ReadWriteConfFile().get_option('test_data', 'sheet_rule')
# sheet_kvconfig = ReadWriteConfFile().get_option('test_data', 'sheet_kvconfig')

class TestAPI():
    def setup(self):
        self.proxies = {
            'https': 'https://127.0.0.1:8080',
            'http': 'http://127.0.0.1:8080'
        }
        logger.info('-----------setup-----------')

        report_excel = ReadWriteConfFile().get_option('report', 'report_dir_folder')
        self.tmp_excel_path = Path().joinpath(REPORT_HTML_API_DIR, report_excel)

        if not Path(self.tmp_excel_path).exists():
            Path(self.tmp_excel_path).mkdir(parents=True, exist_ok=True)

        excel_file_path = ReadWriteConfFile().get_option('test_data', 'excel_file_path')
        excel_file_name = ReadWriteConfFile().get_option('test_data', 'excel_file_name')
        path = Path().joinpath(excel_file_path, excel_file_name)
        logger.info(f"The report file name is {excel_file_name}")
        self.new_file_name = find_copy_current_folder(str(path), str(self.tmp_excel_path), [excel_file_name],
                                                 os.path.splitext(excel_file_name)[0] + '_report')
        logger.info(f"The report file name is {self.new_file_name}")
        logger.info(f"The report file path is {self.tmp_excel_path}")
    def teardown(self):

        logger.info('-----------teardown-----------')
    # @pytest.mark.parametrize('data', api_data)
    @pytest.mark.usefixtures('set_report_folder_api')
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

        for i in range(1, len(list(data.values())[3]) + 1):
            # logger.info(va)
            va = list(data.values())[3][i-1]
            row_pos = va['exec']

            setattr(http, 'step_num', str(i).zfill(3))

            func = getattr(http, va['method'], 'not_find')
            # if isinatance(func, str):
            #     logger.info("aaaa")
            if va['method'].strip().lower().endswith('_api') and str(va['request_data']).strip() == '':
                resp = func(va['request_key'])
            else:
                resp = func(va['request_key'], va['request_data'])
            if str(resp[0]) == 'FAIL':
                write_to_excel(sheet_obj, 'FAIL', row_pos, col_pos_c)
                write_to_excel(sheet_obj, str(resp[1]), row_pos, col_pos_v)
            else:
                write_to_excel(sheet_obj, 'PASS', row_pos, col_pos_c)
                write_to_excel(sheet_obj, str(resp[1]), row_pos, col_pos_v)
            # logger.info(f'Function return value：{str(resp)}')

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
        write_file_path = Path().joinpath(self.tmp_excel_path, self.new_file_name[0])
        logger.info(self.new_file_name)
        wb, sheet = load_excel(write_file_path, sheet_name)
        logger.info(wb)
        logger.info(sheet)
        return wb, sheet, write_file_path


    def save_excel_teardown(self, wb, file_path):
        excel_to_save(wb, file_path)
