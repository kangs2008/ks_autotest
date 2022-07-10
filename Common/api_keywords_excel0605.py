import inspect
import json, sys
import re
import allure
import jsonpath
import requests
from Common.utils import mTime
from Common.handle_logger import logger
from Common.handle_json import HandleJson
import jmespath
import Common.utils as utils
from pathlib import Path


py_module = [utils]

class Http(object):

    def __init__(self):
        self._baseurl = {}
        self._recent_resp_json = {}
        # self.resp_json_alias = {}
        self.relations = {}
        self._session = {}
        self._step_num = 0

    def seturl(self, *args):
        """
        set base URL
        :param: alias
        :return: self._baseurl
        """
        alias = str(tuple(args)[0]).strip()
        _baseurl = str(tuple(args)[1]).strip()
        msg = f"[{mTime()}][{self._step_num}][seturl] before-->[*ARGS:{args}]"
        with allure.step(msg):
            logger.info(msg[14:])
        if alias == '':
            msg = f"[{mTime()}][{self._step_num}][seturl]❌ The 'request_key' is empty, please set url alias."
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:]
        else:
            if _baseurl == '':
                msg = f"[{mTime()}][{self._step_num}][seturl]❌ Please set base url."
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:]
            elif not _baseurl.lower().startswith('http'):
                msg = f"[{mTime()}][{self._step_num}][seturl]❌ The input URl '{_baseurl}' incorrect. Should start 'http'."
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:]
            else:
                self._baseurl[alias] = _baseurl
                msg = f"[{mTime()}][{self._step_num}][seturl] Base URL self._baseurl[{alias}] = {_baseurl}"
                with allure.step(msg):
                    logger.info(msg[14:])
                return "PASS", self._baseurl

    def __get_utils(self, param, _py_module, *args):
        pattern = r'[#][{](.*?)[}]'
        if param is None or param == '':
            return ''
        else:
            res = re.findall(pattern, param)
            if res:
                for _method in res:
                    count = 0
                    _dict = {}
                    for one in _py_module:
                        func = getattr(one, _method, '_method not found')
                        if isinstance(func, str):
                            count += 1
                            _dict[one] = f'The function "{_method}" not found in {one}'
                        else:
                            func = getattr(one, _method, '_method not found')
                            param = param.replace('#{' + _method + '}', func(*args))
                            msg = f"[{mTime()}][{self._step_num}][{inspect.stack()[1][3]}.__get_utils]-----Data preprocessing after, function: {_method} >> {param}"
                            with allure.step(msg):
                                logger.info(msg[14:])
                    if count == len(_py_module):
                        raise Exception(_dict)
            return param

    def otherUtils(self, *args):
        """
        goto python module, find function, exectue
        :param: add dict_key to self.relations
        :param: #{method name of python function}
        :return: dict
        """
        try:
            request_key = str(tuple(args)[0]).strip()
            request_data = str(tuple(args)[1]).strip()
            msg = f"[{mTime()}][{self._step_num}][otherUtils] before-->[*ARGS:{args}]"
            with allure.step(msg):
                logger.info(msg[14:])
            if ',' not in request_data:
                _value = self.__get_utils(request_data, py_module)
                self.relations[request_key] = _value
            else:
                new_input_data = request_data.split(',', 1)
                _method = (new_input_data[0]).strip()
                _params = ((new_input_data[1]).strip()).split(',')
                _params_list = [one for one in _params]
                _value = self.__get_utils(_method, py_module, _params_list)
                self.relations[request_key] = _value

            msg = f"[{mTime()}][{self._step_num}][otherUtils] after-->self.relations['{request_key}'] = {_value}"
            with allure.step(msg):
                logger.info(msg[14:])
            return "PASS", {request_key: _value}
        except Exception as e:
            msg = f"[{mTime()}][{self._step_num}][otherUtils]❌ The method incorrect,\n{e}"
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:]

    def readJsonFile(self, *args):
        """
        readJsonFile
        :param: add dict_key to self.relations
        :param: file path + file name
        :return: dict
        """
        try:
            request_key = str(tuple(args)[0]).strip()
            request_data = str(tuple(args)[1]).strip()
            msg = f"[{mTime()}][{self._step_num}][readJsonFile] before-->[*ARGS:{args}]"
            with allure.step(msg):
                logger.info(msg[14:])
            if ',' not in request_data:
                _path = self.__get_utils(request_data, py_module)
                _path = self.__get_relations(_path)
                with open(Path(_path), 'r', encoding='utf-8') as load_f:
                    load_dict = json.load(load_f)
                self.relations[request_key] = load_dict
                msg = f"[{mTime()}][{self._step_num}][readJsonFile] after-->self.relations[{request_key}] = {load_dict}"
                with allure.step(msg):
                    logger.info(msg[14:])
                return "PASS", {request_key: load_dict}
            else:
                new_input_data = request_data.split(',', 1)
                file_path_name = (new_input_data[0]).strip()
                jmespath_key = (new_input_data[1]).strip()
                if jmespath_key == '':
                    msg = f"[{mTime()}][{self._step_num}][readJsonFile]❌ If ',' in request_key, jmespath_key should not empty, please check it."
                    with allure.step(msg):
                        logger.error(msg[14:])
                    return "FAIL", msg[19:]

                _path = self.__get_utils(file_path_name, py_module)
                _path = self.__get_relations(_path)
                with open(Path(_path), 'r', encoding='utf-8') as load_f:
                    load_dict = json.load(load_f)
                search_value = jmespath.search(jmespath_key, load_dict)  # 检索不到返回 None
                if search_value is None:
                    msg = f"[{mTime()}][{self._step_num}]❌ WARNING jmespath.search({jmespath_key}) not found result in Json, search_value >> '{search_value}'"
                    with allure.step(msg):
                        logger.warning(msg[14:])
                    return "FAIL", msg[19:]
                else:
                    self.relations[request_key] = search_value
                    msg = f"[{mTime()}][{self._step_num}][readJsonFile] after-->self.relations[{request_key}] = {search_value}"
                    with allure.step(msg):
                        logger.info(msg[14:])
                    return "PASS", {request_key: search_value}
        except Exception as e:
            msg = f"[{mTime()}][{self._step_num}][readJsonFile]❌ The method incorrect, \n{e}"
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:]

    def __url(self, alias_url, url_path):
        new_url = ''
        if (url_path is not None) and (url_path.lower().startswith('http')):
            self._baseurl[alias_url] = url_path
            msg = f"[{mTime()}][{self._step_num}][{inspect.stack()[1][3]}.__url] Set URL self._baseurl[{alias_url}] = {url_path}"
            with allure.step(msg):
                logger.info(msg[14:])
            return url_path, ''
        else:
            if url_path != '' and url_path is not None:
                if not self._baseurl[alias_url].lower().startswith('http'):
                    msg = f"[{mTime()}][{self._step_num}]❌ The input URL '{url_path}' incorrect, should start 'http'"
                    with allure.step(msg):
                        logger.error(msg[14:])
                    return "FAIL", msg[19:]
                else:
                    if str(self._baseurl[alias_url])[-1:] == '/':
                        new_url = self._baseurl[alias_url] + url_path
                    else:
                        new_url = self._baseurl[alias_url] + '/' + url_path
            else:
                if not self._baseurl[alias_url].lower().startswith('http'):
                    msg = f"[{mTime()}][{self._step_num}]❌ The input URL '{url_path}' incorrect, should start 'http'"
                    with allure.step(msg):
                        logger.error(msg[14:])
                    return "FAIL", msg[19:]
            return new_url, ''

    def setheader(self, *args):
        """
        A requests session headers
        :param *args: alias required (excel mode)
        :return: self._session[alias].headers
        """
        request_key = str(tuple(args)[0]).strip()
        request_data = str(tuple(args)[1]).strip()
        msg = f"[{mTime()}][{self._step_num}][setheader] before-->[*ARGS:{args}]"
        with allure.step(msg):
            logger.info(msg[14:])
        if ',' not in request_key:
            msg = f"[{mTime()}][{self._step_num}][setheader]❌ The input requests_key ',' not found."
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:]
        else:
            new_input_data = request_key.split(',', 1)
            alias = (new_input_data[0]).strip()
            _key = (new_input_data[1]).strip()
            if _key == '':
                msg = f'[{mTime()}][{self._step_num}][setheader]❌ The input header key is empty, please check it.'
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:]
            try:
                _session = self._session[alias]
            except:
                msg = f"[{mTime()}][{self._step_num}][setheader]❌ The input alias '{alias}' incorrect, self._session = {self._session}"
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:]
            try:
                self._session[alias].headers[_key] = request_data
                msg = f"[{mTime()}][{self._step_num}][setheader] self._session[{alias}].headers[{_key}] = {request_data}"
                with allure.step(msg):
                    logger.info(msg[14:])
            except:
                msg = f"[{mTime()}][{self._step_num}][setheader]❌ The input self._session[{alias}].headers[{_key}] incorrect, please check it. self._session[{alias}].headers = {self._session[alias].headers}"
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:]
            return "PASS", self._session[alias].headers


    def setproxy(self, *args):
        """
        A requests session proxies
        :param *args: alias required (excel mode)
        :return: self._session[alias].proxies
        """
        request_key = str(tuple(args)[0]).strip()
        request_data = str(tuple(args)[1]).strip()
        msg = f"[{mTime()}][{self._step_num}][setproxy] before-->[*ARGS:{args}]"
        with allure.step(msg):
            logger.info(msg[14:])
        if ',' not in request_key:
            msg = f"[{mTime()}][{self._step_num}][setproxy]❌ The input requests_key ',' not found."
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:]
        else:
            new_input_data = request_key.split(',', 1)
            alias = (new_input_data[0]).strip()
            _key = (new_input_data[1]).strip()
            if _key == '':
                msg = f'[{mTime()}][{self._step_num}][setproxy]❌ The input proxy key is empty, please check it.'
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:]
            try:
                _session = self._session[alias]
            except:
                msg = f'[{mTime()}][{self._step_num}][setproxy]❌ The input alias "{alias}" incorrect, self._session = {self._session}'
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:]
            try:
                self._session[alias].proxies[_key] = request_data
                msg = f"[{mTime()}][{self._step_num}][setproxy] self._session[{alias}].proxies[{_key}] = {request_data}"
                with allure.step(msg):
                    logger.info(msg[14:])
            except:
                msg = f"[{mTime()}][{self._step_num}][setproxy]❌ The input self._session[{alias}].proxies[{_key}] incorrect, please check it. self._session[{alias}].proxies = {self._session[alias].proxies}"
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:]
            return "PASS", self._session[alias].proxies

    def session(self, *args):
        """
        create a requests session
        :param: alias
        :return: self._session
        """
        alias = str(tuple(args)[0]).strip()
        msg = f"[{mTime()}][{self._step_num}][session] before-->[*ARGS:{args}]"
        with allure.step(msg):
            logger.info(msg[14:])
        s = requests.Session()
        if alias == '':
            msg = f"[{mTime()}][{self._step_num}][session]❌ The 'request_key' is empty, please set session alias."
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:]
        else:
            self._session[alias] = s
            msg = f"[{mTime()}][{self._step_num}][session] self._session[{alias}] = {s}"
            with allure.step(msg):
                logger.info(msg[14:])
            return "PASS", self._session

    def get_api(self, *args, **kwargs):
        """
        for excel mode only (py mode prohibited use)
        :param *args: required (excel mode)
        :param **kwargs: required (py mode)
        :return: status_code/self.resp_json
        """
        msg = f"[{mTime()}][{self._step_num}][get_api] before-->[*ARGS:{args}][*KWARGS:{kwargs}]"
        with allure.step(msg):
            logger.info(msg[14:])
        input_data = (tuple(args)[0]).strip()
        if ',' not in input_data:
            msg = f"[{mTime()}][{self._step_num}][get_api]❌ No url/session alias in 'request_key', {input_data}, please check it."
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:], 'ERROR'
        else:
            new_input_data = input_data.split(',', 2)
            _len = len(new_input_data)
            if _len < 3:
                msg = f"[{mTime()}][{self._step_num}][get_api]❌ No enough url/session alias in 'request_key', {input_data}, please check it."
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:], 'ERROR'

            _alias_url = str(new_input_data[0]).strip()
            _alias_s = str(new_input_data[1]).strip()
            _key = str(new_input_data[2]).strip()
            try:
                _session = self._session[_alias_s]
            except:
                msg = f'[{mTime()}][{self._step_num}][get_api]❌ The input session alias "{_alias_s}" incorrect, please check it. self._session = {self._session}'
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:], 'ERROR'
            try:
                _url = self._baseurl[_alias_url]
            except:
                msg = f'[{mTime()}][{self._step_num}][get_api]❌ The input url alias "{_alias_url}" incorrect, please check it. self._baseurl = {self._baseurl}'
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:], 'ERROR'
        msg = f"[{mTime()}][{self._step_num}][get_api] after-->self._session[{_alias_s}] = {self._session[_alias_s]}"
        with allure.step(msg):
            logger.info(msg[14:])

        msg = f"[{mTime()}][{self._step_num}][get_api] after-->self._baseurl[{_alias_url}] = {self._baseurl[_alias_url]}"
        with allure.step(msg):
            logger.info(msg[14:])
        new_url, fail_msg = self.__url(_alias_url, _key)
        if new_url == 'FAIL':
            return new_url, fail_msg, 'ERROR'

        if '${' in new_url or '#{' in new_url:
            new_url = self.__get_utils(new_url, py_module)
            new_url = self.__get_relations(new_url)
        msg = f"[{mTime()}][{self._step_num}][get_api] after-->the full url >> {new_url}"
        with allure.step(msg):
            logger.info(msg[14:])

        request_data = str(tuple(args)[1])
        if request_data == '' or request_data == ' ':
            pass
        else:
            if '${' in request_data or '#{' in request_data:
                request_data = self.__get_utils(request_data, py_module)
                request_data = self.__get_relations(request_data)

            if (request_data.startswith('{') and request_data.endswith('}')) or \
                (request_data.startswith('[') and request_data.endswith(']')):
                try:
                    _dict = eval(request_data)
                    kwargs['params'] = _dict
                except Exception as e:
                    msg = f"[{mTime()}][{self._step_num}][get_api]❌ Convert to dict incorrect, string >> '{request_data}' \n{e}"
                    with allure.step(msg):
                        logger.error(msg[14:])
                    return "FAIL", msg[19:], 'ERROR'
            else:
                msg = f"[{mTime()}][{self._step_num}][get_api]❓ WARNING Please check string '{request_data}', should be dict/list ?"
                with allure.step(msg):
                    logger.warning(msg[14:])
                return "FAIL", msg[19:], 'ERROR'
        try:
            res = _session.get(new_url, **kwargs)
        except Exception as e:
            msg = f"[{mTime()}][{self._step_num}][get_api]❌ WARNING: {e}]"
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:], 'ERROR'
        else:
            try:
                resp = res.json()
                code = res.status_code
                msg = f"[{mTime()}][{self._step_num}][get_api] after-->[Response.status_code==>>{code}]"
                with allure.step(msg):
                    logger.info(msg[14:])
                msg2 = f"[{mTime()}][{self._step_num}][get_api] after-->[Response.json()==>>{resp}]"
                with allure.step(msg2):
                    logger.info(msg2[14:])
            except Exception as e:
                msg = f"[{mTime()}][{self._step_num}][get_api]❌ WARNING: {e}]"
                with allure.step(msg):
                    logger.warning(msg[14:])
                code = res.status_code
                resp = res.text
                msg1 = f"[{mTime()}][{self._step_num}][get_api] after-->[Response.status_code==>>{code}]"
                with allure.step(msg1):
                    logger.info(msg1[14:])
                msg2 = f"[{mTime()}][{self._step_num}][get_api] after-->[Response.text==>>\n{resp}]"
                with allure.step(msg2):
                    logger.info(msg2[14:])
                self._recent_resp_json = resp
                return "PASS", resp, code
            else:
                self._recent_resp_json = resp
                return "PASS", resp, code

    def post_api(self, *args, **kwargs):
        """
        for excel mode only (py mode prohibited use)
        :param *args: required (excel mode)
        :param **kwargs: required (py mode)
        :return: status_code/self.resp_json
        """
        msg = f"[{mTime()}][{self._step_num}][post_api] before-->[*ARGS:{args}][*KWARGS:{kwargs}]"
        with allure.step(msg):
            logger.info(msg[14:])
        input_data = (tuple(args)[0]).strip()
        if ',' not in input_data:
            msg = f"[{mTime()}][{self._step_num}][post_api]❌ No url/session alias in 'request_key', {input_data}, please check it."
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:], 'ERROR'
        else:
            new_input_data = input_data.split(',', 2)
            _len = len(new_input_data)
            if _len < 3:
                msg = f"[{mTime()}][{self._step_num}][post_api]❌ No enough url/session alias in 'request_key', {input_data}, please check it."
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:], 'ERROR'

            _alias_url = str(new_input_data[0]).strip()
            _alias_s = str(new_input_data[1]).strip()
            _key = str(new_input_data[2]).strip()
            try:
                _session = self._session[_alias_s]
            except:
                msg = f'[{mTime()}][{self._step_num}][post_api]❌ The input session alias "{_alias_s}" incorrect, please check it. self._session = {self._session}'
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:], 'ERROR'
            try:
                _url = self._baseurl[_alias_url]
            except:
                msg = f'[{mTime()}][{self._step_num}][post_api]❌ The input url alias "{_alias_url}" incorrect, please check it. self._baseurl = {self._baseurl}'
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:], 'ERROR'
        msg = f"[{mTime()}][{self._step_num}][post_api] after-->self._session[{_alias_s}] = {self._session[_alias_s]}"
        with allure.step(msg):
            logger.info(msg[14:])

        msg = f"[{mTime()}][{self._step_num}][post_api] after-->self._baseurl[{_alias_url}] = {self._baseurl[_alias_url]}"
        with allure.step(msg):
            logger.info(msg[14:])
        new_url, fail_msg = self.__url(_alias_url, _key)
        if new_url == 'FAIL':
            return new_url, fail_msg, 'ERROR'

        if '${' in new_url or '#{' in new_url:
            new_url = self.__get_utils(new_url, py_module)
            new_url = self.__get_relations(new_url)
        msg = f"[{mTime()}][{self._step_num}][post_api] after-->the full url >> {new_url}"
        with allure.step(msg):
            logger.info(msg[14:])

        request_data = str(tuple(args)[1])
        if request_data == '' or request_data == ' ':
            pass
        else:
            if '${' in request_data or '#{' in request_data:
                request_data = self.__get_utils(request_data, py_module)
                request_data = self.__get_relations(request_data)

            if (request_data.startswith('{') and request_data.endswith('}')) or \
                    (request_data.startswith('[') and request_data.endswith(']')):
                try:
                    _dict = eval(request_data)
                    kwargs['params'] = _dict
                except Exception as e:
                    msg = f"[{mTime()}][{self._step_num}][post_api]❌ Convert to dict incorrect, string >> '{request_data}' \n{e}"
                    with allure.step(msg):
                        logger.error(msg[14:])
                    return "FAIL", msg[19:], 'ERROR'
            else:
                msg = f"[{mTime()}][{self._step_num}][post_api]❓ WARNING Please check string '{request_data}', should be dict/list ?"
                with allure.step(msg):
                    logger.warning(msg[14:])
                return "FAIL", msg[19:], 'ERROR'
        try:
            res = _session.get(new_url, **kwargs)
        except Exception as e:
            msg = f"[{mTime()}][{self._step_num}][post_api]❌ WARNING: {e}]"
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:], 'ERROR'
        else:
            try:
                resp = res.json()
                code = res.status_code
                msg = f"[{mTime()}][{self._step_num}][post_api] after-->[Response.status_code==>>{code}]"
                with allure.step(msg):
                    logger.error(msg[14:])
                msg2 = f"[{mTime()}][{self._step_num}][post_api] after-->[Response.json()==>>{resp}]"
                with allure.step(msg2):
                    logger.error(msg2[14:])
            except Exception as e:
                msg = f"[{mTime()}][{self._step_num}][post_api]❌ WARNING: {e}]"
                with allure.step(msg):
                    logger.error(msg[14:])
                code = res.status_code
                resp = res.text
                msg1 = f"[{mTime()}][{self._step_num}][post_api] after-->[Response.status_code==>>{code}]"
                with allure.step(msg1):
                    logger.info(msg1[14:])
                msg2 = f"[{mTime()}][{self._step_num}][post_api] after-->[Response.text==>>\n{resp}]"
                with allure.step(msg2):
                    logger.info(msg2[14:])
                self._recent_resp_json = resp
                return "PASS", resp, code
            else:
                self._recent_resp_json = resp
                return "PASS", resp, code

    def save2dict(self, *args):
        """
        for get_api/post_api params/data/json (if py mode, json={'p': 'p1'})
        if tuple(args)[0] == '', tuple(args)[1] required dict
        if tuple(args)[0] != '', tuple(args)[1] any
        :param *args: required (excel mode)
        :return: dict/self._json
        """
        _dict = {}
        input_data = (tuple(args)[0]).strip()
        request_data = str(tuple(args)[1])
        msg = f"[{mTime()}][{self._step_num}][save2dict] before-->[*ARGS:{args}]"
        with allure.step(msg):
            logger.info(msg[14:])

        if input_data == '':
            msg = f"[{mTime()}][{self._step_num}][save2dict]❌ The input 'request_key' is empty, please check it."
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:]
        else:
            _value = self.__get_utils(request_data, py_module)
            _valuen = self.__get_relations(_value)

            if _valuen.lstrip().startswith('='):
                logger.info(type(_valuen))
                self.relations[input_data] = _valuen[1:]
                msg = f'[{mTime()}][{self._step_num}][save2dict] after-->self.relations[{input_data}] = \"{_valuen[1:]}\"'
                with allure.step(msg):
                    logger.info(msg[14:])
                return "PASS", {input_data: _valuen[1:]}
            else:
                try:
                    _dict = eval(_valuen)
                    logger.info(type(_dict))
                except Exception as e:
                    msg = f"[{mTime()}][{self._step_num}][save2dict]❌ Convert to dict error.\n{e}"
                    with allure.step(msg):
                        logger.error(msg[14:])
                    return "FAIL", msg[19:]
                self.relations[input_data] = _dict
                msg = f"[{mTime()}][{self._step_num}][save2dict] after-->self.relations[{input_data}] = {_dict}"
                with allure.step(msg):
                    logger.info(msg[14:])
                return "PASS", {input_data: _dict}

    def resp2dict(self, *args):
        """
        get vlaue from self.resp_json to self.relations[self._sheet_name][key]=value
        1. from self.resp_json['a']['b'] to self.relations[self._sheet_name]['xcode']=10001
        2. to self.relations[self._sheet_name]['xcode']=10001 if args contains '=' e.g. =10001
        """
        _dict = {}
        try:
            input_data = (tuple(args)[0]).strip()
            request_data = str(tuple(args)[1]).strip()
            msg = f"[{mTime()}][{self._step_num}][resp2dict] before-->[*ARGS:{args}]"
            with allure.step(msg):
                logger.info(msg[14:])
            if input_data == '':
                msg = f"[{mTime()}][{self._step_num}][resp2dict]❌ The 'request_key' should not be empty."
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:]
            if ',' not in input_data:  # recent response of xx_api
                if request_data == '':
                    msg = f"[{mTime()}][{self._step_num}][resp2dict] after-->self.relations[{input_data}] = {self._recent_resp_json}"
                    with allure.step(msg):
                        logger.info(msg[14:])
                    self.relations[input_data] = self._recent_resp_json
                    return "PASS", {input_data: self._recent_resp_json}
                else:
                    search_value = jmespath.search(request_data, self._recent_resp_json)  # 检索不到返回 None
                    if search_value is None:
                        msg = f"[{mTime()}][{self._step_num}][resp2dict]❌ jmespath.search({request_data}, self._recent_resp_json) = {search_value}"
                        with allure.step(msg):
                            logger.error(msg[14:])
                        return "FAIL", msg[19:]
                    msg = f"[{mTime()}][{self._step_num}][resp2dict] after-->self.relations[{input_data}] = {search_value}"
                    with allure.step(msg):
                        logger.info(msg[14:])
                    self.relations[input_data] = search_value
                    return "PASS", {input_data: search_value}

            else:  # ',' alias
                new_input_data = input_data.split(',')
                _alias = str(new_input_data[0]).strip()
                _alias_key = str(new_input_data[1]).strip()

                try:
                    get_resp = self.relations[_alias]
                except Exception as e:
                    msg = f"[{mTime()}][{self._step_num}][resp2dict]❌ The input key '{_alias}' not found in self.relations = {self.relations}"
                    with allure.step(msg):
                        logger.error(msg[14:])
                    return "FAIL", msg[19:]
                if _alias_key == '':
                    msg = f"[{mTime()}][{self._step_num}][resp2dict]❌ The relations key 'self.relations[]' should not be empty."
                    with allure.step(msg):
                        logger.error(msg[14:])
                    return "FAIL", msg[19:]
                search_value = jmespath.search(request_data, get_resp)  # 检索不到返回 None
                if search_value is None:
                    msg = f"[{mTime()}][{self._step_num}][resp2dict]❌ jmespath.search({request_data}, self.relations[{_alias}]) = {search_value}"
                    with allure.step(msg):
                        logger.error(msg[14:])
                    return "FAIL", msg[19:]
                msg = f"[{mTime()}][{self._step_num}][resp2dict] after-->self.relations[{request_data}] = {search_value}"
                with allure.step(msg):
                    logger.info(msg[14:])
                self.relations[_alias_key] = search_value
                return "PASS", {_alias_key: search_value}

        except Exception as e:
            msg = f"[{mTime()}][{self._step_num}][resp2json]❌ Convert dict error.\n{e}"
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:]



    def put_api(self):
        pass
    def delete_api(self):
        pass

    def __get_relations(self, param):
        pattern = r'[$][{](.*?)[}]'
        if param is None or param == '':
            return ''
        else:
            for key in self.relations.keys():
                res = re.findall(pattern, param)
                if res:
                    for r in res:
                        if r == key:
                            msg = f"[{mTime()}][{self._step_num}][{inspect.stack()[1][3]}.__get_relations]-----Data preprocessing before, self.__get_relations(param) >> {param}"
                            param = param.replace('${' + key + '}', str(self.relations[key]))

                            msg2 = f"[{mTime()}][{self._step_num}][{inspect.stack()[1][3]}.__get_relations]-----Data preprocessing after, self.__get_relations(param) >> {param}"
                            with allure.step(msg):
                                logger.info(msg[14:])
                            with allure.step(msg2):
                                logger.info(msg2[14:])
            return param


    # def assertInJson(self, *args):
    #     """
    #     get value through jsonpath(self.resp_json, f'$..{json_path}')
    #     WARNING: get jsonpath value maybe not unipue
    #     :param json_path:
    #     :param expect_value:
    #     """
    #     input_data = (tuple(args)[0]).strip()
    #     request_data = tuple(args)[1]
    #     allure_step(f"[{mTime()}][{self._step_num}][assertInJson] before--> self.resp_json==>>{self.resp_json}")
    #     allure_step(f"[{mTime()}][{self._step_num}][assertInJson] before--> request_data(expect)==>>{request_data}")
    #     res = jsonpath.jsonpath(self.resp_json, f'$..{input_data}')  # 找不到是结果是 False
    #     if res is None:
    #         allure_step(f"[{mTime()}][{self._step_num}]WARNING jsonpath-->>f'$..{input_data}'==>>{res}==>>{type(res)}")
    #     allure_step(f"[{mTime()}][{self._step_num}][assertInJson] ACTUAL_VALUE:[{res}]")
    #     allure_step(f"[{mTime()}][{self._step_num}][assertInJson] EXPECT_VALUE:[{request_data}]")
    #     try:
    #         if isinstance(res, list) and len(res) == 1:
    #             assert request_data == res[0]
    #         elif isinstance(res, list) and len(res) > 1:
    #             assert request_data in res
    #         else:
    #             assert request_data == str(res)
    #     except AssertionError as e:
    #         msg = f"[{mTime()}][{self._step_num}][assertInJson]❌ FAIL"
    #         allure_step_error(msg)
    #         return "FAIL", f'ACTUAL_VALUE :[{res}]' + f'<>EXPECT_VALUE :[{request_data}]'
    #     else:
    #         allure_step(f"[{mTime()}][{self._step_num}][assertInJson] PASS")
    #         return 'PASS', f'ACTUAL_VALUE :{res}' + f'<>EXPECT_VALUE :{request_data}'
    def __resp_assert(self, expect_json):
        if expect_json.strip().startswith('{') or expect_json.strip().startswith('['):
            _value = expect_json.strip()
            _value = self.__get_utils(_value, py_module)
            _valuen = self.__get_relations(_value)
            try:
                _dict = eval(str(_valuen))
            except Exception as e:
                msg = f"[{mTime()}][{self._step_num}][assertResp2Json]❌ after--> convert request_data to dict error.{expect_json} \n{e}"
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:]
            return _dict
        else:
            _value = self.__get_utils(expect_json.strip(), py_module)
            _valuen = self.__get_relations(_value)
            return _valuen

    def assert_resp_json(self, *args):
        """
        match dict/str from self.resp_json to compare
        self.resp_json = {"a": [{"b": "b1"}, {"c": "c1"}]}
        assertMatch2Json(self, 'a[0]', '{"b": "b1"}')
        doc: https://jmespath.org/
        :param part_path: get value from self.resp_json[part_path]
        :param expect_value: dict/str
        """
        part_path = str(tuple(args)[0]).strip()
        expect_json = str(tuple(args)[1]).strip()
        msg = f"[{mTime()}][{self._step_num}][assert_resp_json] before-->[*ARGS:{args}]"
        with allure.step(msg):
            logger.info(msg[14:])
        msg = f"[{mTime()}][{self._step_num}][assert_resp_json] before-->self._recent_resp_json = {self._recent_resp_json}"
        with allure.step(msg):
            logger.info(msg[14:])

        if part_path == '':
            if (expect_json.startswith('{') and expect_json.endswith('}')) or \
                (expect_json.startswith('[') and expect_json.endswith(']')):
                _value = self.__get_utils(expect_json, py_module)
                _valuen = self.__get_relations(_value)
                try:
                    _dict = eval(_valuen)
                except Exception as e:
                    msg = f"[{mTime()}][{self._step_num}][assert_resp_json]❌ Convert 'request_data' to dict incorrect, string >> '{_valuen}' \n{e}"
                    with allure.step(msg):
                        logger.error(msg[14:])
                    return "FAIL", msg[19:], 'ERROR'
            else:
                msg = f"[{mTime()}][{self._step_num}][assert_resp_json]❓ WARNING Please check string '{expect_json}', should be dict/list ?"
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:], 'ERROR'

            msg = f"[{mTime()}][{self._step_num}][assert_resp_json] ACTUAL_VALUE:[{self._recent_resp_json}]"
            with allure.step(msg):
                logger.info(msg[14:])
            msg = f"[{mTime()}][{self._step_num}][assert_resp_json] EXPECT_VALUE:[{_dict}]"
            with allure.step(msg):
                logger.info(msg[14:])
            error_count = HandleJson().json_assert(self._recent_resp_json, _dict)
            try:
                assert error_count == 0
            except AssertionError as e:
                msg = f"[{mTime()}][{self._step_num}][assert_resp_json]❌ FAIL {e}"
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", f'ACTUAL_VALUE :{self._recent_resp_json}' + f'<>EXPECT_VALUE :{_dict}'
            else:
                msg = f"[{mTime()}][{self._step_num}][assert_resp_json] PASS"
                with allure.step(msg):
                    logger.info(msg[14:])
                return 'PASS', f'ACTUAL_VALUE :{self._recent_resp_json}' + f'<>EXPECT_VALUE :{_dict}'
        else:
            search_value = jmespath.search(part_path, self._recent_resp_json)  # 检索不到返回 None
            if search_value is None:
                msg = f"[{mTime()}][{self._step_num}]❌ WARNING jmespath.search({part_path}, self._recent_resp_json)==>>{search_value}"
                with allure.step(msg):
                    logger.error(msg[14:])
            msg = f"[{mTime()}][{self._step_num}][assert_resp_json] after-->jmespath.search({part_path}, self._recent_resp_json)==>>{search_value}"
            with allure.step(msg):
                logger.info(msg[14:])
            # _expect = self.__resp_assert(expect_json)
            if (expect_json.startswith('{') and expect_json.endswith('}')) or \
                (expect_json.startswith('[') and expect_json.endswith(']')):
                _value = self.__get_utils(expect_json, py_module)
                _valuen = self.__get_relations(_value)
                try:
                    _dict = eval(_valuen)
                except Exception as e:
                    msg = f"[{mTime()}][{self._step_num}][assert_resp_json]❌ Convert request_data to dict incorrect, string >> '{_valuen}' \n{e}"
                    with allure.step(msg):
                        logger.error(msg[14:])
                    return "FAIL", msg[19:], 'ERROR'
            else:
                msg = f"[{mTime()}][{self._step_num}][assert_resp_json]❓ WARNING Please check string '{expect_json}', should be dict/list ?"
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:], 'ERROR'
            try:
                _search_value = eval(str(search_value))
            except Exception as e:
                msg = f"[{mTime()}][{self._step_num}][assert_resp_json]❌ Convert search_value to dict incorrect, string >> '{str(search_value)}' \n{e}"
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", msg[19:], 'ERROR'
            error_count = HandleJson().json_assert(search_value, _dict)

            msg = f"[{mTime()}][{self._step_num}][assert_resp_json] ACTUAL_VALUE:[{search_value}]"
            with allure.step(msg):
                logger.info(msg[14:])
            msg = f"[{mTime()}][{self._step_num}][assert_resp_json] EXPECT_VALUE:[{_dict}]"
            with allure.step(msg):
                logger.info(msg[14:])
            try:
                assert error_count == 0
            except AssertionError as e:
                msg = f"[{mTime()}][{self._step_num}][assert_resp_json]❌ FAIL {e}"
                with allure.step(msg):
                    logger.error(msg[14:])
                return "FAIL", f'ACTUAL_VALUE :{search_value}' + f'<>EXPECT_VALUE :{_dict}'
            else:
                msg = f"[{mTime()}][{self._step_num}][assert_resp_json] PASS"
                with allure.step(msg):
                    logger.info(msg[14:])
                return 'PASS', f'ACTUAL_VALUE :{search_value}' + f'<>EXPECT_VALUE :{_dict}'



    # def resp(self, *args):
    #     input_data = str(tuple(args)[0]).strip()
    #     if input_data == '':
    #         msg = f'[{mTime()}]❌ Save response alias is empty, please check it.'
    #         allure_step_error(msg)
    #         return "FAIL", msg[14:]
    #     else:
    #         try:
    #             self.relations[self._sheet_name][self.__random_s]
    #         except Exception as e:
    #             self.relations[self._sheet_name][self.__random_s] = {}
    #         finally:
    #             try:
    #                 self.relations[self._sheet_name][self.__random_s][input_data]
    #             except Exception as e2:
    #                 self.relations[self._sheet_name][self.__random_s][input_data] = {}
    #             finally:
    #                 msg1 = f'[{mTime()}] Create self.relations[{self._sheet_name}][{self.__random_s}][{input_data}]'
    #                 allure_step(msg1)
    #                 self.relations[self._sheet_name][self.__random_s][input_data] = self.resp_json_alias[self.__random_s]
    #         msg = f'[{mTime()}] Save response >> self.relations[{self._sheet_name}][{self.__random_s}][{input_data}] = {self.resp_json_alias[self.__random_s]}'
    #         allure_step(msg)
    #         return "PASS", {self.__random_s: {input_data: self.resp_json_alias[self.__random_s]}}

    def assert2json(self, *args):
        """
        match dict/str from self.resp_json to compare
        self.resp_json = {"a": [{"b": "b1"}, {"c": "c1"}]}
        assertMatch2Json(self, 'a[0]', '{"b": "b1"}')
        doc: https://jmespath.org/
        :param part_path: get value from self.resp_json[part_path]
        :param expect_value: dict/str
        """
        json_name = str(tuple(args)[0]).strip()
        part_path = str(tuple(args)[1]).strip()
        if '=' not in json_name:
            msg = f"[{mTime()}][{self._step_num}]❌ request_key not found '=', please check it."
            with allure.step(msg):
                logger.error(msg[14:])
            return "FAIL", msg[19:]
        else:
            expect_json_name = json_name.split('=')
            one_json_name = (expect_json_name[0]).strip()
            two_json_name = (expect_json_name[1]).strip()

            try:
                one_json = self.relations[self._sheet_name][self.__random_s][one_json_name]
                logger.error(111)
                logger.error(one_json)
            except Exception as e:
                logger.error(222)
                msg = f'[{mTime()}] WARNING self.relations[{self._sheet_name}][{self.__random_s}][{one_json_name}] not found.'
                with allure.step(msg):
                    logger.error(msg[14:])
                one_json = self.__get_relations(one_json_name)
                if isinstance(one_json, dict):
                    logger.info('dict')
                    logger.info(type(one_json))
                else:
                    aa = eval(one_json)
                    logger.info(type(aa))
                # search_value_one = jmespath.search(part_path, resp_one)



            else:
                pass
            # try:
            #     resp_two = self.relations[self.__random_s][two_json_name]
            # except Exception as e:
            #     msg = f'[{mTime()}]❌ resp_two self.relations[{self.__random_s}][{two_json_name}] incorrect, please check it. self.relations[{self.__random_s}] >>{self.relations[self.__random_s]}'
            #     allure_step_error(msg)
            #     return "FAIL", msg
            # if part_path == '':
            #     error_count = HandleJson().json_assert(resp_one, resp_two)
            #     allure_step(f"[{mTime()}][{self._step_num}][assert2resp] ACTUAL_VALUE resp_one==>>{resp_one}")
            #     allure_step(f"[{mTime()}][{self._step_num}][assert2resp] EXPECT_VALUE resp_two==>>{resp_two}")
            #     try:
            #         assert error_count == 0
            #     except AssertionError as e:
            #         msg = f"[{mTime()}][{self._step_num}][assertMatch2Json]❌ FAIL"
            #         allure_step_error(msg)
            #         return "FAIL", f'ACTUAL_VALUE :{resp_one}' + f'<>EXPECT_VALUE :{resp_two}'
            #     else:
            #         allure_step(f"[{mTime()}][{self._step_num}][assertMatch2Json] PASS")
            #         return 'PASS', f'ACTUAL_VALUE :{resp_one}' + f'<>EXPECT_VALUE :{resp_two}'
            # else:
            #     if '=' not in part_path:
            #         search_value_one = jmespath.search(part_path, resp_one)  # 检索不到返回 None
            #         if search_value_one is None:
            #             allure_step(f"[{mTime()}][{self._step_num}]❌ WARNING resp_one jmespath.search-->>f'{part_path}'==>>{search_value_one}")
            #         search_value_two = jmespath.search(part_path, resp_two)  # 检索不到返回 None
            #         if search_value_two is None:
            #             allure_step(f"[{mTime()}][{self._step_num}]❌ WARNING resp_two jmespath.search-->>f'{part_path}'==>>{search_value_two}")
            #         error_count = HandleJson().json_assert(resp_one, resp_two)
            #         allure_step(f"[{mTime()}][{self._step_num}][assert2resp] ACTUAL_VALUE resp_one==>>{search_value_one}")
            #         allure_step(f"[{mTime()}][{self._step_num}][assert2resp] EXPECT_VALUE resp_two==>>{search_value_two}")
            #         try:
            #             assert error_count == 0
            #         except AssertionError as e:
            #             msg = f"[{mTime()}][{self._step_num}][assertMatch2Json]❌ FAIL"
            #             allure_step_error(msg)
            #             return "FAIL", f'ACTUAL_VALUE :{search_value_one}' + f'<>EXPECT_VALUE :{search_value_two}'
            #         else:
            #             allure_step(f"[{mTime()}][{self._step_num}][assertMatch2Json] PASS")
            #             return 'PASS', f'ACTUAL_VALUE :{search_value_one}' + f'<>EXPECT_VALUE :{search_value_two}'
            #     else:
            #         _part_path_key = part_path.split('=')
            #         one_path = (_part_path_key[0]).strip()
            #         two_path = (_part_path_key[1]).strip()
            #         search_value_one = jmespath.search(one_path, resp_one)  # 检索不到返回 None
            #         if search_value_one is None:
            #             allure_step(f"[{mTime()}][{self._step_num}]❌ WARNING resp_one jmespath.search-->>f'{one_path}'==>>{search_value_one}")
            #         else:
            #             allure_step(f"[{mTime()}][{self._step_num}] resp_one jmespath.search-->>f'{one_path}'==>>{search_value_one}")
            #
            #         search_value_two = jmespath.search(two_path, resp_two)  # 检索不到返回 None
            #         if search_value_two is None:
            #             allure_step(f"[{mTime()}][{self._step_num}]❌ WARNING resp_two jmespath.search-->>f'{two_path}'==>>{search_value_two}")
            #         else:
            #             allure_step(f"[{mTime()}][{self._step_num}] resp_two jmespath.search-->>f'{two_path}'==>>{search_value_two}")
            #         if search_value_one is not None and search_value_two is not None:
            #             error_count = HandleJson().json_assert(search_value_one, search_value_two)
            #             allure_step(f"[{mTime()}][{self._step_num}][assert2resp] ACTUAL_VALUE resp_one==>>{search_value_one}")
            #             allure_step(f"[{mTime()}][{self._step_num}][assert2resp] EXPECT_VALUE resp_two==>>{search_value_two}")
            #             try:
            #                 assert error_count == 0
            #             except AssertionError as e:
            #                 msg = f"[{mTime()}][{self._step_num}][assert2resp]❌ FAIL"
            #                 allure_step_error(msg)
            #                 return "FAIL", f'ACTUAL_VALUE :{search_value_one}' + f'<>EXPECT_VALUE :{search_value_two}'
            #             else:
            #                 allure_step(f"[{mTime()}][{self._step_num}][assertMatch2Json] PASS")
            #                 return 'PASS', f'ACTUAL_VALUE :{search_value_one}' + f'<>EXPECT_VALUE :{search_value_two}'
            #         else:
            #             msg = f"[{mTime()}][{self._step_num}][assert2resp]❌ FAIL"
            #             logger.error(msg)
            #             logger.error(f'ACTUAL_VALUE :{search_value_one}' + f'<>EXPECT_VALUE :{search_value_two}')
            #             return "FAIL", f'ACTUAL_VALUE :{search_value_one}' + f'<>EXPECT_VALUE :{search_value_two}'

if __name__ == '__main__':
    pass
