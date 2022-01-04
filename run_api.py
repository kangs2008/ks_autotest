import pytest, os, subprocess
from pathlib import Path
from Common.setting import REPORT_HTML_API_DIR
from Common.handle_config import ReadWriteConfFile
from Common.utils import mDate, mDateTime
# cmd =['D:/allure-2.13.6/bin/allure generate D:/desk20201127/ks_web_allure/temp -o D:/desk20201127/ks_web_allure/Report --clean']
# cmd = 'allure generate ./temp -o ./Report --clean'
# os.system(cmd)
# pytest.main(['./TestCases/Login/test_baidu.py', '-sv', '--alluredir', './temp'])  # '--report','re2021'
# cmd = 'allure generate ./temp -o ./Report --clean'
# os.system(cmd)

excel_file_path = r'D:\desk20201127\ks_web_allure\Datas'
excel_file_name = 'test_apidata.xlsx'
sheet_names = 't_接'  # 't_接,t_接22'
sheet_rule = 't_'
sheet_kvconfig = 'config'  # 'config,config22'

ReadWriteConfFile().set_option('report', 'report_dir_folder', mDate()+'_html_api')
ReadWriteConfFile().set_option('report', 'report_file_name', f'report_{mDateTime()}.html')
report_dir = ReadWriteConfFile().get_option('report', 'report_dir_folder')
report_file = ReadWriteConfFile().get_option('report', 'report_file_name')

pytest.main([f'--html=./Report/Html_api/{report_dir}/{report_file}', '--self-contained-html',
             f'--path={str(excel_file_path)}',f'--name={str(excel_file_name)}',
             f'--sheet={str(sheet_names)}',f'--rule={str(sheet_rule)}',
             f'--conf={str(sheet_kvconfig)}'])

# ReadWriteConfFile().set_option('test_data', 'excel_file_path', excel_file_path)
# ReadWriteConfFile().set_option('test_data', 'excel_file_name', excel_file_name)
# ReadWriteConfFile().set_option('test_data', 'sheet_names', sheet_names)
# ReadWriteConfFile().set_option('test_data', 'sheet_rule', sheet_rule)
# ReadWriteConfFile().set_option('test_data', 'sheet_kcConfig', sheet_kvconfig)
# pytest.main(['--html=./Report/Html_api/20220103_html_api/report_.html', '--self-contained-html'])

