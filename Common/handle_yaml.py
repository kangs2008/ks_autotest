import json, re
import os.path

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

    def yaml_write(self, path, file_name, _key, _value):
        with open(os.path.join(path, file_name), 'r', encoding='utf-8') as fp:
            config = yaml.load(fp, Loader=yaml.RoundTripLoader)
            config[_key] = _value
        with open(os.path.join(path, file_name), 'w', encoding='utf-8') as fp2:
            yaml.dump(config, fp2, Dumper=yaml.RoundTripDumper, allow_unicode=True)  # block_sqp_indent=2

    def yaml_read(self, path, file_name):
        with open(os.path.join(path, file_name), 'r', encoding='utf-8') as fp:
            config = yaml.load(fp, Loader=yaml.RoundTripLoader)
            return config

    def yaml_write_to_add(self, path, file_name, _key, _value):
        _list = []
        with open(os.path.join(path, file_name), 'r', encoding='utf-8') as fp:
            config = yaml.load(fp, Loader=yaml.RoundTripLoader)
            for one in config[_key]:
                _list.append(one)
            if type(_value).__name__ == 'DotDict':
               _value = eval(str(_value))
            _list.append(_value)
            config[_key] = _list
        with open(os.path.join(path, file_name), 'w', encoding='utf-8') as fp2:
            yaml.dump(config, fp2, Dumper=yaml.RoundTripDumper, allow_unicode=True)




if __name__ == '__main__':
    pass









