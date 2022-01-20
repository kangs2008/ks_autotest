import pytest
import allure
from pathlib import Path
from Common.handle_logger import logger
from Common.api_keywords_excel import Http
from Common.handle_excel3 import load_excel, excel_to_save

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

    # @pytest.mark.parametrize('data', apidata)
    # def test_all_api(self, data):
    #
    #     http = Http()
    #
    #     http.create_session('s1')
    #     http.seturl(data[0]['url'])
    #     http.addheader('tou', 'add header')
    #     http.get_api('s1', data[1]['url'], data={'a':'a1'}, proxies=None)
    #
    #     http.post_api('s1', data[2]['url'], data={'d':'d1'})
    #     x = http.resp_json['headers']['X-Amzn-Trace-Id']
    #     logger.info(x)



        # logger.info(f"Write Excel：{'save_excel_teardown'}")

    @pytest.mark.parametrize('data', apidata)
    def test_all_api2(self, data):

        http = Http()

        http.create_session('s1')
        http.seturl(data[0]['url'])
        http.setheader('tou', headers={'tou':'add header'})
        http.setproxy('tou', proxies={'tou': 'add header'})
        resp = http.get_api('s1', data[1]['url'], data={'a':'a1'})
        http.save2dict('aa', '=aaaa')
        http.save2dict('bb', 'headers,X-Amzn-Trace-Id')
        http.savejson(json={"p": "p1"})

        http.post_api('s1', data[2]['url'], data={'d':'d1'})
        x = http.resp_json['headers']['X-Amzn-Trace-Id']
        logger.info(x)












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
        write_file_path = Path().joinpath(self.tmp_excel_path, self.new_file_name[0])
        logger.info(self.new_file_name)
        wb, sheet = load_excel(write_file_path, sheet_name)
        logger.info(wb)
        logger.info(sheet)
        return wb, sheet, write_file_path


    def save_excel_teardown(self, wb, file_path):
        excel_to_save(wb, file_path)
