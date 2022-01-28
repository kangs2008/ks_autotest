import json, re
from Common.handle_logger import logger
import allure
from pathlib import Path
from ruamel import yaml


class HandleYaml:
    """
    YAML data
    """

    def read_yaml_data(self, yamlpath):
        """
        read yaml file
        :param yamlpath: path + filename
        :return: dict
        """
        with open(yamlpath, mode='r', encoding='utf-8') as fp:
            d = yaml.load(fp, Loader=yaml.RoundTripLoader)  # to keep comment
        return d
    def set_yaml_data(self, yamlpath, _data):
        """
        write yaml file
        :param yamlpath: path + filename
        :return: dict
        """
        with open(yamlpath, mode='w', encoding='utf-8') as fp:
            yaml.dump(_data, fp, Dumper=yaml.RoundTripDumper, allow_unicode=True)

    def data_pretty(self, data):
        """
        将字典数据类型转换为json格式类型数据
        :param data: 字典数据类型
        :return: json格式字符串
        """
        json_dict = json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False)
        return json_dict

if __name__ == '__main__':
    pass









