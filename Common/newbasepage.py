import time, sys, datetime, cv2, os, platform
import allure, inspect
from functools import wraps
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from Common.handle_logger import logger as case_logger
from Common.setting import PIC_DIR, FREQUENCY, TIMEOUT, RELATIVE_DIR
from Common.utils import usageTime, mTime

from appium.webdriver.common.mobileby import MobileBy



LOCATOR_LIST = {
    # selenium
    'css': By.CSS_SELECTOR,
    'id_': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_name': By.CLASS_NAME,
    # appium
    'ios': MobileBy.IOS_PREDICATE
}


class PageObject(object):
    """
    Page Object pattern.
    """

    def __init__(self, driver):
        """
        :param: driver `selenium.webdriver.WebDriver` Selenium webdriver instance
        """
        self.driver = driver

    def goto(self, url):
        """
        :param:  url
        """
        self.driver.get(url)
        # self.driver.implicitly_wait(5)

    def save_capture_ob(self, loc_name):
        """
        take a screenshot
        :param loc_name: capture name
        """
        loc_name = loc_name.replace(' ', '_').replace('　', '_')
        time.sleep(0.01)
        start_time = datetime.datetime.now()
        file_name = os.path.join(PIC_DIR, f'{time.strftime("%Y%m%d_%H%M%S", time.localtime())}_{loc_name}.png')
        relative_name = os.path.join(RELATIVE_DIR + f'{time.strftime("%Y%m%d_%H%M%S", time.localtime())}_{loc_name}.png')
        try:
            self.driver.save_screenshot(file_name)
            with open(file_name, mode='rb') as f:
                file = f.read()
            allure.attach(file, loc_name, allure.attachment_type.PNG)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]{},time:{}".format(sys._getframe().f_code.co_name, relative_name, usageTime(end_time, start_time)))
        except Exception as e:
            with allure.step(f"[{mTime()}][FAIL][{sys._getframe().f_code.co_name}][{loc_name}]"):
                print(e)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]{},time:{}".format(sys._getframe().f_code.co_name, relative_name, usageTime(end_time, start_time)))
        else:
            return file_name


def kb_info(func):
    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        with allure.step(f"[{mTime()}][Method:{func.__name__}]"):
            pass
        case_logger.info(f"[Method:{func.__name__}]")
        return result
    return inner



