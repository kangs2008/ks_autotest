import json, sys
import re
import allure
import jsonpath
import requests
from Common.utils import mTime
from Common.handle_logger import logger
from Common.handle_json import HandleJson
import jmespath
import random
# from Common.handle_faker import RandomData
import Common.utils as utils
from pathlib import Path


py_module = [utils]

class Http(object):

    def __init__(self):
        self.baseurl = ''
        self.resp_json = {}
        self.resp_json_alias = {}
        self.relations = {}
        self._json = {}
        self.proxy = {}
        self._session = {}
        self.step_num = 0
        self.__random_s = None

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
                            _dict[one] =f'The function "{_method}" not found in {one}'
                        else:
                            func = getattr(one, _method, '_method not found')
                            param = param.replace('#{' + _method + '}', func(*args))
                            allure_step(f"[{mTime()}][{self.step_num}]--<__get_utils>--------数据预处理after:--_method:{_method}>>{param}")
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
            allure_step(f"[{mTime()}][{self.step_num}][otherUtils] before-->[*ARGS:{args}]")
            if ',' not in request_key:
                _value = self.__get_utils(request_data, py_module)
                self.relations[request_key] = _value
            else:
                new_input_data = request_data.split(',', 1)
                _method = (new_input_data[0]).strip()
                _params = ((new_input_data[1]).strip()).split(',')
                _params_list = [one for one in _params]
                _value = self.__get_utils(_method, py_module, _params_list)
                self.relations[request_key] = _value

            allure_step(f"[{mTime()}][{self.step_num}][otherUtils] after-->self.relations['{request_key}']={_value}")
            allure_step(f"[{mTime()}][{self.step_num}][otherUtils] method return value:[" + '{\'' + f"{request_key}" + "\':\'" + f"{_value}" + '\'}' + "]")
            return "PASS", '{\'' + f"{request_key}" + "\':\'" + f"{_value}" + '\'}'
        except Exception as e:
            msg = f"[{mTime()}][{self.step_num}][otherUtils]❌ incorrect\n{e}"
            allure_step_error(msg)
            return "FAIL", msg[14:]

    def readJsonFile(self, *args):
        """
        readJsonFile
        :param: add dict_key to self.relations
        :param: file path + file name
        :return: dict
        """
        try:
            _key = str(tuple(args)[0]).strip()
            file_path_name = str(tuple(args)[1]).strip()
            _path = self.__get_utils(file_path_name, py_module)
            _path = self.__get_relations(_path)
            with open(Path(_path), 'r', encoding='utf-8') as load_f:
                load_dict = json.load(load_f)
            self.relations[_key] = load_dict
            allure_step(f"[{mTime()}][{self.step_num}][readJsonFile] after-->self.relations['{_key}']={load_dict}")
            allure_step(
                f"[{mTime()}][{self.step_num}][readJsonFile] method return value:{self.relations[_key]}")
            return "PASS", self.relations[_key]
        except Exception as e:
            msg = f"[{mTime()}][{self.step_num}][readJsonFile]❌ incorrect\n{e}"
            allure_step_error(msg)
            return "FAIL", msg[14:]

    def create_session(self, *args):
        """
        create a requests session
        :param: alias
        :return: self._session
        """
        alias = (tuple(args)[0]).strip()
        s = requests.Session()
        if alias == '':
            # msg = f"[{mTime()}][{self.step_num}][create_session]❌ before-->The input parameter does not empty"
            # allure_step_error(msg)
            # return "FAIL", msg[14:]
            self.__random_s = 'alias' + str(random.randint(1000, 9999))
            self._session[self.__random_s] = s
            allure_step(f"[{mTime()}][{self.step_num}][create_session] self._session[{self.__random_s}] == {s}")
        else:
            self._session[alias] = s
            allure_step(f"[{mTime()}][{self.step_num}][create_session] self._session[{alias}] == {s}")

        # allure_step(f"[{mTime()}][{self.step_num}][create_session] method return value:[{self._session}]")
        return "PASS", self._session

    def __get_alais_url(self, args):
        input_data = (tuple(args)[0]).strip()
        if ',' not in input_data:
            _session = self._session[self.__random_s]
            url = input_data
            allure_step(f"[{mTime()}][{self.step_num}][create_session] self._session[{self.__random_s}]")
        else:
            new_input_data = input_data.split(',', 1)
            alais = (new_input_data[0]).strip()
            url = (new_input_data[1]).strip()
            try:
                _session = self._session[alais]
            except:
                msg = f'[{mTime()}]❌ The input alais "{alais}" incorrect, please check it. self._session{self._session}'
                allure_step_error(msg)
                return "FAIL", msg[14:]
            else:
                allure_step(f"[{mTime()}][{self.step_num}] self._session[{alais}]")
        return _session, url, alais

    def __url(self, url_path):
        new_url = ''
        if (url_path is not None) and (url_path.startswith('http')):
            self.baseurl = url_path
            return self.baseurl
        else:
            if url_path != '' and url_path is not None:
                if not self.baseurl.startswith('http'):
                    msg = f"[{mTime()}][{self.step_num}]❌ The input URL '{url_path}' incorrect."
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
                else:
                    if str(self.baseurl)[-1:] == '/':
                        new_url = self.baseurl + url_path
                    else:
                        new_url = self.baseurl + '/' + url_path
            else:
                if not self.baseurl.startswith('http'):
                    msg = f"[{mTime()}][{self.step_num}]❌ The input URL '{url_path}' incorrect."
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
        return new_url

    def setheader(self, *args):
        """
        A requests session headers
        :param *args: alias required (excel mode)
        :return: self._session[alias].headers
        """
        try:
            request_key = str(tuple(args)[0]).strip()
            request_data = str(tuple(args)[1]).strip()
            if ',' not in request_key:
                self._session[self.__random_s].headers[request_key] = request_data
                allure_step(f"[{mTime()}][{self.step_num}][setheader] method return alias '{self._session[self.__random_s].headers}'")
                return "PASS", self._session[self.__random_s].headers
            else:
                new_input_data = request_key.split(',', 1)
                alias = (new_input_data[0]).strip()
                _key = (new_input_data[1]).strip()
                try:
                    self._session[alias].headers[_key] = request_data
                    allure_step(f"[{mTime()}][{self.step_num}][setheader]-->self._session[{alias}].headers[{_key}]==>>{request_data}")
                except:
                    msg = f"[{mTime()}][{self.step_num}][setheader]❌ The input session alias '{alias}' incorrect, please check it. self._session{self._session}"
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
                # allure_step(f"[{mTime()}][setheader] method return alias '{self._session[alias].headers}'")
                return "PASS", self._session[alias].headers
        except Exception as e:
            msg = f"[{mTime()}][{self.step_num}][setheader]❌ -->self.session.headers incorrect"
            allure_step_error(msg)
            return "FAIL", msg[14:]

    def setproxy(self, *args):
        """
        A requests session proxies
        :param *args: alias required (excel mode)
        :return: self._session[alias].proxies
        """
        try:
            request_key = str(tuple(args)[0]).strip()
            request_data = str(tuple(args)[1]).strip()
            if ',' not in request_key:
                # msg = f'[{mTime()}][setproxy]❌ No session alias, please check it.'
                # allure_step_error(msg)
                # return "FAIL", msg[14:]
                self._session[self.__random_s].proxies[request_key] = request_data
                allure_step(f"[{mTime()}][{self.step_num}][setheader] method return alias '{self._session[self.__random_s].headers}'")
                return "PASS", self._session[self.__random_s].proxies
            else:
                new_input_data = request_key.split(',', 1)
                alias = (new_input_data[0]).strip()
                _key = (new_input_data[1]).strip()
                try:
                    self._session[alias].proxies[_key] = request_data
                    allure_step(f"[{mTime()}][{self.step_num}][setproxy]-->self._session[{alias}].proxies[{_key}]==>>{request_data}")
                except:
                    msg = f"[{mTime()}][{self.step_num}][setproxy]❌ The input session alias '{alias}' incorrect, please check it. self._session{self._session}"
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
                # allure_step(f"[{mTime()}][setproxy] method return alias '{self._session[alias].proxies}'")
                return "PASS", self._session[alias].proxies

        except Exception as e:
            msg = f"[{mTime()}][{self.step_num}][setproxy]❌ -->self.session.proxies incorrect"
            allure_step_error(msg)
            return "FAIL", msg[14:]

    def seturl(self, *args):
        request_key = str(tuple(args)[0]).strip()
        if (request_key is not None) and (request_key.startswith('http')):
            self.baseurl = request_key
            allure_step(f"[{mTime()}][{self.step_num}][seturl]-->{self.baseurl}")
        else:
            msg = f"[{mTime()}][{self.step_num}][seturl]❌ -->The input URl {self.baseurl} incorrect."
            allure_step_error(msg)
            return "FAIL", msg[14:]
        allure_step(f"[{mTime()}][{self.step_num}][seturl] method return value:{self.baseurl}")
        return "PASS", self.baseurl

    def get_api(self, *args, **kwargs):
        """
        for excel mode only (py mode prohibited use)
        :param *args: required (excel mode)
        :param **kwargs: required (py mode)
        :return: status_code/self.resp_json
        """
        __session, url, alais = self.__get_alais_url(args)
        new_url = self.__url(url)
        if '${' in new_url or '#{' in new_url:
            new_url = self.__get_utils(new_url, py_module)
            new_url = self.__get_relations(new_url)
        allure_step(f"[{mTime()}][{self.step_num}][get_api] before-->[URL:{new_url}],[*ARGS:{args}],[**KWARGS:{kwargs}]")
        allure_step(f"[{mTime()}][{self.step_num}][get_api] before-->__session[{__session}]")
        if self._json:
            kwargs['params'] = self._json
            allure_step(f"[{mTime()}][{self.step_num}][get_api] before-->kwargs[params]<==>self._json==>>[{self._json}]")
        kwargs['timeout'] = 1
        try:
            res = __session.get(new_url, **kwargs)
        except Exception as e:
            allure_step_error(f"[{mTime()}][{self.step_num}][get_api]❌ WARNING: {e}]")
            self._json = {}
            self.resp_json = {}
            return "FAIL", e, 'ERROR'
        else:
            try:
                resp = res.json()
                code = res.status_code
                allure_step(f"[{mTime()}][{self.step_num}][get_api] after-->[Response.status_code==>>{code}]")
                allure_step(f"[{mTime()}][{self.step_num}][get_api] after-->[Response.json()==>>{resp}]")
            except Exception as msg:
                allure_step_error(f"[{mTime()}][{self.step_num}][get_api]❌ WARNING: {msg}]")
                code = res.status_code
                resp = res.text
                self.resp_json_alias[alais] = resp
                allure_step(f"[{mTime()}][{self.step_num}][get_api] after-->[Response.status_code==>>{code}]")
                allure_step(f"[{mTime()}][{self.step_num}][get_api] after-->[Response.text==>>\n{resp}]")
                return "PASS", resp, code
            else:
                self._json = {}
                self.resp_json = resp
                self.resp_json_alias[alais] = self.resp_json
                allure_step(f"[{mTime()}][{self.step_num}][get_api] method return alias:[{code}/{resp}]")
                return "PASS", resp, code

    def post_api(self, *args, **kwargs):
        """
        for excel mode only (py mode prohibited use)
        :param *args: required (excel mode)
        :param **kwargs: required (py mode)
        :return: status_code/self.resp_json
        """
        __session, url, alais = self.__get_alais_url(args)
        new_url = self.__url(url)
        if '${' in new_url or '#{' in new_url:
            new_url = self.__get_utils(new_url, py_module)
            new_url = self.__get_relations(new_url)
        allure_step(f"[{mTime()}][{self.step_num}][post_api] before-->[URL:{new_url}],[*ARGS:{args}],[**KWARGS:{kwargs}]")
        allure_step(f"[{mTime()}][{self.step_num}][post_api] before-->__session[{__session}]")
        if self._json:
            kwargs['json'] = self._json
            allure_step(f"[{mTime()}][{self.step_num}][post_api] before-->kwargs[json]<==>self._json==>>[{self._json}]")
        kwargs['timeout'] = 2
        try:
            res = __session.post(new_url, **kwargs)
        except Exception as e:
            allure_step_error(f"[{mTime()}][{self.step_num}][post_api]❌ WARNING: {e}]")
            self._json = {}
            self.resp_json = {}
            return "FAIL", e, 'ERROR'
        else:
            try:
                resp = res.json()
                code = res.status_code
                allure_step(f"[{mTime()}][{self.step_num}][post_api] after-->[Response.status_code==>>{code}]")
                allure_step(f"[{mTime()}][{self.step_num}][post_api] after-->[Response.json()==>>{resp}]")
            except Exception as msg:
                allure_step_error(f"[{mTime()}][{self.step_num}][post_api]❌ WARNING: {msg}]")
                code = res.status_code
                resp = res.text
                self.resp_json_alias[alais] = resp
                allure_step(f"warning: {msg}")
                allure_step(f"[{mTime()}][{self.step_num}][post_api] after-->[Response.status_code==>>{code}]")
                allure_step(f"[{mTime()}][{self.step_num}][post_api] after-->[Response.text==>>\n{resp}]")
                return "PASS", resp, code
            else:
                self._json = {}
                self.resp_json = resp
                self.resp_json_alias[alais] = self.resp_json
                allure_step(f"[{mTime()}][{self.step_num}][post_api] method return alias:[{code}/{resp}]")
                return "PASS", resp, code

    def resp(self, *args, **kwargs):
        input_data = (tuple(args)[0]).strip()
        try:
            _resp = self.resp_json_alias[input_data]
        except:
            msg = f'[{mTime()}]❌ The input alais "{input_data}" incorrect, please check it.'
            allure_step_error(msg)
            return "FAIL", msg[14:]
        allure_step(f"[{mTime()}][{self.step_num}][resp] after-->self.resp_json_alias[{input_data}]==>>{_resp}")
        return "PASS", _resp

    def savejson(self, *args, **kwargs):
        """
        for get_api/post_api params/data/json (if py mode, json={'p': 'p1'})
        if tuple(args)[0] == '', tuple(args)[1] required dict
        if tuple(args)[0] != '', tuple(args)[1] any
        :param *args: required (excel mode)
        :param **kwargs: required (py mode)
        :return: dict/self._json
        """
        _dict = {}
        try:
            input_data = (tuple(args)[0]).strip()
            request_data = str(tuple(args)[1])
            allure_step(f"[{mTime()}][{self.step_num}][savejson] before1-->[*ARGS:{args}],[**KWARGS:{kwargs}]")
            _value = self.__get_utils(request_data, py_module)
            logger.error(_value)
            _valuen = self.__get_relations(_value)
            allure_step(f"[{mTime()}][{self.step_num}][savejson] before2-->request_data:{_valuen}")
            logger.error(_valuen)
            if input_data == '':
                if _valuen.startswith('{\'') or _valuen.startswith('[{\'') or \
                        _valuen.startswith('{\"') or _valuen.startswith('[{\"'):
                    try:
                        _dict = eval(_valuen)
                    except Exception as e:
                        msg = f"[{mTime()}][{self.step_num}][savejson]1❌ convert dict error.\n{e}"
                        allure_step_error(msg)
                        return "FAIL", msg[14:]
                    self._json = _dict
                    allure_step(f"[{mTime()}][{self.step_num}][savejson]1 after-->self._json==>>{self._json}")
                    allure_step(f"[{mTime()}][{self.step_num}][savejson]1 method return value:{self._json}")
                    return "PASS", self._json
                else:
                    msg = f"[{mTime()}][{self.step_num}][savejson]1 WARNING: The 'request_key' is '', should be 'dict' type."
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
            else:
                search_value = jmespath.search(input_data, self._json)  # 检索不到返回 None
                if _valuen.startswith('{\'') or _valuen.startswith('[{\'') or \
                        _valuen.startswith('{\"') or _valuen.startswith('[{\"'):
                    try:
                        _dict = eval(_valuen)
                    except Exception as e:
                        msg = f"[{mTime()}][{self.step_num}][savejson]2❌ convert dict error.\n{e}"
                        allure_step_error(msg)
                        return "FAIL", msg[14:]
                    if search_value is None:
                        allure_step(f"[{mTime()}][{self.step_num}][savejson]2 WARNING: jmespath.search({input_data},self._json)==>>{search_value}")
                        if '.' in input_data:
                            msg = f"[{mTime()}][{self.step_num}][savejson]2 WARNING: '.' is in the request_key '{input_data}'"
                            allure_step_error(msg)
                            return "FAIL", msg[14:]
                        self._json[input_data] = _dict
                    else:
                        self.__abs_jmespath(input_data, _dict)
                    allure_step(f"[{mTime()}][{self.step_num}][savejson]2 after-->self._json==>>{self._json}")
                    allure_step(f'[{mTime()}][{self.step_num}][savejson]2 method return value:{self._json}')
                    return "PASS", self._json
                else:
                    if search_value is None:
                        allure_step(f"[{mTime()}][{self.step_num}][savejson]3 WARNING: jmespath.search({input_data},self._json)==>>{search_value}")
                        if '.' in input_data:
                            msg = f"[{mTime()}][{self.step_num}][savejson]3 WARNING: '.' is in the request_key '{input_data}'"
                            allure_step_error(msg)
                            return "FAIL", msg[14:]
                        self._json[input_data] = _valuen
                    else:
                        self.__abs_jmespath(input_data, _valuen)

                    allure_step(f"[{mTime()}][{self.step_num}][savejson]3 after-->self._json==>>{self._json}")
                    allure_step(f'[{mTime()}][{self.step_num}][savejson]3 method return value:{self._json}')
                    return "PASS", self._json

        except Exception as e:
            msg = f"[{mTime()}][{self.step_num}][savejson]❌ convert dict error.\n{e}"
            allure_step_error(msg)
            return "FAIL", msg[14:]

    def __abs_jmespath(self, datan, _dict):
        """ for self._json """
        dataL = datan.split('.')
        _list = []
        for one in dataL:
            if one.startswith('['):
                onen = one.replace('[', '').replace(']', '')
                _list.append(onen)
            elif not one.startswith('[') and '[' in one:
                onen = one.split('[')
                _list.append(onen[0])
                _list.append(onen[1][:-1])
            else:
                _list.append(one)
        allure_step(f"[{mTime()}][{self.step_num}]----------数据预处理after:self.__abs_jmespath({datan,_dict})")
        length = len(_list)
        if length == 1:
            self._json[_list[0]] = _dict
        elif length == 2:
            self._json[_list[0]][_list[1]] = _dict
        elif length == 3:
            self._json[_list[0]][_list[1]][_list[2]] = _dict
        elif length == 4:
            self._json[_list[0]][_list[1]][_list[2]][_list[3]] = _dict
        elif length == 5:
            self._json[_list[0]][_list[1]][_list[2]][_list[3]][_list[4]] = _dict
        elif length == 6:
            self._json[_list[0]][_list[1]][_list[2]][_list[3]][_list[4]][_list[5]] = _dict
        elif length == 7:
            self._json[_list[0]][_list[1]][_list[2]][_list[3]][_list[4]][_list[5]][_list[6]] = _dict
        elif length == 8:
            self._json[_list[0]][_list[1]][_list[2]][_list[3]][_list[4]][_list[5]][_list[6]][_list[7]] = _dict
        elif length == 9:
            self._json[_list[0]][_list[1]][_list[2]][_list[3]][_list[4]][_list[5]][_list[6]][_list[7]][_list[8]] = _dict
        elif length == 10:
            self._json[_list[0]][_list[1]][_list[2]][_list[3]][_list[4]][_list[5]][_list[6]][_list[7]][_list[8]][_list[9]] = _dict
        else:
            print('length > 10')

    def resp2dict(self, *args, **kwargs):
        """
        get vlaue from self.resp_json to self.relations[key]=value
        1. from self.resp_json['a']['b'] to self.relations['xcode']=10001
        2. to self.relations['xcode']=10001 if args contains '=' e.g. =10001
        """
        _dict = {}
        try:
            input_data = (tuple(args)[0]).strip()
            request_data = str(tuple(args)[1])
            allure_step(f"[{mTime()}][{self.step_num}][resp2json] before-->[*ARGS:{args}],[**KWARGS:{kwargs}]")

            if input_data == '':
                msg = f"[{mTime()}][{self.step_num}][resp2json]❌ The 'request_key' is '', should not be empty."
                allure_step_error(msg)
                return "FAIL", msg[14:]
            elif request_data.lstrip().startswith('='):
                _value = self.__get_utils(request_data.lstrip()[1:], py_module)
                request_data_value = self.__get_relations(_value)
                if request_data_value.startswith('{\'') or request_data_value.startswith('[{\'') or \
                        request_data_value.startswith('{\"') or request_data_value.startswith('[{\"'):
                    try:
                        _dict = eval(request_data_value)
                    except Exception as e:
                        msg = f"[{mTime()}][{self.step_num}][resp2json]1❌ convert dict error.\n{e}"
                        allure_step_error(msg)
                        return "FAIL", msg[14:]
                    self.relations[input_data] = _dict
                    allure_step(f"[{mTime()}][{self.step_num}][resp2json]1 after-->self.relations==>>{self.relations}")
                    allure_step(f'[{mTime()}][{self.step_num}][resp2json]1 method return value:'+"{"+f'"{input_data}\": "{_dict}"'+"}")
                    # return "PASS", {f'{input_data}': f'{_dict}'}
                    return "PASS", self.relations
                else:
                    self.relations[input_data] = request_data_value
                    allure_step(f"[{mTime()}][{self.step_num}][resp2json]2 after-->self.relations==>>{self.relations}")
                    allure_step(f'[{mTime()}][{self.step_num}][resp2json]2 method return value:'+"{"+f'"{input_data}\": "{request_data_value}"'+"}")
                    # return "PASS", {f'{input_data}': f'{request_data_value}'}
                    return "PASS", self.relations
            else:
                _value = self.__get_utils(request_data.strip(), py_module)
                request_data_value = self.__get_relations(_value)
                if request_data_value.startswith('{\'') or request_data_value.startswith('[{\'') or \
                        request_data_value.startswith('{') or request_data_value.startswith('[{') or \
                        request_data_value.startswith('{\"') or request_data_value.startswith('[{\"'):
                    msg = f"[{mTime()}][{self.step_num}][resp2json]❌ The 'request_data' startswith '{request_data_value}' incorret."
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
                search_value = jmespath.search(request_data_value, self.resp_json)  # 检索不到返回 None
                if search_value is None:
                    msg = f"[{mTime()}][{self.step_num}][resp2json]❌ jmespath.search({request_data_value},self.resp_json)==>>{search_value}"
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
                else:
                    self.relations[input_data] = search_value
                    allure_step(f"[{mTime()}][{self.step_num}][resp2json]3 after-->self.relations==>>{search_value}")
                    allure_step(f'[{mTime()}][{self.step_num}][resp2json]3 method return value:'+"{"+f'"{input_data}\": "{search_value}"'+"}")
                    # return "PASS", {f'{input_data}': f'{search_value}'}
                    return "PASS", self.relations
        except Exception as e:
            msg = f"[{mTime()}][{self.step_num}][resp2json]❌ convert dict error.\n{e}"
            allure_step_error(msg)
            return "FAIL", msg[14:]



    # def save2dict(self, *args, **kwargs):
    #     """
    #     get vlaue from self.resp_json to self.relations[key]=value
    #     1. to self.relations['xcode']=10001 from self.resp_json['a']['b']
    #     2. to self.relations['xcode']=10001 if args contains '=' e.g. =10001
    #     """
    #     try:
    #         request_key = (tuple(args)[0]).strip()
    #         request_data = str(tuple(args)[1])
    #         allure_step(f"[{mTime()}][{self.step_num}][save2dict] before-->[*ARGS:{args}],[**KWARGS:{kwargs}]")
    #         if request_data.startswith('='):
    #             _value = self.__get_utils(request_data[1:], py_module)
    #             request_data_value = self.__get_relations(_value)
    #             self.relations[request_key] = request_data_value
    #         else:  # get data from self.resp_json
    #             request_data_path, end = self.__abs(request_data)
    #             if jsonpath.jsonpath(self.resp_json, f"$..{end}") is False:
    #                 msg = f"[{mTime()}][{self.step_num}][save2dict] The input path '{end}' not in self.resp_josn, please check it. self.resp_json:\n{self.resp_json}"
    #                 allure_step_error(msg)
    #                 return "FAIL", msg[14:]
    #             else:
    #                 request_data_value = eval(str(self.resp_json) + str(request_data_path))
    #                 self.relations[request_key] = request_data_value
    #
    #         allure_step(f"[{mTime()}][{self.step_num}][save2dict] after-->self.relations[{request_key}]==>>[{self.relations[request_key]}]")
    #         allure_step(f"[{mTime()}][{self.step_num}][save2dict] method return value:[{request_data_value}]")
    #         return "PASS", self.relations
    #     except Exception as e:
    #         msg = f"[{mTime()}][{self.step_num}][save2dict]❌ save dict error.."
    #         allure_step_error(msg)
    #         return "FAIL", msg[14:]

    def put_api(self):
        pass
    def delete_api(self):
        pass

    def __abs(self, datan):
        """ for savejson """
        dataL = datan.split(',')
        tmp = ''
        for one in dataL:
            if one.strip().isdigit():
                tmp = tmp + f"[{one.strip()}]"
            else:
                tmp = tmp + f"['{one.strip()}']"
        allure_step(f"[{mTime()}][{self.step_num}]----------数据预处理after:--__abs(datan)>>{datan}>>{tmp}--")
        return tmp, dataL[-1:][0]

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
                            param = param.replace('${' + key + '}', str(self.relations[key]))
                            allure_step(f"[{mTime()}][{self.step_num}]----------数据预处理after:--self.relations[{key}]>>{self.relations[key]}--")
            return param

    def assertInJson(self, *args):
        """
        get value through jsonpath(self.resp_json, f'$..{json_path}')
        WARNING: get jsonpath value maybe not unipue
        :param json_path:
        :param expect_value:
        """
        input_data = (tuple(args)[0]).strip()
        request_data = tuple(args)[1]
        allure_step(f"[{mTime()}][{self.step_num}][assertInJson] before--> self.resp_json==>>{self.resp_json}")
        allure_step(f"[{mTime()}][{self.step_num}][assertInJson] before--> request_data(expect)==>>{request_data}")
        res = jsonpath.jsonpath(self.resp_json, f'$..{input_data}')  # 找不到是结果是 False
        if res is None:
            allure_step(f"[{mTime()}][{self.step_num}]WARNING jsonpath-->>f'$..{input_data}'==>>{res}==>>{type(res)}")
        allure_step(f"[{mTime()}][{self.step_num}][assertInJson] ACTUAL_VALUE:[{res}]")
        allure_step(f"[{mTime()}][{self.step_num}][assertInJson] EXPECT_VALUE:[{request_data}]")
        try:
            if isinstance(res, list) and len(res) == 1:
                assert request_data == res[0]
            elif isinstance(res, list) and len(res) > 1:
                assert request_data in res
            else:
                assert request_data == str(res)
        except AssertionError as e:
            msg = f"[{mTime()}][{self.step_num}][assertInJson]❌ FAIL"
            allure_step_error(msg)
            return "FAIL", f'ACTUAL_VALUE :[{res}]' + f'<>EXPECT_VALUE :[{request_data}]'
        else:
            allure_step(f"[{mTime()}][{self.step_num}][assertInJson] PASS")
            return 'PASS', f'ACTUAL_VALUE :{res}' + f'<>EXPECT_VALUE :{request_data}'

    # def assertAbsPath(self, *args):
    #     """
    #     get value from self.resp_json[absolute_path_value] tp compare
    #     {"a": [{"b": "b1"}, {"c": "c1"}]}
    #     assertAbsPath(self, 'a[0].b', 'b1')
    #     doc: https://jmespath.org/
    #     :param abs_path:
    #     :param expect_value:
    #     """
    #     abs_path = (tuple(args)[0]).strip()
    #     request_data = tuple(args)[1]
    #     allure_step(f"[{mTime()}][assertAbsPath] before-->self.resp_json==>>{self.resp_json}")
    #     allure_step(f"[{mTime()}][assertAbsPath] before-->request_data(expect)==>>{request_data}")
    #
    #     search_value = jmespath.search(abs_path, self.resp_json)
    #     allure_step(f"[{mTime()}][assertAbsPath] :{search_value}")
    #     allure_step(f"[{mTime()}][assertAbsPath] EXPECT_VALUE:{request_data}")
    #     try:
    #         assert search_value == request_data
    #     except AssertionError as e:
    #         msg = f"[{mTime()}][assertAbsPath]❌ FAIL"
    #         allure_step_error(msg)
    #         return "FAIL", f'ACTUAL_VALUE :[{search_value}]' + f'<>EXPECT_VALUE :[{request_data}]'
    #     else:
    #         allure_step(f"[{mTime()}][assertAbsPath] PASS")
    #         return 'PASS', f'ACTUAL_VALUE :{search_value}' + f'<>EXPECT_VALUE :{request_data}'
    #
    # def assertResp2Json(self, *args):
    #     """
    #     compare expect_dict and self.resp_json
    #     assertResp2Json(self, z, {"a": [{"b": "b1"}, {"c": "c1"}]})
    #     :param expect_dict: dict only
    #     """
    #     expect_json = str(tuple(args)[1])
    #     allure_step(f"[{mTime()}][assertResp2Json] before-->self.resp_json==>>{self.resp_json}")
    #     allure_step(f"[{mTime()}][assertResp2Json] before-->request_data(expect)==>>{expect_json}")
    #     if expect_json.startswith('{') or expect_json.startswith('['):
    #         _value = str(expect_json).strip().replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
    #         _valuen = self.__get_relations(_value)
    #         try:
    #             _dict = json.loads(str(_valuen))
    #         except Exception as e:
    #             msg = f"[{mTime()}][assertResp2Json]❌ after--> convert request_data to dict error.{expect_json}"
    #             allure_step_error(msg)
    #             allure_step_error(f"[{mTime()}][assertResp2Json]❌ FAIL")
    #             return "FAIL", msg[14:]
    #     else:
    #         msg = f"[{mTime()}][assertResp2Json]❌ The input request_data '{expect_json}' incorrect, should be dict string."
    #         allure_step_error(msg)
    #         return "FAIL", msg[14:]
    #     error_count = HandleJson().json_assert(self.resp_json, _dict)
    #     allure_step(f"[{mTime()}][assertResp2Json] ACTUAL_VALUE:[{self.resp_json}]")
    #     allure_step(f"[{mTime()}][assertResp2Json] EXPECT_VALUE:[{_dict}]")
    #     try:
    #         assert error_count == 0
    #     except AssertionError as e:
    #         msg = f"[{mTime()}][assertResp2Json]❌ FAIL"
    #         allure_step_error(msg)
    #         return "FAIL", f'ACTUAL_VALUE :{self.resp_json}' + f'<>EXPECT_VALUE :{_dict}'
    #     else:
    #         allure_step(f"[{mTime()}][assertResp2Json] PASS")
    #         return 'PASS', f'ACTUAL_VALUE :{self.resp_json}' + f'<>EXPECT_VALUE :{_dict}'

    def assertMatch2Json(self, *args, **kwargs):
        """
        match dict/str from self.resp_json to compare
        self.resp_json = {"a": [{"b": "b1"}, {"c": "c1"}]}
        assertMatch2Json(self, 'a[0]', '{"b": "b1"}')
        doc: https://jmespath.org/
        :param part_path: get value from self.resp_json[part_path]
        :param expect_value: dict/str
        """
        part_path = str(tuple(args)[0]).strip()
        expect_json = str(tuple(args)[1])
        allure_step(f"[{mTime()}][{self.step_num}][assertMatch2Json] before-->self.resp_json==>>{self.resp_json}")
        allure_step(f"[{mTime()}][{self.step_num}][assertMatch2Json] before-->request_data(expect)==>>{expect_json}")

        if part_path == '' or part_path == 'null' or part_path == 'None' or part_path == 'resp_json':
            _expect = self.__resp_assert(expect_json)
            error_count = HandleJson().json_assert(self.resp_json, _expect)
            allure_step(f"[{mTime()}][{self.step_num}][assertMatch2Json] ACTUAL_VALUE:[{self.resp_json}]")
            allure_step(f"[{mTime()}][{self.step_num}][assertMatch2Json] EXPECT_VALUE:[{_expect}]")
            try:
                assert error_count == 0
            except AssertionError as e:
                msg = f"[{mTime()}][{self.step_num}][assertMatch2Json]❌ FAIL"
                allure_step_error(msg)
                return "FAIL", f'ACTUAL_VALUE :{self.resp_json}' + f'<>EXPECT_VALUE :{_expect}'
            else:
                allure_step(f"[{mTime()}][{self.step_num}][assertMatch2Json] PASS")
                return 'PASS', f'ACTUAL_VALUE :{self.resp_json}' + f'<>EXPECT_VALUE :{_expect}'
        else:
            search_value = jmespath.search(part_path, self.resp_json)  # 检索不到返回 None
            if search_value is None:
                allure_step(f"[{mTime()}][{self.step_num}]WARNING jmespath.search-->>f'{part_path}'==>>{search_value}")
            allure_step(f"[{mTime()}][{self.step_num}][assertMatch2Json] after-->self.resp_json.{part_path}==>>{search_value}")
            _expect = self.__resp_assert(expect_json)
            # _expect = self.__get_relations(expect_json)
            error_count = HandleJson().json_assert(search_value, _expect)

            allure_step(f"[{mTime()}][{self.step_num}][assertMatch2Json] ACTUAL_VALUE:[{self.resp_json}]")
            allure_step(f"[{mTime()}][{self.step_num}][assertMatch2Json] EXPECT_VALUE:[{_expect}]")
            try:
                assert error_count == 0
            except AssertionError as e:
                msg = f"[{mTime()}][{self.step_num}][assertMatch2Json]❌ FAIL"
                allure_step_error(msg)
                return "FAIL", f'ACTUAL_VALUE :{search_value}' + f'<>EXPECT_VALUE :{_expect}'
            else:
                allure_step(f"[{mTime()}][{self.step_num}][assertMatch2Json] PASS")
                return 'PASS', f'ACTUAL_VALUE :{search_value}' + f'<>EXPECT_VALUE :{_expect}'

    def __resp_assert(self, expect_json):
        if expect_json.strip().startswith('{') or expect_json.strip().startswith('['):
            _value = expect_json.strip()
            _value = self.__get_utils(_value, py_module)
            _valuen = self.__get_relations(_value)
            try:
                _dict = eval(str(_valuen))
            except Exception as e:
                msg = f"[{mTime()}][{self.step_num}][assertResp2Json]❌ after--> convert request_data to dict error.{expect_json}"
                allure_step_error(msg)
                return "FAIL", msg[14:]
            return _dict
        else:
            _value = self.__get_utils(expect_json.strip(), py_module)
            _valuen = self.__get_relations(_value)
            return _valuen

def allure_step(value):
    with allure.step(value):
        logger.info(value[14:])

def allure_step_error(value):
    with allure.step(value):
        logger.error(value[14:])

if __name__ == '__main__':
    pass
