import time, sys, datetime, cv2
import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from Common.handle_logger import logger as case_logger
from Common.setting import PIC_DIR, FREQUENCY, TIMEOUT, RELATIVE_DIR
from Common.utils import usageTime, mTime


class BasePage:
    """
    BasePage class
    """

    def __init__(self, driver):
        self.driver = driver

    def save_capture(self, loc_name):
        """
        take a screenshot
        :param loc_name: capture name
        """
        try:
            start_time = datetime.datetime.now()
            file_name = PIC_DIR + r"\{}_{}.png".format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()), loc_name)
            relative_name = RELATIVE_DIR + r"\{}_{}.png".format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()), loc_name)
            self.driver.save_screenshot(file_name)
            with open(file_name, mode='rb') as f:
                file = f.read()
            allure.attach(file, loc_name, allure.attachment_type.PNG)
            end_time = datetime.datetime.now()
            case_logger.info("[{}]{} TIME:".format(sys._getframe().f_code.co_name, relative_name, usageTime(end_time,start_time)))
        except Exception as e:
            with allure.step(f"[{mTime()}][{sys._getframe().f_code.co_name}][{loc_name}] FAIL"):
                pass
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]{} TIME:".format(sys._getframe().f_code.co_name, relative_name, usageTime(end_time, start_time)))

    def save_capture_paint(self, loc_name, pos):
        """
        screenshot with paint pos
        :param img_doc: capture name
        :param pos: element location
        """
        try:
            start_time = datetime.datetime.now()
            file_name = PIC_DIR + r"\{}_{}.png".format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()), loc_name)
            relative_name = RELATIVE_DIR + r"\{}_{}.png".format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()),
                                                             loc_name)
            self.driver.save_screenshot(file_name)

            screenvc = cv2.imread(file_name)
            img_res = cv2.circle(screenvc, pos, 15, (0, 0, 225), 2)
            cv2.imwrite(file_name, img_res)

            with open(file_name, mode='rb') as f:
                file = f.read()
            allure.attach(file, loc_name, allure.attachment_type.PNG)
            end_time = datetime.datetime.now()
            case_logger.info("[{}]{} TIME:{}".format(sys._getframe().f_code.co_name, relative_name, usageTime(end_time,start_time)))
        except Exception as e:
            with allure.step(f"[{mTime()}][{sys._getframe().f_code.co_name}][{loc_name}] FAIL"):
                pass
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]{} TIME:{}".format(sys._getframe().f_code.co_name, relative_name, usageTime(end_time, start_time)))

    def goto_url(self, url, pic, timeout=TIMEOUT, frequency=FREQUENCY):
        """
        goto url
        :param url: url
        :param pic: '' or None :don't take a screenshot
        :param timeout: 20s
        :param frequency: 0.5s
        """
        try:
            start_time = datetime.datetime.now()
            d = self.driver.get(url)
        except Exception as e:
            with allure.step(f"[{mTime()}][{sys._getframe().f_code.co_name}][{url}] FAIL"):
                pass
            end_time = datetime.datetime.now()
            case_logger.error("[{}]<{}>FAIL. TIME:{}s".format(sys._getframe().f_code.co_name, url, usageTime(end_time,start_time)))
        else:
            with allure.step(f"[{mTime()}][{sys._getframe().f_code.co_name}][{url}] FAIL"):
                if pic != '':
                    self.save_capture('goto_url')
                else:
                    pass
                pass
            end_time = datetime.datetime.now()
            case_logger.info("[{}]<{}>FAIL. TIME:{}s".format(sys._getframe().f_code.co_name, url, usageTime(end_time,start_time)))
            return d


    def wait_ele_to_visible(self, loc, loc_info, func_name, timeout=TIMEOUT, frequency=FREQUENCY):
        """
        wait until locator visible
        :param loc_name: locator name
        :param loc: find element by xpath/id...
        :param loc_info: locator name and explain
        :param func_name: method name
        :param timeout: 20s
        :param frequency: 0.5s
        """
        try:
            start_time = datetime.datetime.now()
            WebDriverWait(self.driver, timeout, frequency).until(EC.visibility_of_element_located(loc))
        except Exception as e:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc} FAIL"):
                pass
            end_time = datetime.datetime.now()
            case_logger.error("[{}]<{}><{}>locator<{}>FAIL. TIME:{}s".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, usageTime(end_time,start_time)))
        else:
            end_time = datetime.datetime.now()
            case_logger.info("[{}]<{}><{}>locator<{}> TIME:{}s".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, usageTime(end_time,start_time)))

    def get_ele(self, loc_name, loc, loc_info, func_name, pic, timeout=TIMEOUT, frequency=FREQUENCY):
        """
        find element
        :param loc_name: locator name
        :param loc: find element by xpath/id...
        :param loc_info: locator name and explain
        :param func_name: method name
        :param pic: '' or None :don't take a screenshot
        :param timeout: 20s
        :param frequency: 0.5s
        :return: WebElement object
        """
        self.wait_ele_to_visible(loc, loc_info, func_name, timeout, frequency)
        try:
            start_time = datetime.datetime.now()
            ele = self.driver.find_element(*loc)
        except Exception as e:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc} FAIL"):
                pass
            end_time = datetime.datetime.now()
            case_logger.error("[{}]<{}><{}>locator<{}>FAIL. TIME:{}s".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, usageTime(end_time,start_time)))
        else:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc}"):
                if pic != '':
                    self.save_capture(loc_name)
                else:
                    pass
                pass
            end_time = datetime.datetime.now()
            case_logger.info("[{}]<{}><{}>locator<{}> TIME:{}s".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, usageTime(end_time,start_time)))
            return ele

    def get_ele_pos(self, loc_name, loc, loc_info, func_name, timeout=TIMEOUT, frequency=FREQUENCY):
        """
        find element location middle pos
        :param loc_name: locator name
        :param loc: find element by xpath/id...
        :param loc_info: locator name and explain
        :param func_name: method name
        :param timeout: 20s
        :param frequency: 0.5s
        :return: WebElement object, pos
        """
        self.wait_ele_to_visible(loc, loc_info, func_name, timeout, frequency)
        try:
            start_time = datetime.datetime.now()
            ele = self.driver.find_element(*loc)
            loca = ele.location
            lx = loca['x']
            ly = loca['y']

            size = ele.size
            h = size['height']
            hw = size['width']

            p_x = int(int(h) / 2)
            p_y = int(int(hw) / 2)

            pos_xx = int(lx) + p_y
            pos_yy = int(ly) + p_x
        except Exception as e:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc} FAIL"):
                pass
            end_time = datetime.datetime.now()
            case_logger.error("[{}]<{}><{}>locator<{}>FAIL. TIME:{}s".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, usageTime(end_time,start_time)))
        else:
            # with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc}"):
            #     pass
            return ele, (pos_xx, pos_yy)

    def get_eles(self, loc_name, loc, loc_info, func_name, pic='', timeout=TIMEOUT, frequency=FREQUENCY):
        """
        find all element
        :param loc_name: locator name
        :param loc: find element by xpath/id...
        :param loc_info: locator name and explain
        :param func_name: method name
        :param pic: '' or None :don't take a screenshot
        :param timeout: 20s
        :param frequency: 0.5s
        :return: WebElement object
        """
        self.wait_ele_to_visible(loc, loc_info, func_name, timeout, frequency)
        try:
            start_time = datetime.datetime.now()
            eles = self.driver.find_elements(*loc)
        except Exception as e:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc} FAIL"):
                pass
            end_time = datetime.datetime.now()
            case_logger.error("[{}]<{}><{}>locator<{}>FAIL. TIME:{}".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, usageTime(end_time,start_time)))
        else:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc}"):
                if pic != '':
                    self.save_capture(loc_name)
                else:
                    pass
                pass
            end_time = datetime.datetime.now()
            case_logger.error(
                "[{}]<{}><{}>locator<{}> TIME:{}".format(func_name, sys._getframe().f_code.co_name, loc_info, loc,
                                                                   usageTime(end_time, start_time)))
            return eles

    def input_text(self, loc_name, loc, loc_info, func_name, pic, text, timeout=TIMEOUT, frequency=FREQUENCY):
        """
        input text into box
        :param loc_name: locator name
        :param loc: find element by xpath/id...
        :param loc_info: locator name and explain
        :param func_name: method name
        :param pic: '' or None :don't take a screenshot
        :param text: text
        :param timeout: 20s
        :param frequency: 0.5s
        """
        ele, pos = self.get_ele_pos(loc_name, loc, loc_info, func_name, timeout, frequency)
        try:
            start_time = datetime.datetime.now()
            ele.clear()
            ele.send_keys(text)
        except Exception as e:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc} FAIL"):
                pass
            end_time = datetime.datetime.now()
            case_logger.error("[{}]<{}><{}>locator<{}>input<{}>FAIL. TIME:{}s".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, text, usageTime(end_time,start_time)))
        else:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc}input:[{text}]"):
                if pic != '':
                    self.save_capture_paint(loc_name, pos)
                else:
                    pass
                pass
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]<{}><{}>locator<{}>input<{}> TIME:{}s".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, text,
                                                                usageTime(end_time,start_time)))

    def clear_text(self, loc_name, loc, loc_info, func_name, pic='', timeout=TIMEOUT, frequency=FREQUENCY):
        """
        clear text
        :param loc_name: locator name
        :param loc: find element by xpath/id...
        :param loc_info: locator name and explain
        :param func_name: method name
        :param pic: '' or None :don't take a screenshot
        :param timeout: 20s
        :param frequency: 0.5s
        """
        ele, pos = self.get_ele_pos(loc_name, loc, loc_info, func_name, timeout, frequency)
        try:
            start_time = datetime.datetime.now()
            ele.clear()
        except Exception as e:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc} FAIL"):
                pass
            end_time = datetime.datetime.now()
            case_logger.error("[{}]<{}><{}>locator<{}>FAIL. TIME:{}".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, usageTime(end_time,start_time)))
        else:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc}"):
                if pic != '':
                    self.save_capture_paint(loc_name, pos)
                else:
                    pass
                pass
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]<{}><{}>locaator<{}> TIME:{}s".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, usageTime(end_time,start_time)))

    def click_ele(self, loc_name, loc, loc_info, func_name, pic, timeout=TIMEOUT, frequency=FREQUENCY):
        """
        click button/element
        :param loc_name: locator name
        :param loc: find element by xpath/id...
        :param loc_info: locator name and explain
        :param func_name: method name
        :param pic: '' or None :don't take a screenshot
        :param timeout: 20s
        :param frequency: 0.5s
        """
        ele, pos = self.get_ele_pos(loc_name, loc, loc_info, func_name, timeout, frequency)
        try:
            start_time = datetime.datetime.now()

            ele.click()
        except Exception as e:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc} FAIL"):
                pass
            end_time = datetime.datetime.now()
            case_logger.error("[{}]<{}><{}>locator<{}>FAIL. TIME:{}s".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, usageTime(end_time,start_time)))

        else:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc}"):
                if pic != '':
                    self.save_capture_paint(loc_name, pos)
                else:
                    pass
                pass
            end_time = datetime.datetime.now()
            case_logger.info("[{}]<{}><{}>locator<{}> TIME:{}s".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, usageTime(end_time,start_time)))

    def get_ele_text(self, loc_name, loc, loc_info, func_name, pic, timeout=TIMEOUT, frequency=FREQUENCY):
        """
        get element text
        :param loc_name: locator name
        :param loc: find element by xpath/id...
        :param loc_info: locator name and explain
        :param func_name: method name
        :param pic: '' or None :don't take a screenshot
        :param timeout: 20s
        :param frequency: 0.5s
        :return: text value
        """
        ele, pos = self.get_ele_pos(loc_name, loc, loc_info, func_name, timeout, frequency)
        try:
            start_time = datetime.datetime.now()
            text = ele.text
        except Exception as e:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc} FAIL"):
                pass
            end_time = datetime.datetime.now()
            case_logger.error("[{}]<{}><{}>locator<{}>FAIL. TIME:{}s".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, usageTime(end_time,start_time), e))
        else:
            with allure.step(f"[{mTime()}][{func_name}][{loc_info}]{loc}return value:[{text}]"):

                if pic != '':
                    print(pic + '111111')
                    self.save_capture_paint(loc_name, pos)
                else:
                    pass
                pass
            end_time = datetime.datetime.now()
            case_logger.info("[{}]<{}><{}>locator<{}>value:[{}] TIME:{}".format(func_name, sys._getframe().f_code.co_name, loc_info, loc, text, usageTime(end_time,start_time)))
            return text
































    # def get_eles_text(self, loc, loc_info, img_doc, m, timeout=TIMEOUT, frequency=FREQUENCY):
    #     """
    #     获取WebElement对象的所有文本值
    #     :param loc: 元素定位的XPATH元组表达式
    #     :param img_doc: 截图说明
    #     :param timeout: 等待的超时时间
    #     :param frequency: 轮询频率
    #     :return: WebElement对象的文本值的列表
    #     """
    #     self.wait_ele_to_visible(loc_name, loc, loc_info, func_name, timeout, frequency)
    #     try:
    #         # all_text = self.get_eles(loc, img_doc)
    #         case_logger.info("[{}]<{}>获取元素<{}>的所有文本值".format(m, sys._getframe().f_code.co_name, loc_info))
    #         all_text = self.driver.find_elements(*loc).text
    #         text_list = []
    #         for one_text in all_text:
    #             text_list.append(one_text.text)
    #     except Exception as e:
    #         case_logger.error("[{}]<{}>获取元素<{}>的所有文本值失败！ERROR : {}".format(m, sys._getframe().f_code.co_name, loc_info, e))
    #         self.save_capture(img_doc)
    #         raise e
    #         # case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))
    #     else:
    #         case_logger.info("[{}]<{}>返回值为<{}>".format(m, sys._getframe().f_code.co_name, text_list))
    #         return text_list
    #
    # def get_ele_attr(self, attr_name, loc, loc_info, img_doc, m, timeout=TIMEOUT, frequency=FREQUENCY):
    #     """
    #     获取WebElement对象的属性值
    #     :param attr_name: 属性名称
    #     :param loc: 元素定位的XPATH元组表达式
    #     :param img_doc: 截图说明
    #     :param timeout: 等待的超时时间
    #     :param frequency: 轮询频率
    #     :return: WebElement对象的属性值
    #     """
    #     self.wait_element_to_be_exist(loc_name, loc, loc_info, func_name, timeout, frequency)
    #     try:
    #         # value = self.get_ele(loc, img_doc).get_attribute(attr_name)
    #         case_logger.info("[{}]<{}>获取元素<{}>的属性<{}>的值".format(m, sys._getframe().f_code.co_name, loc_info, attr_name))
    #         value = self.driver.find_element(*loc).get_attribute(attr_name)
    #     except Exception as e:
    #         case_logger.error("[{}]<{}>获取元素<{}>的属性<{}>的值失败！".format(m, sys._getframe().f_code.co_name, loc_info, attr_name))
    #         self.save_capture(img_doc)
    #         case_logger.error("[{}]<{}>错误信息<{}>".format(m, sys._getframe().f_code.co_name, e))
    #         raise e
    #     else:
    #         case_logger.info("[{}]<{}>获取到的元素属性值为<{}>".format(m, sys._getframe().f_code.co_name, value))
    #         return value
    #
    # def switch_to_frame(self, loc, img_doc, timeout=TIMEOUT, frequency=FREQUENCY):
    #     """
    #     切换iframe页面
    #     :param loc: 元素定位的XPATH元组表达式
    #     :param img_doc: 截图说明
    #     :param timeout: 等待的超时时间
    #     :param frequency: 轮询频率
    #     :return:
    #     """
    #     try:
    #         case_logger.info("<{}>在{}中根据元素<{}>进行iframe切换".format(sys._getframe().f_code.co_name, img_doc, loc))
    #         start_time = time.time()
    #         WebDriverWait(self.driver, timeout, frequency).until(EC.frame_to_be_available_and_switch_to_it(loc))
    #     except Exception as e:
    #         case_logger.error("<{}>在{}中根据元素<{}>进行iframe切换失败！".format(sys._getframe().f_code.co_name, img_doc, loc))
    #         self.save_capture(img_doc)
    #
    #         case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))
    #         raise e
    #     else:
    #         end_time = time.time()
    #         case_logger.info("<{}>在{}中根据元素<{}>进行iframe切换，等待时间：{}秒".
    #                          format(sys._getframe().f_code.co_name, img_doc, loc, round(end_time - start_time, 2)))
    #
    # def switch_to_default_content(self, img_doc):
    #     """
    #     切换iframe到main页面
    #     :param img_doc: 截图说明
    #     :return:
    #     """
    #     try:
    #         case_logger.info(f"<{sys._getframe().f_code.co_name}>切换iframe到main页面")
    #         self.driver.switch_to.default_content()
    #     except Exception as e:
    #         case_logger.error(f"<{sys._getframe().f_code.co_name}>切换iframe到main页面失败！")
    #         self.save_capture(img_doc)
    #
    #         case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))
    #         raise e
    #
    # def switch_to_parent(self, img_doc):
    #     """
    #     切换iframe到上一层页面
    #     :param img_doc: 截图说明
    #     :return:
    #     """
    #     try:
    #         case_logger.info(f"<{sys._getframe().f_code.co_name}>切换iframe到上一层页面")
    #         self.driver.switch_to.parent_frame()
    #     except Exception as e:
    #         case_logger.error(f"<{sys._getframe().f_code.co_name}>切换iframe到上一层页面失败！")
    #         self.save_capture(img_doc)
    #
    #         case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))
    #         raise e
    #
    # # def upload_file(self, filename, img_doc, browser_type="chrome"):
    # #     """
    # #     非input标签的文件上传
    # #     :param filename: 文件名（绝对路径）
    # #     :param img_doc: 截图说明
    # #     :param browser_type: 浏览器类型
    # #     :return:
    # #     """
    # #     try:
    # #         case_logger.info("上传文件（{}）".format(filename))
    # #         time.sleep(2)
    # #         upload(filePath=filename, browser_type=browser_type)
    # #     except Exception as e:
    # #         case_logger.error("上传文件（{}）失败！".format(filename))
    # #         self.save_screenshot(img_doc)
    # #         raise e
    # #     else:
    # #         time.sleep(2)
    #
    # def suspend_mouse(self, loc, img_doc, timeout=TIMEOUT, frequency=FREQUENCY):
    #     """
    #     鼠标悬浮
    #     :param loc: 元素定位的XPATH元组表达式
    #     :param img_doc: 截图说明
    #     :param timeout: 等待的超时时间
    #     :param frequency: 轮询频率
    #     :return:
    #     """
    #     try:
    #         case_logger.info("<{}>在{}上根据元素<{}>进行悬浮".format(sys._getframe().f_code.co_name, img_doc, loc))
    #         self.wait_ele_to_click(loc, img_doc, timeout, frequency)
    #         # ele = self.get_ele(loc, img_doc)
    #         ele = self.driver.find_element(*loc)
    #         ActionChains(self.driver).move_to_element(ele).perform()
    #     except Exception as e:
    #         case_logger.error("<{}>在{}上根据元素<{}>进行悬浮失败！".format(sys._getframe().f_code.co_name, img_doc, loc))
    #         self.save_capture(img_doc)
    #         case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))
    #         raise e
    #
    # def alert_close(self, img_doc, alert_type='alert', text=None, timeout=TIMEOUT, frequency=FREQUENCY):
    #     """
    #     弹框关闭
    #     :param img_doc: 截图说明
    #     :param alert_type: 弹框类型：alert/confirm/prompt
    #     :param text: prompt弹框输入的文本
    #     :param timeout: 等待的超时时间
    #     :param frequency: 轮询频率
    #     :return:
    #     """
    #     try:
    #         case_logger.info("<{}>在{}中切换并关闭{}类型的弹框".format(sys._getframe().f_code.co_name, img_doc, alert_type))
    #         start_time = time.time()
    #         WebDriverWait(self.driver, timeout, frequency).until(EC.alert_is_present())
    #         if alert_type in ['alert', 'confirm']:
    #             self.driver.switch_to.alert.accept()
    #         elif alert_type == 'prompt':
    #             self.driver.switch_to.alert.send_keys(text)
    #             self.driver.switch_to.alert.accept()
    #         else:
    #             case_logger.error("<{}>不支持{},请确认alert的类型".format(sys._getframe().f_code.co_name, alert_type))
    #     except Exception as e:
    #         case_logger.error("<{}>在{}中切换并关闭{}类型的弹框失败！".format(sys._getframe().f_code.co_name, img_doc, alert_type))
    #         self.save_capture(img_doc)
    #         case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))
    #         raise e
    #     else:
    #         end_time = time.time()
    #         case_logger.info("<{}>在{}中切换并关闭{}类型的弹框，等待时间：{}秒".
    #                          format(sys._getframe().f_code.co_name, img_doc, alert_type, round(end_time - start_time, 2)))
    #
    # def select_action(self, loc, img_doc, content, select_type, timeout=TIMEOUT, frequency=FREQUENCY):
    #     """
    #     Select操作
    #     :param loc: 元素定位的XPATH元组表达式
    #     :param img_doc: 截图说明
    #     :param content: select_by_方法的入参
    #     :param select_type: select类型
    #     :param timeout: 等待的超时时间
    #     :param frequency: 轮询频率
    #     :return:
    #     """
    #     self.wait_ele_to_click(loc, img_doc, timeout, frequency)
    #     try:
    #         case_logger.info("<{}>在{}上根据元素<{}>以{}方式进行下拉选择".format(sys._getframe().f_code.co_name, img_doc, loc, select_type))
    #         ele = self.get_ele(loc, img_doc)
    #         if select_type == 'index':
    #             Select(ele).select_by_index(content)
    #         elif select_type == 'value':
    #             Select(ele).select_by_value(content)
    #         elif select_type == 'text':
    #             Select(ele).select_by_visible_text(content)
    #         else:
    #             case_logger.error("<{}>不支持{},请确认Select的类型".format(sys._getframe().f_code.co_name, select_type))
    #     except Exception as e:
    #         case_logger.error("<{}>在{}上根据元素<{}>以{}方式进行下拉选择失败！".format(sys._getframe().f_code.co_name, img_doc, loc, select_type))
    #         self.save_capture(img_doc)
    #         case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))
    #         raise e
    #
    # def switch_to_windows(self, loc, img_doc, timeout=TIMEOUT, frequency=FREQUENCY):
    #     """
    #     窗口切换
    #     :param loc: 元素定位的XPATH元组表达式
    #     :param img_doc: 截图说明
    #     :param timeout: 等待的超时时间
    #     :param frequency: 轮询频率
    #     :return:
    #     """
    #     try:
    #         case_logger.info("<{}>在{}中根据元素<{}>进行窗口切换".format(sys._getframe().f_code.co_name, img_doc, loc))
    #         cur_handles = self.driver.window_handles  # 获取点击之前的窗口总数
    #         start_time = time.time()
    #         self.click_ele(loc, img_doc, timeout, frequency)  # 点击按钮后新的窗口出现
    #         WebDriverWait(self.driver, timeout, frequency).until(EC.new_window_is_opened(cur_handles))
    #         wins = self.driver.window_handles  # 再次获取窗口总数
    #         self.driver.switch_to.window(wins[-1])  # 切换到新的页面
    #     except Exception as e:
    #         case_logger.error("<{}>在{}中根据元素<{}>进行窗口切换失败！".format(sys._getframe().f_code.co_name, img_doc, loc))
    #         self.save_capture(img_doc)
    #         case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))
    #         raise e
    #     else:
    #         end_time = time.time()
    #         case_logger.info("<{}>在{}中根据元素<{}>进行窗口切换，等待时间：{}秒".
    #                          format(sys._getframe().f_code.co_name, img_doc, loc, round(end_time - start_time, 2)))
    #
    #
    # def wait_ele_to_click(self, loc, loc_info, img_doc, timeout=TIMEOUT, frequency=FREQUENCY):
    #     """
    #     等待元素可点击
    #     :param loc: 元素定位的XPATH元组表达式
    #     :param img_doc: 截图说明
    #     :param timeout: 等待的超时时间
    #     :param frequency: 轮询频率
    #     :return:
    #     """
    #     try:
    #         case_logger.info("[{}]<{}>开始等待页面元素<{}>是否可点击！".format(img_doc, sys._getframe().f_code.co_name, loc))
    #         start_time = datetime.datetime.now()
    #         WebDriverWait(self.driver, timeout, frequency).until(EC.element_to_be_clickable(*loc))
    #     except Exception as e:
    #         case_logger.error("[{}]<{}>页面元素<{}>等待可点击失败！".format(img_doc, sys._getframe().f_code.co_name, loc))
    #         self.save_capture(img_doc)
    #         case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))
    #         raise e
    #     else:
    #         end_time = datetime.datetime.now()
    #         case_logger.info("[{}]<{}>页面元素<{}>等待可点击，等待时间：{}s ".format(img_doc, sys._getframe().f_code.co_name, loc, usageTime(end_time,start_time)))
    #
    # def wait_element_to_be_exist(self, loc, img_doc, timeout=TIMEOUT, frequency=FREQUENCY):
    #     """
    #     等待元素存在
    #     :param loc: 元素定位的XPATH元组表达式
    #     :param img_doc: 截图说明
    #     :param timeout: 等待的超时时间
    #     :param frequency: 轮询频率
    #     :return:
    #     """
    #     try:
    #         case_logger.info("[{}]<{}>开始等待页面元素<{}>是否存在！".format(img_doc, sys._getframe().f_code.co_name, loc))
    #         start_time = datetime.datetime.now()
    #         WebDriverWait(self.driver, timeout, frequency).until(EC.presence_of_element_located(*loc))
    #     except Exception as e:
    #         case_logger.error("[{}]<{}>页面元素<{}>等待存在失败！".format(img_doc, sys._getframe().f_code.co_name, loc))
    #         self.save_capture(img_doc)
    #         case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))
    #         raise e
    #     else:
    #         end_time = datetime.datetime.now()
    #         case_logger.info("[{}]<{}>页面元素<{}>等待存在，等待时间：{}s ".format(img_doc, sys._getframe().f_code.co_name, loc, usageTime(end_time,start_time)))