class Element(object):
    """
    BasePage class
    """

    def __init__(self, info="undefined", index=0, **kwargs):
        self.index = index
        self.desc = info
        self.context = None
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        self.k, self.v = next(iter(kwargs.items()))

        if self.k not in LOCATOR_LIST.keys():
            raise ValueError("Element positioning of type '{}' is not supported.".format(self.k))
        self.locator = (LOCATOR_LIST[self.k], self.v)



    def __get__(self, instance, owner):
        if instance is None:
            return None
        self.context = instance.driver
        return self

    def __set__(self, instance, value):
        self.__get__(instance, instance.__class__)
        # ele.send_keys(value)

    def _get_element(self):
        """
        Find if the element exists.
        """
        elems = self.context.find_elements(*self.locator)
        if len(elems) == 1:
            pass
        elif len(elems) > 1:
            case_logger.info("❓ Find '{n}' elements : {loc}".format(
                n=len(elems), loc=self.locator))
        else:
            case_logger.info("❌ Find '0' elements : {loc}".format(loc=self.locator))
            return elems
        return elems[self.index]

    def wait_ele_to_visible(self, timeout=TIMEOUT, frequency=FREQUENCY):
        """
        wait until locator visible
        :param timeout: 5s
        :param frequency: 0.5s
        """
        func = sys._getframe().f_code.co_name
        start_time = datetime.datetime.now()
        try:
            WebDriverWait(self.context, timeout, frequency).until(EC.visibility_of_element_located(self.locator))
        except Exception as e:
            with allure.step(f"[{mTime()}][FAIL][{func}][{self.desc}][{self.locator}]"):
                self.__return_value(e)
            end_time = datetime.datetime.now()
            case_logger.error(
                "[FAIL][{}]<{}>,locator:<{}>,time:{}s".format(func, self.desc, self.locator,
                                                               usageTime(end_time, start_time)))
        else:
            end_time = datetime.datetime.now()
            with allure.step(f"[{mTime()}][{func}][{self.desc}][{self.locator}]"):
                pass
            case_logger.info(
                "[{}]<{}>,locator:<{}>,time:{}s".format(func, self.desc, self.locator, usageTime(end_time, start_time)))

    def wait_ele_to_not_visible(self, timeout=TIMEOUT, frequency=FREQUENCY):
        """
        wait until locator visible
        :param timeout: 5s
        :param frequency: 0.5s
        """
        func = sys._getframe().f_code.co_name
        start_time = datetime.datetime.now()
        try:
            WebDriverWait(self.context, timeout, frequency).until_not(EC.visibility_of_element_located(self.locator))
        except Exception as e:
            with allure.step(f"[{mTime()}][FAIL][{func}][{self.desc}][{self.locator}]"):
                self.__return_value(e)
            end_time = datetime.datetime.now()
            case_logger.error(
                "[FAIL][{}]<{}>,locator:<{}>,time:{}s".format(func, self.desc, self.locator,
                                                               usageTime(end_time, start_time)))
        else:
            end_time = datetime.datetime.now()
            with allure.step(f"[{mTime()}][{func}][{self.desc}][{self.locator}]"):
                pass
            case_logger.info(
                "[{}]<{}>,locator:<{}>,time:{}s".format(func, self.desc, self.locator, usageTime(end_time, start_time)))


    def ele_input_text(self, text, pic='', timeout=TIMEOUT, frequency=FREQUENCY):
        """
        input text into box
        :param text: text
        :param pic: '' or None :don't take a screenshot
        :param timeout: 20s
        :param frequency: 0.5s
        """
        func = sys._getframe().f_code.co_name
        start_time = datetime.datetime.now()
        try:

            ele = self._get_element()
            # ele.clear()
            ele.send_keys(text)
            self.context.execute_script("arguments[0].setAttribute('style',arguments[1]);", ele, 'border:2px solid red;')
        except Exception as e:
            with allure.step(f"[{mTime()}][FAIL][{func}][{self.desc}][{self.locator}],input:[{text}]"):
                self.__return_value(e)
            end_time = datetime.datetime.now()
            case_logger.error(
                "[FAIL][{}]<{}>,locator:<{}>,time:{}s".format(func, self.desc, self.locator,
                                                               usageTime(end_time, start_time)))
        else:
            with allure.step(f"[{mTime()}][{func}][{self.desc}][{self.locator}],input:[{text}]"):
                if pic != '':
                    self.save_capture(self.desc)
            self.context.execute_script("arguments[0].removeAttribute('style')", ele)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]<{}>,locator:<{}>,input:<{}>,time:{}s".format(func, self.desc, self.locator,
                                                               text, usageTime(end_time, start_time)))

    def ele_clear(self, pic='', timeout=TIMEOUT, frequency=FREQUENCY):
        """
        input text into box
        :param text: text
        :param pic: '' or None :don't take a screenshot
        :param timeout: 20s
        :param frequency: 0.5s
        """
        func = sys._getframe().f_code.co_name
        start_time = datetime.datetime.now()
        try:
            ele = self._get_element()
            self.context.execute_script("arguments[0].setAttribute('style',arguments[1]);", ele,
                                        'border:2px solid red;')
            ele.clear()
        except Exception as e:
            with allure.step(f"[{mTime()}][FAIL][{func}][{self.desc}][{self.locator}]"):
                self.__return_value(e)
            end_time = datetime.datetime.now()
            case_logger.error(
                "[FAIL][{}]<{}>,locator:<{}>,time:{}s".format(func, self.desc, self.locator,
                                                               usageTime(end_time, start_time)))
        else:
            with allure.step(f"[{mTime()}][{func}][{self.desc}][{self.locator}]"):
                if pic != '':
                    self.save_capture(self.desc)
            self.context.execute_script("arguments[0].removeAttribute('style')", ele)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]<{}>,locator:<{}>,time:{}s".format(func, self.desc, self.locator,
                                                               usageTime(end_time, start_time)))


    def ele_click(self, pic='', timeout=TIMEOUT, frequency=FREQUENCY):
        """
        input text into box
        :param text: text
        :param pic: '' or None :don't take a screenshot
        :param timeout: 20s
        :param frequency: 0.5s
        """
        func = sys._getframe().f_code.co_name
        start_time = datetime.datetime.now()
        try:
            ele = self._get_element()
            self.context.execute_script("arguments[0].setAttribute('style',arguments[1]);", ele,
                                        'border:2px solid red;')
            with allure.step(f"[{mTime()}][{func}][{self.desc}][{self.locator}]"):
                if pic != '':
                    self.save_capture(self.desc)
            ele.click()
        except Exception as e:
            with allure.step(f"[{mTime()}][FAIL][{func}][{self.desc}][{self.locator}]"):
                self.__return_value(e)
            end_time = datetime.datetime.now()
            case_logger.error(
                "[FAIL][{}]<{}>,locator:<{}>,time:{}s".format(func, self.desc, self.locator,
                                                               usageTime(end_time, start_time)))
        else:
            self.context.execute_script("arguments[0].removeAttribute('style')", ele)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]<{}>,locator:<{}>,time:{}s".format(func, self.desc, self.locator,
                                                               usageTime(end_time, start_time)))

    def ele_get_element(self, pic='', timeout=TIMEOUT, frequency=FREQUENCY):
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
        func = sys._getframe().f_code.co_name
        start_time = datetime.datetime.now()
        try:
            ele = self._get_element()
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
            self.context.execute_script("arguments[0].setAttribute('style',arguments[1]);", ele,
                                        'border:2px solid red;')
        except Exception as e:
            with allure.step(f"[{mTime()}][FAIL][{func}][{self.desc}][{self.locator}]"):
                self.__return_value(e)
            end_time = datetime.datetime.now()
            case_logger.error(
                "[FAIL][{}]<{}>,locator:<{}>,time:{}s".format(func, self.desc, self.locator,
                                                               usageTime(end_time, start_time)))
        else:
            with allure.step(f"[{mTime()}][{func}][{self.desc}][{self.locator}]"):
                self.__return_value(ele)
                if pic != '':
                    self.save_capture(self.desc)
            self.context.execute_script("arguments[0].removeAttribute('style')", ele)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]<{}>,locator:<{}>,pos<{}>,element:<{}>,time:{}s".format(func, self.desc, self.locator, (pos_xx, pos_yy),
                                                                           ele, usageTime(end_time, start_time)))
            return ele, (pos_xx, pos_yy)

    def ele_get_text(self, pic='', timeout=TIMEOUT, frequency=FREQUENCY):
        """
        input text into box
        :param text: text
        :param pic: '' or None :don't take a screenshot
        :param timeout: 20s
        :param frequency: 0.5s
        """
        func = sys._getframe().f_code.co_name
        start_time = datetime.datetime.now()
        try:

            ele = self._get_element()
            text = ele.text
            self.context.execute_script("arguments[0].setAttribute('style',arguments[1]);", ele,
                                        'border:2px solid red;')
        except Exception as e:
            with allure.step(f"[{mTime()}][FAIL][{func}][{self.desc}][{self.locator}]"):
                self.__return_value(e)
            end_time = datetime.datetime.now()
            case_logger.error(
                "[FAIL][{}]<{}>,locator:<{}>,time:{}s".format(func, self.desc, self.locator,
                                                               usageTime(end_time, start_time)))
        else:
            with allure.step(f"[{mTime()}][{func}][{self.desc}][{self.locator}]"):
                self.__return_value(text)
                if pic != '':
                    self.save_capture(self.desc)
            self.context.execute_script("arguments[0].removeAttribute('style')", ele)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]<{}>,locator:<{}>,return:<{}>time:{}s".format(func, self.desc, self.locator, text,
                                                               usageTime(end_time, start_time)))
            return text

    def __return_value(self, value):
        with allure.step(f"VALUE:[{value}]"):
            pass

    def save_capture(self, loc_name):
        """
        take a screenshot
        :param loc_name: capture name
        """
        loc_name = loc_name.replace(' ', '_').replace('　', '_')
        time.sleep(0.01)
        start_time = datetime.datetime.now()
        file_name = os.path.join(PIC_DIR, f'{time.strftime("%Y%m%d_%H%M%S", time.localtime())}_{loc_name}.png')
        relative_name = os.path.join(RELATIVE_DIR + f'{time.strftime("%Y%m%d_%H%M%S", time.localtime())}_{loc_name}.png')
        try:
            self.context.save_screenshot(file_name)
            with open(file_name, mode='rb') as f:
                file = f.read()
            allure.attach(file, loc_name, allure.attachment_type.PNG)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]{},time:{}".format(sys._getframe().f_code.co_name, relative_name, usageTime(end_time, start_time)))
        except Exception as e:
            with allure.step(f"[{mTime()}][FAIL][{sys._getframe().f_code.co_name}][{loc_name}]"):
                self.__return_value(e)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]{},time:{}".format(sys._getframe().f_code.co_name, relative_name, usageTime(end_time, start_time)))


    def save_capture_paint(self, loc_name, pos):
        """
        screenshot with paint pos
        :param img_doc: capture name
        :param pos: element location
        """
        loc_name = loc_name.replace(' ', '_').replace('　', '_')
        time.sleep(0.01)
        start_time = datetime.datetime.now()
        file_name = os.path.join(PIC_DIR, f'{time.strftime("%Y%m%d_%H%M%S", time.localtime())}_{loc_name}.png')
        relative_name = os.path.join(RELATIVE_DIR + f'{time.strftime("%Y%m%d_%H%M%S", time.localtime())}_{loc_name}.png')
        try:
            self.context.save_screenshot(file_name)
            screenvc = cv2.imread(file_name)
            img_res = cv2.circle(screenvc, pos, 15, (0, 0, 225), 2)
            cv2.imwrite(file_name, img_res)

            with open(file_name, mode='rb') as f:
                file = f.read()
            allure.attach(file, loc_name, allure.attachment_type.PNG)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]{},time:{}".format(sys._getframe().f_code.co_name, relative_name, usageTime(end_time, start_time)))
        except Exception as e:
            with allure.step(f"[{mTime()}][FAIL][{sys._getframe().f_code.co_name}][{loc_name}]"):
                self.__return_value(e)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]{},time:{}".format(sys._getframe().f_code.co_name, relative_name, usageTime(end_time, start_time)))




    def ele_get_attr_value(self, attr_name, pic='', timeout=TIMEOUT, frequency=FREQUENCY):
        """
        input text into box
        :param text: text
        :param pic: '' or None :don't take a screenshot
        :param timeout: 20s
        :param frequency: 0.5s
        """
        func = sys._getframe().f_code.co_name
        start_time = datetime.datetime.now()
        try:

            ele = self._get_element()
            self.context.execute_script("arguments[0].setAttribute('style',arguments[1]);", ele,
                                        'border:2px solid red;')
            attr_value = ele.get_attribute(attr_name)
        except Exception as e:
            with allure.step(f"[{mTime()}][FAIL][{func}][{self.desc}][{self.locator}]"):
                self.__return_value(e)
            end_time = datetime.datetime.now()
            case_logger.error(
                "[FAIL][{}]<{}>,locator:<{}>,time:{}s".format(func, self.desc, self.locator,
                                                              usageTime(end_time, start_time)))
        else:
            with allure.step(f"[{mTime()}][{func}][{self.desc}][{self.locator}][ele attr:{attr_value}]"):
                pass
                if pic != '':
                    self.save_capture(self.desc)
            self.context.execute_script("arguments[0].removeAttribute('style')", ele)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]<{}>,locator:<{}>,return:<{}>time:{}s".format(func, self.desc, self.locator, attr_value,
                                                                   usageTime(end_time, start_time)))
            return attr_value

    @kb_info
    def kb_enter(self):
        ele = self._get_element()
        ele.send_keys(Keys.ENTER)

    @kb_info
    def kb_select_all(self):
        ele = self._get_element()
        if platform.system().lower() == "darwin":
            ele.send_keys(Keys.COMMAND, "a")
        else:
            ele.send_keys(Keys.CONTROL, "a")

    @kb_info
    def kb_cut(self):
        ele = self._get_element()
        if platform.system().lower() == "darwin":
            ele.send_keys(Keys.COMMAND, "x")
        else:
            ele.send_keys(Keys.CONTROL, "x")

    @kb_info
    def kb_copy(self):
        ele = self._get_element()
        if platform.system().lower() == "darwin":
            ele.send_keys(Keys.COMMAND, "c")
        else:
            ele.send_keys(Keys.CONTROL, "c")

    @kb_info
    def kb_paste(self):
        ele = self._get_element()
        if platform.system().lower() == "darwin":
            ele.send_keys(Keys.COMMAND, "v")
        else:
            ele.send_keys(Keys.CONTROL, "v")

    @kb_info
    def kb_backspace(self):
        ele = self._get_element()
        ele.send_keys(Keys.BACKSPACE)

    @kb_info
    def kb_delete(self):
        ele = self._get_element()
        ele.send_keys(Keys.DELETE)

    @kb_info
    def kb_tab(self):
        ele = self._get_element()
        ele.send_keys(Keys.TAB)

    @kb_info
    def kb_space(self):
        ele = self._get_element()
        ele.send_keys(Keys.SPACE)







