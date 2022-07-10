import pytest
import allure
import os
from pathlib import Path
from Common.handle_logger import logger
from Common.api_keywords_excel0605 import Http
from Common.handle_excel6 import load_excel, excel_to_save, Handle_excel, write_to_excel
from Common.handle_config import ReadWriteConfFile
from Common.setting import REPORT_HTML_API_DIR, REPORT_DIR
from Common.handle_file3 import find_copy_current_folder

# sheet_names = ReadWriteConfFile().get_option('test_data', 'sheet_names')
# sheet_rule = ReadWriteConfFile().get_option('test_data', 'sheet_rule')
# sheet_kvconfig = ReadWriteConfFile().get_option('test_data', 'sheet_kvconfig')

class TestAPI():
    """
    TestAPI
    """
    test_file = []
    new_file_name = []
    write_file_path = ''
    wb = None
    def setup(self):
        logger.info('*' * 100)
        logger.info(f'---{self.__class__.__name__}--------setup-----------')
        # self.proxies = {
        #     'https': 'https://127.0.0.1:8080',
        #     'http': 'http://127.0.0.1:8080'
        # }

        report_excel = ReadWriteConfFile().get_option('report', 'report_dir_folder')
        self.tmp_excel_path = Path().joinpath(REPORT_DIR, report_excel)

        if not Path(self.tmp_excel_path).exists():
            Path(self.tmp_excel_path).mkdir(parents=True, exist_ok=True)

        excel_file_path = ReadWriteConfFile().get_option('test_data', 'excel_file_path')
        excel_file_name = ReadWriteConfFile().get_option('test_data', 'excel_file_name')
        html_file_name = ReadWriteConfFile().get_option('report', 'report_file_name')
        path = Path().joinpath(excel_file_path, excel_file_name)
        logger.info(f"The report file name is : {excel_file_name}")
        if excel_file_name not in self.test_file:
            self.test_file.append(excel_file_name)
            self.new_report_name = find_copy_current_folder(str(path), str(self.tmp_excel_path), [excel_file_name],
                                                     os.path.splitext(excel_file_name)[0] + '_report')
            self.new_file_name.append(self.new_report_name[0])
        logger.info(f"The report html name is : {html_file_name}")
        logger.info(f"The report excel name is : {self.new_file_name}")
        logger.info(f"The report file path is : {self.tmp_excel_path}")

        self.write_file_path = Path().joinpath(self.tmp_excel_path, self.new_file_name[0])
        self.wb = self.load_report_excel(self.write_file_path)

    def teardown(self):

        logger.info(f'---{self.__class__.__name__}--------teardown-----------')
        logger.info('*' * 100)
    # @pytest.mark.parametrize('data', api_data)
    @pytest.mark.usefixtures('set_report_folder_api')
    @pytest.mark.usefixtures('set_report_folder_api_teardown')
    def test_all_api(self, _data):
        """
        test_all_api
        """
        http = Http()

        allure.dynamic.feature(f'API_interface_test')
        allure.dynamic.story(f'{list(_data.values())[1]}<>{list(_data.values())[0]}')
        allure.dynamic.description(f'FILE SHEET： {list(_data.values())[0]}  \n\nFILE INSERT SHEET： {list(_data.values())[1]}  \n\nFILE CONFIG SHEET： {list(_data.values())[2]}  \n\nFILE NAME： {list(_data.values())[3]}  \n\nFILE PATH： {list(_data.values())[4]}')
        logger.info(list(_data.values()))
        logger.info(f'FILE SHEET： {list(_data.values())[0]}  FILE INSERT SHEET： {list(_data.values())[1]}  FILE CONFIG SHEET： {list(_data.values())[2]}  FILE NAME： {list(_data.values())[3]}  FILE PATH： {list(_data.values())[4]}')


        logger.info(f"Execute test suite: {self.__class__.__name__}")
        logger.info(f"Execute test case: {list(_data.values())[0]}")

        setattr(http, '_sheet_name', list(_data.values())[0])

        for i in range(1, len(list(_data.values())[5]) + 1):
            va = list(_data.values())[5][i-1]
            row_pos = va['exec']
            # logger.info(3333333)
            self.allurestep(va, str(i).zfill(3))
            self.__t_data(va, str(i).zfill(3))

            setattr(http, '_step_num', str(i).zfill(3))

            func = getattr(http, va['method'], 'The method not find in Http Class.')
            code = None
            # if isinstance(func, str):
            #     status = 'FAIL'
            #     resp = func
            #     code = ''
            # logger.error(func)

            # if va['method'].strip().lower().endswith('_api') and str(va['request_data']).strip() == '':
            if va['method'].strip().lower().endswith('_api'):
                status, resp, code = func(va['request_key'], va['request_data'])
            else:
                if isinstance(func, str):
                    status = 'FAIL'
                    resp = func
                else:
                    status, resp = func(va['request_key'], va['request_data'])

            if list(_data.values())[1] != '' and list(_data.values())[1] in va['title']:
                obj = self.wb[list(_data.values())[1]]
            else:
                obj = self.wb[list(_data.values())[0]]
            exec_c, col_pos_c = Handle_excel(self.write_file_path).get_column_values_by_title(obj, 'return_code')
            exec_v, col_pos_v = Handle_excel(self.write_file_path).get_column_values_by_title(obj, 'return_values')
            exec_s, col_pos_s = Handle_excel(self.write_file_path).get_column_values_by_title(obj, 'status')
            if status == 'FAIL':
                write_to_excel(obj, 'FAIL', row_pos, col_pos_c)
                write_to_excel(obj, str(resp), row_pos, col_pos_v)
                if code:
                    write_to_excel(obj, str(code), row_pos, col_pos_s)
            else:
                write_to_excel(obj, 'PASS', row_pos, col_pos_c)
                write_to_excel(obj, str(resp), row_pos, col_pos_v)
                if code:
                    write_to_excel(obj, str(code), row_pos, col_pos_s)
            self.save_excel_teardown()

        logger.info(f"Write Excel：{'save_excel_teardown'}")

    def allurestep(self, va, _num):
        if va['title'] != '':
            with allure.step(f"[{_num}]Test title：{va['title']}"):
                logger.info(f"[{_num}]Test title：{va['title']}")

    def __t_data(self, va, _num):
        title = ''
        method = ''
        request_key = ''
        request_data = ''
        num = ''
        if va['num'] != '':
            num = va['num']
        if va['title'] != '':
            title = va['title']
        if va['method'] != '':
            method = va['method']
        if va['request_key'] != '':
            request_key = va['request_key']
        if va['request_data'] != '':
            request_data = va['request_data']
        logger.info(f"[{_num}]Test datas:【num:[{num}], title:[{title}], method:[{method}], request_key:[{request_key}], request_data:[{request_data}]】")

    def load_report_excel(self, write_file_path):
        wb = load_excel(write_file_path)
        return wb

    def save_excel_teardown(self):
        excel_to_save(self.wb, self.write_file_path)
