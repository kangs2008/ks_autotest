import pytest
import allure
import sys
from Common.login_datas import data1
from Common.handle_logger import logger
from Pages.BaiduPage.baidu_page import BaiduPage
from Common.basepage import BasePage

@allure.feature("login 异常测试用例，feature")
@pytest.mark.usefixtures('start_session')
# @pytest.mark.usefixtures('report')
# @pytest.mark.usefixtures('refresh_page')
class TestLogin:

    # 异常测试用例
    @allure.story("测试login 方法，story")
    @pytest.mark.parametrize('data', data1)
    def test_login(self, data, start_session):
        """描述！！！！"""
        logger.info(f" 执行 {self.__class__.__name__} 测试套件Suite ")
        logger.info(f" 执行 {sys._getframe().f_code.co_name} 测试用例Case ")
        baidu = BaiduPage(start_session)
        news = baidu.get_news_text()

        baidu.search(data['input'])
        assert news == data['news']
        logger.info(" 结束执行 {0} 测试用例， 测试结果 --- PASS ".format(sys._getframe().f_code.co_name))







    # # 异常测试用例
    # @allure.story("login 异常1，story")
    # @pytest.mark.parametrize('data', invalid_data2)
    # # @allure.dynamic.description('动态描述？')
    # def test_login_user_error(self, data, start_session):
    #     allure.dynamic.description('动态描述？')
    #     logger.info(" 执行 {0} 测试套件Suite ".format(self.__class__.__name__))
    #     logger.info(" 执行 {0} 测试用例Case ".format(sys._getframe().f_code.co_name))
    #
    #     BaiduPage(start_session).input_username(data['user'])
    #     BaiduPage(start_session).input_pwd(data['pwd'])
    #     BaiduPage(start_session).login_btn()
    #     # msg = BaiduPage(start_session).get_login_errMsg()
    #     msg = BaiduPage(start_session).get_user_errMsg()
    #     logger.info("期望值：{0}".format(data['expect']))
    #     logger.info("实际值：{0}".format(msg))
    #     try:
    #         assert msg, data['expect']
    #         logger.info(" 结束执行 {0} 测试用例， 测试结果 --- PASS ".format(sys._getframe().f_code.co_name))
    #         BaiduPage(start_session).save_screenshot("{0}-正常截图".format(data['user']))
    #     except:
    #         logger.error(" 结束执行 {0} 测试用例， 测试结果 --- False ".format(sys._getframe().f_code.co_name))
    #         BaiduPage(start_session).save_screenshot("{0}-异常截图".format(data['user']))
    #         raise
    #
    # # 异常测试用例
    # @allure.story("login 异常3，story")
    # @pytest.mark.parametrize('data', invalid_data3)
    # def test_login_pwd_error(self, data, start_session):
    #     allure.dynamic.title("aaaaa")
    #     logger.info(" 执行 {0} 测试套件Suite ".format(self.__class__.__name__))
    #     logger.info(" 执行 {0} 测试用例Case ".format(sys._getframe().f_code.co_name))
    #
    #     try:
    #         BaiduPage(start_session).input_username(data['user'])
    #         BaiduPage(start_session).input_pwd(data['pwd'])
    #         BaiduPage(start_session).login_btn()
    #
    #         msg = BaiduPage(start_session).get_pwd_errMsg()
    #         logger.info("期望值：{0}".format(data['expect']))
    #         logger.info("实际值：{0}".format(msg))
    #         assert msg, data['expect']
    #         msg = '111111'
    #         assert msg, data['expect']
    #         # assertTrueMethod(msg, data['expect'])
    #
    #         logger.info(" 结束执行 {0} 测试用例， 测试结果 --- PASS ".format(sys._getframe().f_code.co_name))
    #         BaiduPage(start_session).save_screenshot("正常截图")
    #     except:
    #         logger.error(" 结束执行 {0} 测试用例， 测试结果 --- False ".format(sys._getframe().f_code.co_name))
    #         BaiduPage(start_session).save_screenshot("异常截图")
    #         raise
    #
    # # 异常测试用例
    # @allure.story("login 异常4，story")
    # @pytest.mark.parametrize('data', invalid_data4)
    # def test_login_pwd_error(self, data, start_session):
    #     allure.dynamic.title("aaaaa")
    #     logger.info(" 执行 {0} 测试套件Suite ".format(self.__class__.__name__))
    #     logger.info(" 执行 {0} 测试用例Case ".format(sys._getframe().f_code.co_name))
    #
    #     try:
    #         BaiduPage(start_session).input_username(data['user'])
    #         BaiduPage(start_session).input_pwd(data['pwd'])
    #         BaiduPage(start_session).login_btn()
    #
    #         msg = BaiduPage(start_session).get_pwd_errMsg()
    #         logger.info("期望值：{0}".format(data['expect']))
    #         logger.info("实际值：{0}".format(msg))
    #         assert msg, data['expect']
    #         msg = '111111'
    #         assert msg, data['expect']
    #         # assertTrueMethod(msg, data['expect'])
    #
    #         logger.info(" 结束执行 {0} 测试用例， 测试结果 --- PASS ".format(sys._getframe().f_code.co_name))
    #         BaiduPage(start_session).save_screenshot("正常截图")
    #     except:
    #         logger.error(" 结束执行 {0} 测试用例， 测试结果 --- False ".format(sys._getframe().f_code.co_name))
    #         BaiduPage(start_session).save_screenshot("异常截图")
    #         raise

    # 正常用例
    # @pytest.mark.lucas
    # @pytest.mark.smoke
    # @pytest.mark.parametrize('data', pass_data)
    # def test_login_success(self, data, start_session):
    #     logger.info(" 执行 {0} 测试套件Suite ".format(self.__class__.__name__))
    #     logger.info(" 执行 {0} 测试用例Case ".format(sys._getframe().f_code.co_name))
    #     BaiduPage(start_session).input_username(data['user'])
    #     BaiduPage(start_session).input_pwd(data['pwd'])
    #     BaiduPage(start_session).login_btn()
    #
    #     try:
    #         assert IndexPage(start_session[0]).isExist_logout_ele()
    #         logger.info(" 结束执行 {0} 测试用例， 测试结果 --- PASS ".format(sys._getframe().f_code.co_name))
    #         start_session[1].save_pictuer("{0}-正常截图".format(LD.success_data['name']))
    #     except:
    #         logger.error(" 结束执行 {0} 测试用例， 测试结果 --- False ".format(sys._getframe().f_code.co_name))
    #         start_session[1].save_pictuer("{0}-异常截图".format(LD.success_data['name']))
    #         raise
