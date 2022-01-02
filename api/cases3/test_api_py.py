import pytest
import allure
import os, sys
from Common.handle_logger import logger
from api.apikeywords.apiKeyWords3 import Http
from Common.handle_excel import excel_to_case, load_excel, excel_to_save, Handle_excel
from Common.handle_config import ReadWriteConfFile
from Common.setting import REPORT_DIR, BASE_DIR
num = '1'
execfile = r''
apidata = [[{'method':'seturl', 'url':'http://httpbin.org'},
            {'method':'get_api', 'url':'get'},
            {'method':'post_api', 'url':'post'},
            {'method':'get_api', 'url':'get'}
]]

class TestAPI():

    def setup(self):
        self.proxies = {
            'https': 'https://127.0.0.1:8080',
            'http': 'http://127.0.0.1:8080'
        }
        logger.info('setup-----------')
    def teardown(self):

        logger.info('teardown-----------')

    @pytest.mark.parametrize('data', apidata)
    def test_all_api(self, requests_session, data):

        http = Http()

        http.create_session()
        http.seturl(data[0]['url'])
        http.addheader('tou', 'add header')
        http.get_api(data[1]['url'], data={'a':'a1'}, proxies=self.proxies)

        http.post_api(data[2]['url'], data={'d':'d1'})
        x = http.resp_json['headers']['X-Amzn-Trace-Id']
        logger.info(x)







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

    def load_excel_setup(self, sheet_name, file_name, file_path):
        if num == '':
            numstr = ''
        else:
            numstr = f'(' + num + ')'
        p = self._re_file_path(file_path)
        write_file_name = os.path.splitext(file_name)[0] + '_report' + numstr + os.path.splitext(file_name)[1]
        new_path = file_path.replace(file_path, tmp_excel_path)

        if p:
            new_path = new_path + p

        write_file_path = os.path.join(new_path, write_file_name)
        logger.info(f'aaaaaaaa{write_file_path}')
        wb, sheet = load_excel(write_file_path, sheet_name)
        return wb, sheet, write_file_path
    def _re_file_path(self, file_path):
        datas_path = os.path.join(BASE_DIR, "Datas")
        logger.info(file_path)
        logger.info(datas_path)
        logger.info('datas_path')
        if sys.platform == 'win32':
            new_report_path = file_path.replace(datas_path.replace('\\', '/'), '')
            # p, f = os.path.split(new_report_path.replace('/', '\\'))
            p, f = os.path.split(new_report_path)
        else:
            new_report_path = file_path.replace(datas_path, '')
            p, f = os.path.split(new_report_path)
        return p

    def save_excel_teardown(self, wb, file_path):
        excel_to_save(wb, file_path)

    def __to_list(self, file_str, name):
        fileList = str(file_str).split(',')
        for one in fileList:
            pre = os.path.splitext(one)[0]
            if pre in name:
                return name
