import json, re
from Common.handle_logger import logger
class HandleJson:
    """
    定义一个json格式数据处理类
    """

    @staticmethod
    def loads_data(data):
        """
        将json数据格式的数据转换为字典型的数据类型
        :param data: json格式字符串
        :return: 字典数据类型
        """
        dict_ison = json.loads(data)
        return dict_ison

    @staticmethod
    def load_data(filename):
        """
        读取json文件中的json数据并转换为字典型的数据类型
        :param filename:json文件名
        :return:字典数据类型
        """
        with open(filename, mode='r', encoding='utf-8') as fp:
            dict_file = json.load(fp)
        return dict_file

    @staticmethod
    def dumps_data(data):
        """
        将字典数据类型转换为json格式类型数据
        :param data: 字典数据类型
        :return: json格式字符串
        """
        json_dict = json.dumps(data, ensure_ascii=False)
        return json_dict

    @staticmethod
    def dump(data, filename):
        """
        将字典数据类型转换为json格式数据并存储到json格式的文件中
        :param data: 字典数据类型
        :param filename: json文件名
        :return: json格式文件
        """
        with open(filename, mode='w', encoding='utf-8') as fp:
            json.dump(data, fp)

    def json_generator(self, indict, key_value=None):
        """
        :param indict:
        :param key_value:
        :return:
        """
        key_value = key_value[:] if key_value else []
        if isinstance(indict, dict):
            for key, value in indict.items():
                tier = -1
                if isinstance(value, dict):
                    if len(value)==0:
                        yield key_value + [key, '{}']
                    else:
                        for d in self.json_generator(value, key_value + [key]):
                            yield d
                elif isinstance(value, list):
                    if len(value) == 0:
                        yield key_value + [key, '[]']
                    else:
                        for v in value:
                            tier =tier +1
                            for d in self.json_generator(v, key_value + [key +'[{0}]'.format(tier)]):
                                yield d
                else:
                    yield key_value + [key, value]
        else:
            if not key_value:
                yield indict
            else:
                yield key_value + [indict]

    def json_assert(self, a_json, e_json):

        """
        JSON数据比较断言
        ：param a＿json：实际的json数据
        ：param e＿json：期望的json数据
        :return:
        """
        error_count = 0
        #转为方便比较的数据流结构
        a_flow = self.structure_flow_sub(a_json)
        e_flow = self.structure_flow_sub(e_json)
        #检查期望结果是否使用｛IGNORE｝
        start_reg_pat = u'.*'
        ignore_reg_pat = start_reg_pat + u"{{IGNORE}}\s*$"
        ignore_count = 0
        msg = 'success'
        for e_v in e_flow.values():
            if isinstance(e_v, list):
                for each in e_v:
                    each = str(each)
                    if re.match(ignore_reg_pat, each):
                        ignore_count += 1
            else:
                e_v = str(e_v)
                if re.match(ignore_reg_pat, e_v):
                    ignore_count += 1
        if sorted(a_flow.keys()) == sorted(e_flow.keys()):
            if ignore_count > 0:
                for k, v in iter(e_flow.items()):
                    # 若value为 ＂｛｛IGNORE｝｝” 则忽略比对
                    v = str(v)
                    if isinstance(v, list):
                        # reg_ignore_object = map(lambda _each:re.match(ignore_reg_pat, unicode(_each)), v)
                        reg_ignore_object = map(lambda _each: re.match(ignore_reg_pat, _each), v)
                        if None not in reg_ignore_object and len(reg_ignore_object) == len(v):
                            continue
                    elif re.match(ignore_reg_pat, v):
                        continue
                    else:
                        if str(a_flow[k]) != v:
                            msg = (
                                "[!] RESPONSE-JSON＝＝＞ [{K}]的＊＊VALUE＊＊不同：\n ＜actual＞：{A} \n < expect >:{E}".format(K=k,
                                                                                                                  A=str(
                                                                                                                      a_flow[
                                                                                                                          k]),
                                                                                                                  E=v))
                            error_count += 1
                            print(msg)
                            logger.info(msg)

                    if isinstance(str(a_flow[k]), list) and isinstance(v, list):
                        if sorted(str(a_flow[k])) != sorted(v):
                            msg = ("[!] RESPONSE-JSON＝＝＞ [{K}]的＊＊VALUE＊＊不同：\n ＜actual＞：{A} \n < expect >: {E}".format(K=k, A=a_flow[k], E=v))
                            error_count += 1
                            print(msg)
                            logger.info(msg)
                        else:
                            if str(a_flow[k]) != v:
                                msg = ("[!] RESPONSE-JSON＝＝＞ [{K}]的＊＊VALUE＊＊不同：\n ＜actual＞：{A} \n < expect >:{E}".format(K=k,A=str(a_flow[k]), E=v))
                                error_count += 1
                                print(msg)
                                logger.info(msg)
            else: # 默认全部比较
                for k, v in iter(e_flow.items()):
                    v = str(v)
                    if isinstance(str(a_flow[k]), list) and isinstance(v, list):
                        if sorted(str(a_flow[k])) != sorted(v):
                            msg = ("[!] RESPONSE-JSON＝＝＞ [{K}]的＊＊VALUE＊＊不同：\n ＜actual＞： {A} \n < expect >:{E}".format(K=k, A=str(a_flow[k]), E=v))
                            error_count += 1
                            print(msg)
                            logger.info(msg)
                    else:
                        if str(a_flow[k]) != v:
                            msg = (
                                "[!] RESPONSE-JSON＝＝＞ [{K}]的＊＊VALUE＊＊不同：\n ＜actual＞： {A} \n < expect >:{E}".format(K=k, A=str(a_flow[k]), E=v))
                            error_count += 1
                            print(msg)
                            logger.info(msg)
        else:
            msg = (
                f"[!] RESPONSE-JSON＝＝＞ ＊＊KEY＊＊不同：\n ＜actual＞：{sorted(a_flow.keys())} \n < expect >:{sorted(e_flow.keys())}")
            error_count += 1
            print(msg)
            logger.info(msg)
        return  error_count
        # if error_count != 0:
        #     raise 'aaaaaa'

    def structure_flow_sub(self, json_gen_obj):
        """
        ：param json_gen_obj：
        :return:
        """
        structure = {}
        for i in self.json_generator(json_gen_obj):
            if '.'.join(i[:-1]) in structure.keys() and not isinstance(structure['.'.join(i[:-1])], list):
                structure['.'.join(i[:-1])] = [structure['.'.join(i[:-1])]]
                structure['.'.join(i[:-1])].append(i[-1])
            elif '.'.join(i[:-1]) in structure.keys() and isinstance(structure['.'.join(i[:-1])], list):
                structure['.'.join(i[:-1])].append(i[-1])
            else:
                structure['.'.join(i[:-1])] = i[-1]
        return structure


if __name__ == '__main__':
    a = {"employees": ["Bill", "戻る", "你好吗"]}
    b = {"employees": ["Bill", "戻るあ", "你好吗"]}
    # HandleJson().json_assert(a, b)
    # HandleJson().structure_flow_sub(a)
    print(HandleJson().json_generator(a))









