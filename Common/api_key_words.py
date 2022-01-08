import json, sys
import re
import allure
import jsonpath
import requests

from Common.handle_logger import logger
from Common.handle_json import HandleJson
import jmespath

class Http(object):

    def __init__(self):
        self.baseurl = ''
        self.session = None

        self.resp_json = {}
        self.relations = {}
        self.param = {}
        self.return_values = None

    def __url(self, url_path):
        new_url = ''
        if (url_path is not None) and (url_path.startswith('http')):
            self.baseurl = url_path
            return self.baseurl
        else:
            if url_path != '' and url_path is not None:
                if not self.baseurl.startswith('http'):
                    logger.info(f"❌ The input URL '{url_path}' incorrect.")
                    raise  Exception(f"❌ The input URL '{url_path}' incorrect.")
                else:
                    if str(self.baseurl)[-1:] == '/':
                        new_url = self.baseurl + url_path
                    else:
                        new_url = self.baseurl + '/' + url_path
            else:
                if not self.baseurl.startswith('http'):
                    logger.info(f"❌ The input URL '{url_path}' incorrect.")
                    raise  Exception(f"❌ The input URL '{url_path}' incorrect.")
        return new_url


    def addheader(self, _key, _value):
        try:
            logger.info(f"[{sys._getframe().f_code.co_name}]-->self.session.headers[{_key}] = {_value}")

            self.session.headers[_key] = _value
            return self.session.headers
        except Exception as e:
            logger.info(f"❌ [{sys._getframe().f_code.co_name}]-->self.session.headers[{_key}] = {_value}")
            logger.error(e)

    def seturl(self, _url, *args, **kwargs):

        if (_url is not None) and (_url.startswith('http')):
            self.baseurl = _url
            self.return_value = self.baseurl
            logger.info(f"[{sys._getframe().f_code.co_name}]-->{self.baseurl}")
        else:
            logger.info(f"❌ [{sys._getframe().f_code.co_name}]-->{self.baseurl}")
            self.return_value = self.baseurl
            raise Exception(f"❌ The input URL {_url} incorrect.")

    def __get_relations(self, param):
        pattern = r'[$][{](.*?)[}]'
        logger.info(param)
        if param is None or param == '':
            return ''
        else:
            for key in self.relations.keys():
                res = re.findall(pattern, param)
                if res:
                    for r in res:
                        if r == key:
                            param = param.replace('${' + key + '}', str(self.relations[key]))
                            logger.info(f"----------数据预处理after:--self.relations[{key}]>>{self.relations[key]}--")
            return param

    def __get_data(self, param):
        """ for saveparam """
        # if (param is None) or param == '':
        #     return None
        # else:
        param = param.replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
        paramn = self.__get_relations(param)
        paramn = json.loads(paramn)
        logger.info(f"----------数据预处理before:--json.loads(paramn)>>{type(param)}>>{param}--")
        logger.info(f"----------数据预处理after :--json.loads(paramn)>>{type(paramn)}>>{paramn}--")
        return paramn


    def saveparam(self, *args, **kwargs):
        try:
            input_data = (tuple(args)[0]).strip()
            request_data = str(kwargs['data'])
            logger.info(request_data)
            if str(request_data).startswith('${') and str(request_data).endswith('}'):
                request_data_value = self.__get_data(str(request_data))
            else:
                request_data_value = self.__get_relations(request_data)
            logger.info(f'-----------request_data_value   {request_data_value}')
            self.param[input_data] = request_data_value
            self.return_value = self.param
            logger.info(f"[{sys._getframe().f_code.co_name}]after-->self.param==>>{self.param}")
            return self.return_value
        except Exception as e:
            self.param = {}
            self.return_value = None
            logger.error(e)

    def save2dict(self, *args, **kwargs):
        """ to dict {'a': 'b'} """
        try:
            input_data = (tuple(args)[0]).strip()
            request_data = kwargs['data']

            if str(request_data).strip().startswith('${') and str(request_data).strip().endswith('}'):
                _value = str(request_data).strip().replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
                _value = self.__get_relations(_value)
                request_data_vlaue = eval(_value)
            else:
                request_data_vlaue = self.__get_relations(str(request_data).strip())
            logger.info(f'aaaaaaaaaaaaaaa{request_data_vlaue}')
            logger.info(f"[{sys._getframe().f_code.co_name}]before-->self.relations==>>{self.relations}")
            self.relations[input_data] = request_data_vlaue
            self.return_value = self.relations[input_data]
            return self.relations
        except Exception as e:
            self.return_value = None
            logger.error(e)


    def get_api(self, _url, *args, **kwargs):
        params = str(kwargs['data'])
        if not self.session:
            self.create_session()
        new_url = self.__url(_url)
        if '${' in new_url:
            new_url = self.__get_relations(new_url)
        logger.info(f"[{sys._getframe().f_code.co_name}]before-->[URL:{new_url}],[**KWARGS:{kwargs}]")

        if params != '':
            self.param.update(self.__params2get(params))
        logger.info(f"[{sys._getframe().f_code.co_name}]before-->[params/kwargs['data']:{params}]")
        kwargs.pop('data')
        res = self.session.get(new_url, params=self.param, **kwargs)
        try:
            resp = res.json()
            logger.info(f"[{sys._getframe().f_code.co_name}]after-->[Response.json()==>>{resp}]")
        except Exception as msg:
            resp = res.text
            logger.info(f"warning: {msg}")
            logger.info(f"[{sys._getframe().f_code.co_name}]after-->[Response.text==>>\n{resp}]")
        else:
            self.param = {}
            self.return_value = resp
            self.resp_json = resp
            return resp

    def __params2get(self, param):
        """ for get_api self.param """
        if str(param).strip().startswith('{') and str(param).strip().endswith('}'): # for py
            return eval(param) # 20220108
        else:
            if '=' not in param:
                logger.error("The input parameters should contain '='.  e.g. xx1=aa,xx2=bb")
                raise Exception("The input parameters should contain '='.  e.g. xx1=aa,xx2=bb")
            else:
                _dict = {}
                _key = (param).strip().split('=')[0]
                _value = (param).strip().split('=')[1]
                if str(_value).strip().startswith('{') and str(_value).strip().endswith('}'):
                    _value = _value.replace('\'', '"').replace('\n', '').replace('\r', '').replace(
                        '\t', '')
                    _valuen = self.__get_relations(_value)
                    _dict[_key] = _valuen
                else:
                    _dict[_key] = self.__get_relations(_value)
                return _dict

    def __params2post(self, _data):
        """ for post_api data/json """
        _dict = {}
        logger.info('----_data--' + str(_data))
        if (str(_data).strip().startswith('{') and str(_data).strip().endswith('}')) or (str(_data).strip().startswith('[{') and str(_data).strip().endswith('}]')):
            _value = str(_data).strip().replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
            _valuen = self.__get_relations(_value)
            _dict = json.loads(str(_valuen))
        elif '=' not in _data:
            logger.error("The input parameters should contain '=' or dict type.  e.g. xx1=aa or {'xx': 'cc'}")
            raise Exception("The input parameters should contain '=' or dict type.  e.g. xx1=aa or {'xx': 'cc'}")
        else:
            _key = str(_data).strip().split('=')[0]
            _value = str(_data).strip().split('=')[1]
            _value = _value.replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
            _valuen = self.__get_relations(_value)
            logger.info('----_valuen--'+_valuen)
            _dict[_key] = _valuen
            return _dict


    def post_api(self, _url, *args, **kwargs):
        _data = str(kwargs['data'])
        if not self.session:
            self.create_session()
        new_url = self.__url(_url)
        if '${' in new_url:
            new_url = self.__get_relations(new_url)
        logger.info(f"[{sys._getframe().f_code.co_name}]before-->[URL:{new_url}],[**KWARGS:{kwargs}]")
        _dataN = self.__params2post(_data)

        logger.info(f"[{sys._getframe().f_code.co_name}]before-->[json/kwargs['data']/self.__params2post:{_dataN}]")
        kwargs.pop('data')
        res = self.session.post(new_url, json=_dataN, **kwargs)
        try:
            resp = res.json()
            logger.info(f"[{sys._getframe().f_code.co_name}]after-->[Response.json()==>>{resp}]")
        except Exception as msg:
            resp = res.text
            logger.info(f"warning: {msg}")
            logger.info(f"[{sys._getframe().f_code.co_name}]after-->[Response.text==>>\n{resp}]")
        else:
            self.return_value = resp
            self.resp_json = resp
            return resp

    def put_api(self):
        pass
    def delete_api(self):
        pass

    def create_session(self):
        """
        A Requests session
        :return:
        """
        self.session = requests.Session()

        logger.info(f"[{sys._getframe().f_code.co_name}]after-->{self.session}")
        return self.session

    def __abs(self, datan):
        """ for savejson """
        dataL = datan.split(',')
        tmp = ''
        for one in dataL:
            if one.strip().isdigit():
                tmp = tmp + f"[{one.strip()}]"
            else:
                tmp = tmp + f"['{one.strip()}']"
        logger.info(f"----------数据预处理after:--__abs(datan)>>{datan}>>{tmp}--")
        return tmp

    def savejson(self, *args, **kwargs):
        """ from self.resp_json to self.relations """
        try:
            input_data = (tuple(args)[0]).strip()
            request_data = kwargs['data']
            # input_data = args[0]
            # request_data = args[1]
            logger.info(f"[{sys._getframe().f_code.co_name}]before-->self.relations==>>{self.relations}")
            request_data_path = self.__abs(request_data)
            request_data_vlaue = eval(str(self.resp_json) + str(request_data_path))
            self.relations[input_data.strip()] = str(request_data_vlaue)
            self.return_value = self.relations[input_data.strip()]
            logger.info(f"[{sys._getframe().f_code.co_name}]after-->self.relations==>>{self.relations}")
            return {f'{input_data}': f'{request_data_vlaue}'}
        except Exception as e:
            logger.error(e)

    def __allurestep(self, str_fail='FAIL'):
        if str_fail == 'FAIL':
            with allure.step(f"对比结果：{str_fail}"):
                pass

    def assertInJson(self, *args, **kwargs):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
        input_data = (tuple(args)[0]).strip()
        request_data = kwargs['data']

        res = jsonpath.jsonpath(self.resp_json, f'$..{input_data}')  # 找不到是结果是 False

        logger.info(f"ACTUAL_VALUE:[{res}]")
        logger.info(f"EXPECT_VALUE:[{request_data}]")
        try:
            if isinstance(res, list) and len(res) == 1:
                assert request_data == res[0]
            elif isinstance(res, list) and len(res) > 1:
                assert request_data in res
            else:
                assert request_data == res
        except AssertionError as e:
            self.return_value('FAIL')
            logger.info('--Fail--用例失败--')
            logger.exception(e)
            # raise
            str_result = 'FAIL'
        else:
            self.return_value('PASS')
            logger.info('--Pass--用例成功--')
            str_result = 'PASS'

    # def assertSchema(self, schema):
    #     """
    #     Assert JSON Schema
    #     doc: https://json-schema.org/
    #     """
    #     try:
    #         validate(instance=ResponseResult.response, schema=schema)
    #     except ValidationError as msg:
    #         self.assertEqual("Response data", "Schema data", msg)
    #     else:
    #         self.assertTrue(True)

    def assertAbsPath(self, *args, **kwargs):
        """
        Assert Absolute path data
        doc: https://jmespath.org/

        {"a": [{"b": "b1"}, {"c": "c1"}]}
        assertAbsPath(self, 'a[0].b', 'b1')
        :param abs_path:
        :param expect_json:
        """
        abs_path = (tuple(args)[0]).strip()
        expect_value = kwargs['data']

        search_value = jmespath.search(abs_path, self.resp_json)
        if search_value is None:
            logger.info(f"执行函数search_value:{search_value}")
            assert abs_path, None
        else:
            logger.info(f"执行函数search_value2:{search_value}")
            assert search_value, expect_value
        pass

    def assertResp2Json(self, *args, **kwargs):
        """
        z = {"a": [{"b": "b1"}, {"c": "c1"}]}
        assertResp2Json(self, z, {"a": [{"b": "b1"}, {"c": "c1"}]})

        :param resp_json:
        :param expect_json:
        """
        # abs_path = (tuple(args)[0]).strip()
        expect_json = kwargs['data']
        try:
            _value = str(expect_json).strip().replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
            _valuen = self.__get_relations(_value)
            _dict = json.loads(str(_valuen))

            error_count = HandleJson().json_assert(self.resp_json, _dict)
            logger.info(f"执行函数:{sys._getframe().f_code.co_name}--")
            if error_count != 0:
                raise Exception('aaaaaa')
        except Exception as e:
            logger.error(e)
        else:
            pass

    def assertMatch2Json(self, *args, **kwargs):
        """
        {"a": [{"b": "b1"}, {"c": "c1"}]}
        assertMatch2Json(self, 'a[0]', '{"b": "b1"}')
        doc: https://jmespath.org/
        :param part_path:
        :param expect_json:
        """
        part_path = (tuple(args)[0]).strip()
        expect_json = kwargs['data']

        search_value = jmespath.search(part_path, self.resp_json)


        try:
            logger.info(f"执行函数----search_value:{search_value}")
            _value = str(expect_json).strip().replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
            _valuen = self.__get_relations(_value)
            _dict = json.loads(str(_valuen))

            error_count = HandleJson().json_assert(search_value, _dict)
            if error_count != 0:
                raise Exception('aaaaaa')
        except AssertionError as e:
            self.return_value('FAIL')
            logger.info('--Fail--用例失败--')
            logger.exception(e)
            # raise
            str_result = 'FAIL'
        else:
            logger.info('--Pass--用例成功--')
            str_result = 'PASS'




    def return_value(self, value):
        with allure.step(f"值是：{value}"):
            logger.info(f"值是：{value}")

if __name__ == '__main__':
    pass
