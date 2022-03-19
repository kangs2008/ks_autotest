import json, re
from Common.handle_logger import logger
import allure

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
                                f"[!] RESPONSE-JSON== > [{k}] ** VALUE ** diff:\n < actual >: {str(a_flow[k])} \n < expect >:{v}")
                            error_count += 1
                            allure_step_error(msg)

                    if isinstance(str(a_flow[k]), list) and isinstance(v, list):
                        if sorted(str(a_flow[k])) != sorted(v):
                            msg = (
                                f"[!] RESPONSE-JSON== > [{k}] ** VALUE ** diff:\n < actual >: {str(a_flow[k])} \n < expect >:{v}")
                            error_count += 1
                            allure_step_error(msg)
                        else:
                            if str(a_flow[k]) != v:
                                msg = (
                                    f"[!] RESPONSE-JSON== > [{k}] ** VALUE ** diff:\n < actual >: {str(a_flow[k])} \n < expect >:{v}")
                                error_count += 1
                                allure_step_error(msg)
            else: # 默认全部比较
                for k, v in iter(e_flow.items()):
                    v = str(v)
                    if isinstance(str(a_flow[k]), list) and isinstance(v, list):
                        if sorted(str(a_flow[k])) != sorted(v):
                            msg = (f"[!] RESPONSE-JSON== > [{k}] ** VALUE ** diff:\n < actual >: {str(a_flow[k])} \n < expect >:{v}")
                            error_count += 1
                            allure_step_error(msg)
                    else:
                        if str(a_flow[k]) != v:
                            msg = (f"[!] RESPONSE-JSON== > [{k}] ** VALUE ** diff:\n < actual >: {str(a_flow[k])} \n < expect >:{v}")
                            error_count += 1
                            allure_step_error(msg)
        else:
            msg = (
                f"[!] RESPONSE-JSON== > ** KEY ** diff:\n < actual >:{sorted(a_flow.keys())} \n < expect >:{sorted(e_flow.keys())}")
            error_count += 1
            allure_step_error(msg)
        return error_count
        # if error_count != 0:
        #     raise 'aaaaaa'

    def json_generator(self, indict, key_value=None):
        """
        :param indict:
        :param key_value:
        :return:
        """
        key_value = key_value[:] if key_value else []
        # print(indict)
        if isinstance(indict, list):
            print('00')
            tier = -1
            for v in indict:
                tier = tier+1
                for d in self.json_generator(v, key_value + ['[{0}]'.format(tier)]):
                    yield d

        elif isinstance(indict, dict):
            print(indict)
            print(11)
            for key, value in indict.items():
                tier = -1
                print(f"--key--{key}-value-{value}--")
                if isinstance(value, dict):
                    print(22)
                    if len(value) == 0:
                        yield key_value + [key, '{}']
                    else:
                        for d in self.json_generator(value, key_value + [key]):
                            yield d
                elif isinstance(value, list):
                    print(33)

                    if len(value) == 0:
                        yield key_value + [key, '[]']
                    else:
                        for v in value:
                            tier = tier + 1
                            print(v, key_value + [key + '[{0}]'.format(tier)])
                            for d in self.json_generator(v, key_value + [key + '[{0}]'.format(tier)]):
                                print(f'-d---{d}-------')
                                yield d
                else:
                    print(44)
                    yield key_value + [key, value]
        else:
            yield key_value + [indict]


    def structure_flow_sub(self, json_gen_obj):
        """
        ：param json_gen_obj：
        :return:
        """
        structure = {}
        for i in self.json_generator(json_gen_obj):
            print(f"---i----{i}--------{i[:-1]}----{structure.keys()}--------")
            if '.'.join(i[:-1]) in structure.keys() and not isinstance(structure['.'.join(i[:-1])], list):
                print('---a')
                structure['.'.join(i[:-1])] = [structure['.'.join(i[:-1])]]
                structure['.'.join(i[:-1])].append(i[-1])
            elif '.'.join(i[:-1]) in structure.keys() and isinstance(structure['.'.join(i[:-1])], list):
                print('---b')
                structure['.'.join(i[:-1])].append(i[-1])
            else:
                print('---c----------')
                structure['.'.join(i[:-1])] = i[-1]
        return structure


def allure_step_error(value):
    with allure.step(value):
        logger.error(value[14:])

if __name__ == '__main__':
    # a = {"employees": [2, "戻る", {'bbb': 'bbb1'}], 'aaa': 'aaa1'}
    # b = {"employees": [2, "戻る", {'bbb': 'bbb1'}], 'aaa': 'aaa1'}
    # a = {"employees1": 121}
    # b = {"employees": 11}
    # a = [33,{"employees": '11', 'aaa1': ["戻る", 2]}]
    # b = [33,{"employees": '11', 'aaa1': ["戻る", 2]}]
    a = [121, 22]
    b = [121, 22]
    print(HandleJson().json_assert(a, b))
    # HandleJson().structure_flow_sub(a)
    # print(HandleJson().json_generator(a))









