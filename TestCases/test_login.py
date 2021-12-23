import pytest
import allure
import sys, re, os
from Common.handle_logger import logger
from Pages.BaiduPage.baidu_page import BaiduPage
from Common.handle_excel import excel_to_case, load_excel, excel_to_save, Handle_excel
from Common.handle_config import ReadWriteConfFile
from Common.utils import usageTime, mTime

def get_excel_data():
    # execfile = ReadWriteConfFile().get_option('exec', 'exec_file_path')
    # execst = ReadWriteConfFile().get_option('exec', 'st')
    execsheet = ReadWriteConfFile().get_option('exec', 'exec_sheet_name')
    webdata = excel_to_case(os.path.dirname(__file__), 'execst', execsheet)
    return webdata

# @allure.feature("login 异常测试用例，feature")
@pytest.mark.usefixtures('start_session')
# @pytest.mark.usefixtures('report')
# @pytest.mark.usefixtures('refresh_page')
class TestWebUI:

    # @allure.story("111测试login 方法，baidu")
    @pytest.mark.parametrize('data', get_excel_data())
    def test_web_ui(self, data, start_session):
        """描述！！！！"""
        allure.dynamic.feature(f'{os.path.basename(__file__)}')
        allure.dynamic.story(f'{list(data.values())[0]}<>{list(data.values())[1]}')
        logger.info(f" 执行 {os.path.basename(__file__)}.{self.__class__.__name__}.{sys._getframe().f_code.co_name} 测试套件Suite ")
        logger.info(f" 执行 {list(data.values())[0]} 测试用例Case ")
        logger.info(f" 执行 {data}")

        allure.dynamic.description(
            f'FILE SHEET： {list(data.values())[0]}  \n\nFILE NAME： {list(data.values())[1]}  \n\nFILE PATH： {list(data.values())[2]}')
        logger.info(
            f'FILE SHEET： {list(data.values())[0]}  FILE NAME： {list(data.values())[1]}  FILE PATH： {list(data.values())[2]}')
        # _data = list(data.values())[3]
        _dict = {}
        for i in range (0, len(list(data.values())[3])):
            va = list(data.values())[3][i]
            # self.allurestep(va)  # tilte only
            self.__t_data(i+1, va)
            re_value = va['return_values']

            func = getattr(BaiduPage(start_session), va['method'])
            ps = [_dict.get(p, p) for p in (va['parameter']).split(',')]
            if ps[0] == '':
                ps.clear()
                ps.append(va['capture'])
            else:
                ps.append(va['capture'])
            if va['method'].startswith('assert'):
                logger.info(f'----{func}----')
                logger.info(f'----func(\"{ps[0]}\", \"{va["expect"]}\")----')
                func(ps[0], va['expect'])
            else:
                return_value = func(*ps)
                logger.info(f'----"{return_value}" = func(*ps)----')
                if return_value:
                    logger.info(f'----re_value = va["return_values"] = "{re_value}"----')
                    _dict[re_value] = return_value
                    logger.info(f'----_dict["{re_value}"] = "{return_value}"----')



    def allurestep(self, va):
        if va['title'] != '':
            with allure.step(f"test title：{va['title']}"):
                logger.info(f"test title：{va['title']}")

    def __t_data(self, count, va):
        title = ''
        page = ''
        method = ''
        parameter = ''
        return_values = ''
        expect = ''
        capture = ''

        if va['title'] != '':
            title = va['title']
        if va['page'] != '':
            page = va['page']
        if va['method'] != '':
            method = va['method']
        if va['parameter'] != '':
            parameter = va['parameter']
        if va['return_values'] != '':
            return_values = va['return_values']
        if va['expect'] != '':
            expect = va['expect']
        if va['capture'] != '':
            capture = va['capture']
        logger.info(f"test step{count}:【title:[{title}], page:[{page}], method:[{method}], parameter:[{parameter}], return_values:[{return_values}], expect:[{expect}], capture:[{capture}]】")

        with allure.step(f"[{mTime()}]test step{count}:【title:[{title}], page:[{page}], method:[{method}], parameter:[{parameter}], return_values:[{return_values}], expect:[{expect}], capture:[{capture}]】"):
            pass

    def __new_data(self, param, _data):
        pattern = r'[$][{](.*?)[}]'
        param = param.replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
        for key in _data:
            logger.info(f"----------数据--------------------[{key}]>>{_data[key]}--")
            res = re.findall(pattern, param)
            if res:
                for r in res:
                    if r == key:
                        param = param.replace('${' + key + '}', str(_data[key]))
                        logger.info(f"----------数据预处理after:--self.relations[{key}]>>{_data[key]}--")
        return param

    def __new_dict(self, param, return_value, _dict):
        param = param.replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
        if param is None or param == '':
            return _dict
        else:
            if (param).startswith('${') and (param).endswith('}'):
                pass
            else:
                _dict[param] = return_value
                logger.info('66666666666666666')
            return _dict

    def __get_relations(self, param, _data):
        pattern = r'[$][{](.*?)[}]'
        if param is None or param == '':
            return None
        else:
            for key in _data:
                logger.info(f"----------数据--------------------[{key}]>>{_data[key]}--")
                res = re.findall(pattern, param)
                if res:
                    for r in res:
                        if r == key:
                            param = param.replace('${' + key + '}', str(_data[key]))
                            logger.info(f"----------数据预处理after:--self.relations[{key}]>>{_data[key]}--")
            return param
    def __get_data(self, param, _data):
        if (param is None) or param == '':
            return None
        else:
            param = param.replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
            paramn = self.__get_relations(param, _data)
            # paramn = json.loads(paramn)
            logger.info(f"----------数据预处理before:--json.loads(paramn)>>{type(param)}>>{param}--")
            logger.info(f"----------数据预处理after :--json.loads(paramn)>>{type(paramn)}>>{paramn}--")
            return  paramn