class Elements(object):
    """
    BasePage class
    """

    def __init__(self, info="undefined", index='ALL', **kwargs):
        self.index = index
        self.desc = info
        self.context = None
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        self.k, self.v = next(iter(kwargs.items()))

        if self.k not in LOCATOR_LIST.keys():
            raise ValueError("Element positioning of type '{}' is not supported.".format(self.k))
        self.locator = (LOCATOR_LIST[self.k], self.v)

    def __get__(self, instance, owner):
        if instance is None:
            return None
        self.context = instance.driver
        return self

    def __set__(self, instance, value):
        self.__get__(instance, instance.__class__)
        # ele.send_keys(value)

    def _get_elements(self):
        """
        Find if the element exists.
        """
        elems = self.context.find_elements(*self.locator)
        if len(elems) == 1:
            case_logger.info("❓ Find '1' element: {loc} ".format(loc=self.locator))
        elif len(elems) > 1:
            if str(self.index).isdigit():
                elems = [elems[int(self.index)]]
        else:
            case_logger.info("❌ Find '0' element : {loc}").format(loc=self.locator)
            return elems
        return elems

    def eles_get_elements(self, timeout=TIMEOUT, frequency=FREQUENCY):
        """
        find element location middle pos
        :param loc_name: locator name
        :param loc: find element by xpath/id...
        :param loc_info: locator name and explain
        :param func_name: method name
        :param timeout: 20s
        :param frequency: 0.5s
        :return: WebElement对象的文本值的列表
        :return: WebElement对象的文本值的列表 长度
        """
        func = sys._getframe().f_code.co_name
        start_time = datetime.datetime.now()
        try:
            eles = self._get_elements()
        except Exception as e:
            with allure.step(f"[{mTime()}][FAIL][{func}][{self.desc}][{self.locator}][self.index[{self.index}]]"):
                self.__return_value(e)
            end_time = datetime.datetime.now()
            case_logger.error(
                "[FAIL][{}]<{}>,locator:<{}>,[self.index[{}]],time:{}s".format(func, self.desc, self.locator,
                                                               self.index, usageTime(end_time, start_time)))
        else:
            with allure.step(f"[{mTime()}][{func}][{self.desc}][{self.locator}][self.index[{self.index}]]"):
                self.__return_value(eles)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]<{}>,locator:<{}>,<self.index[{}]>,time:{}s".format(func, self.desc, self.locator, self.index, usageTime(end_time, start_time)))
            case_logger.info('[{}]elements:<{}>'.format(func, eles))
            return eles, len(eles)

    def __return_value(self, value):
        with allure.step(f"VALUE:[{value}]"):
            pass




    def eles_get_elements_text(self, timeout=TIMEOUT, frequency=FREQUENCY):
        """
        获取WebElement对象的所有文本值
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return: WebElement对象的文本值的列表
        :return: WebElement对象的文本值的列表 长度
        """
        func = sys._getframe().f_code.co_name
        start_time = datetime.datetime.now()
        try:
            eles = self._get_elements()
            text_list = []
            for one_ele in eles:
                text_list.append(one_ele.text)
        except Exception as e:
            with allure.step(
                    f"[{mTime()}][FAIL][{func}][{self.desc}][{self.locator}][self.index[{self.index}]]"):
                self.__return_value(e)
            end_time = datetime.datetime.now()
            case_logger.error(
                "[FAIL][{}]<{}>,locator:<{}>,[self.index[{}]],time:{}s".format(func, self.desc, self.locator,
                                                                               self.index,
                                                                               usageTime(end_time, start_time)))
        else:
            with allure.step(f"[{mTime()}][{func}][{self.desc}][{self.locator}][self.index[{self.index}]]"):
                self.__return_value(text_list)
            end_time = datetime.datetime.now()
            case_logger.info(
                "[{}]<{}>,locator:<{}>,<self.index[{}]>,time:{}s".format(func, self.desc, self.locator,
                                                                         self.index,
                                                                         usageTime(end_time, start_time)))
            case_logger.info('[{}]elements:<{}>'.format(func, text_list))
            return text_list, len(eles)





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
