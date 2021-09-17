import pytest
from selenium import webdriver
from Common.handle_logger import logger

from selenium.webdriver.remote.webdriver import WebDriver
import pytest
from Common.basepage import BasePage


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        #判断用例是否失败或者xfail跳过的测试
        if (report.skipped and xfail) or (report.failed and not xfail):
        	#获取测试用例代码中webDriver参数来获取浏览器进行抓屏
            for i in item.funcargs:
                if isinstance(item.funcargs[i], WebDriver):
                	#截图
                    BasePage(item.funcargs[i]).save_capture("异常图")
                    pass
                pass
            pass
        report.extra = extra


# def create_driver(options=Options()):
#     # type: () -> webdriver.Remote
#     if config.arguments and len(config.arguments) > 0:
#         for arg in config.arguments:
#             options.add_argument(arg)
#             pass
#         pass
#     driver = None
#     if config.runMode == config.RunModeType.remote:
#         driver = webdriver.Remote(command_executor=config.remoteUrl, options=options)
#         pass
#     else:
#         driver = webdriver.Chrome(options=options)
#         pass
#     driver.set_page_load_timeout(config.timeOut)
#     driver.set_script_timeout(config.timeOut)
#     driver.set_window_size(1366, 768)
#     return driver
#     pass

# @pytest.fixture(scope='class', autouse=False)
# def project_session_start():
#     logger.info("========== open browser ===========")
#     global driver
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     yield driver
#     driver.quit()
#     logger.info("========== close browser ===========")

# @pytest.fixture()
# def project_func():
#     print("project_func")

