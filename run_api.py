import pytest, os, subprocess
from pathlib import Path
from Common.setting import REPORT_HTML_API_DIR
from Common.handle_config import ReadWriteConfFile
# cmd =['D:/allure-2.13.6/bin/allure generate D:/desk20201127/ks_web_allure/temp -o D:/desk20201127/ks_web_allure/Report --clean']
# cmd = 'allure generate ./temp -o ./Report --clean'
# os.system(cmd)


# pytest.main(['./TestCases/Login/test_baidu.py', '-sv', '--alluredir', './temp'])  # '--report','re2021'
# cmd = 'allure generate ./temp -o ./Report --clean'
# os.system(cmd)

# pytest.main(['./TestCases/Login/test_baidu.py', '--html=./Report/html/report_.html', '--self-contained-html'])

report_excel = ReadWriteConfFile().get_option('report_dir', 'report_dir_folder')
tmp_excel_path = Path().joinpath(REPORT_HTML_API_DIR, report_excel, 'report_.html')
pytest.main(['--html=./Report/Html_api/20220103_html_api/report_.html', '--self-contained-html'])

