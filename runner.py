import os, click
import subprocess

import pytest
from Common.handle_config import ReadWriteConfFile
from Common.setting import REPORT_DIR, BASE_DIR, REPORT_CURRENT_DIR
from Common.handle_file import file_zip_path, file_del, file_copy, file_and_folder_copy, current_folder_file_copy

print('aaaaaaaaaaaaaaaaa')
pytest.main([]) #'--report','re2021'
# os.system('allure generate ./temp -o ./Report --clean')
def set_exec_ini(section, option, value):
    ReadWriteConfFile().add_section(section)
    ReadWriteConfFile().set_option(section, option, value)

def allure_generate():
    # cmd =['D:/allure-2.13.6/bin/allure generate D:/desk20201127/ks_web_allure/temp -o D:/desk20201127/ks_web_allure/Report --clean']
    cmd = ['allure generate ./temp -o ./Report --clean']
    # id = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read().decode('utf-8')
    os.system('allure generate ./temp -o ./Report --clean')
    print('id')

    report_dir = ReadWriteConfFile().get_option('report_dir', 'report_dir_folder')
    copy_to = os.path.join(REPORT_CURRENT_DIR, report_dir)
    file_del(os.path.join(BASE_DIR, 'temp'))
    file_and_folder_copy(REPORT_DIR, f'{copy_to}', [], '')
    # set_exec_ini('report_dir', 'report_dir_folder', '')
    print('-----copy end')
    pass
allure_generate()

print('bbbbbbbb')
# if __name__ == '__main__':
#     # pytest.main(['./TestCases/Login/test_baidu.py', '--alluredir', './temp'])
#     main()


