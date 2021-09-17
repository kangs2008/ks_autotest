import os

import pytest

# pytest.main(['-s', './TestCases/Login/test_baidu.py', '--alluredir', './temp'])
pytest.main(['./TestCases/Login/test_baidu.py', '--alluredir', './temp'])

os.system('allure generate ./temp -o ./Report --clean')
