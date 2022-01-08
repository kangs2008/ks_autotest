import pytest, os, subprocess
from Common.setting import BASE_DIR, REPORT_DIR
# cmd =['D:/allure-2.13.6/bin/allure generate D:/desk20201127/ks_web_allure/temp -o D:/desk20201127/ks_web_allure/Report --clean']
# cmd = 'allure generate ./temp -o ./Report --clean'
# os.system(cmd)


pytest.main(['./TestCasesWeb/Login/test_baidu.py', '-sv', '--alluredir', './temp'])  # '--report','re2021'
cmd = 'allure generate ./temp -o ./Report --clean'
os.system(cmd)

# pytest.main(['./TestCasesWeb/Login/test_baidu.py', '--html=./Report/html/report_.html', '--self-contained-html'])


