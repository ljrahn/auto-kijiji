from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from utilities.utils import *
import logging
import time
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger(__name__)


class SeleniumUIActions:
    """Uses selenium library to ineract with web elements. This is a base level page interaction module that is called
    by page_objects modules. Common method params:
    :param locator: configurable string to be 'xpath', 'css_selector', 'link_text', 'id', and defines the type of
    locator being used to locate the element
    :param element: The element to be controlled. if xpath, example form would be '//div[@class="ant-card"]'. Example
    would scroll to this element, click this element, etc.
    :param wait_time: set to True to explicitly wait for element for time specified in config file, set to int or float
    in seconds to wait for specific time"""
    def __init__(self, driver):
        self.driver = driver
        self.timeout_value = 10

    def wait_for_items_in_wrapper(self, wrapper=None, items=None, wait_time=True):
        """Waits for a list of text elements within a given xpath wrapper element.
        :param wrapper: xpath element whose html wrapps the text items
        :param items: a list of text elements to wait for visibility"""
        try:
            if wait_time is True:
                wait_time = self.timeout_value

            all_elements_ec = [EC.visibility_of_all_elements_located((By.XPATH, wrapper.format(element))) for element in
                               items]
            WebDriverWait(self.driver, float(wait_time)).until(_wait_for_all(*all_elements_ec))
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise
        except exceptions.ElementClickInterceptedException:
            self._get_exception_message('click_intercepted')
            raise

    def wait_for_element_visibility(self, locator='xpath', element=None, wait_time=True):
        """Wait for an elements visibility
        :param element: Additionally you can pass a list of elements to wait for multiple items elements to be visible
        on the page"""
        locator = self._get_locator(locator)
        if wait_time is True:
            wait_time = self.timeout_value
        try:
            if isinstance(element, list):
                all_elements_ec = [EC.presence_of_element_located((locator, all_elements)) for all_elements in element]
                WebDriverWait(self.driver, float(wait_time)).until(_wait_for_all(*all_elements_ec))
            else:
                WebDriverWait(self.driver, float(wait_time)).until(
                    EC.visibility_of_element_located((locator, element)))
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise
        except exceptions.ElementClickInterceptedException:
            self._get_exception_message('click_intercepted')
            raise
        time.sleep(0.15)

    def wait_for_element_invisibility(self, locator='xpath', element=None, wait_time=True):
        """Wait for an elements visibility
        :param element: Additionally you can pass a list of elements to wait for multiple items elements to be visible
        on the page"""
        locator = self._get_locator(locator)
        if wait_time is True:
            wait_time = self.timeout_value
        try:
            if isinstance(element, list):
                all_elements_ec = [EC.invisibility_of_element_located((locator, all_elements)) for all_elements in element]
                WebDriverWait(self.driver, float(wait_time)).until(_wait_for_all(*all_elements_ec))
            else:
                WebDriverWait(self.driver, float(wait_time)).until(
                    EC.invisibility_of_element_located((locator, element)))
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise
        except exceptions.ElementClickInterceptedException:
            self._get_exception_message('click_intercepted')
            raise
        time.sleep(0.15)

    def wait_for_element_presence(self, locator='xpath', element=None, wait_time=True):
        """Wait for an elements presence in the html. This differs from wait for element visibility in that an element
        would pass this check if it is not visible on a page but exists within the pages html.
        :param element: Additionally you can pass a list of elements to wait for multiple items elements to be visible
        on the page"""
        locator = self._get_locator(locator)
        if wait_time is True:
            wait_time = self.timeout_value
        try:
            if isinstance(element, list):
                all_elements_ec = [EC.presence_of_element_located((locator, all_elements)) for all_elements in element]
                WebDriverWait(self.driver, float(wait_time)).until(_wait_for_all(*all_elements_ec))
            else:
                WebDriverWait(self.driver, float(wait_time)).until(
                    EC.presence_of_element_located((locator, element)))
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise
        except exceptions.ElementClickInterceptedException:
            self._get_exception_message('click_intercepted')
            raise
        time.sleep(0.15)

    def scroll_into_view(self, locator='xpath', element=None, wait_time=True):
        """Scrolls elements into view"""
        locator = self._get_locator(locator)

        if wait_time is True:
            wait_time = self.timeout_value
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(false);", WebDriverWait(
                    self.driver, float(wait_time)).until(EC.element_to_be_clickable(
                        (locator, element))))
            # time.sleep(0.25)
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise
        except exceptions.ElementClickInterceptedException:
            self._get_exception_message('click_intercepted')
            raise

    def click_element(self, locator='xpath', element=None, wait_time=True):
        """Clicks element"""
        locator = self._get_locator(locator)

        if wait_time is True:
            wait_time = self.timeout_value
        try:
            item = WebDriverWait(self.driver, float(wait_time)).until(
                EC.element_to_be_clickable((locator, element)))
            time.sleep(0.15)
            item.click()
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise
        except exceptions.ElementClickInterceptedException as e:
            logger.warning(f"ElementClickInterceptedException :: {e} :: Attempting alternate click")
            self.click_element_alternate(element=element)

    def click_element_alternate(self, locator='xpath', element=None, wait_time=True):
        """Alternative click that uses javascript injection? to click elements incase the other click_element method
        does not work properly"""
        locator = self._get_locator(locator)

        if wait_time is True:
            wait_time = self.timeout_value

        try:
            self.driver.execute_script("arguments[0].click(false);", WebDriverWait(
                self.driver, float(wait_time)).until(EC.element_to_be_clickable((locator, element))))
            time.sleep(0.15)
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise
        except exceptions.ElementClickInterceptedException:
            self._get_exception_message('click_intercepted')
            raise

    def send_keys_element(self, locator='xpath', element=None, keys=None, clear_text=True, wait_time=True):
        """Sends text to an element that can be typed to
        :param keys: the string of keys you want to send the the element
        :param clear_text: If set True, will preclear the text that is in the element"""
        try:
            locator = self._get_locator(locator)

            if wait_time is True:
                wait_time = self.timeout_value

            item = WebDriverWait(self.driver, float(wait_time)).until(
                EC.element_to_be_clickable((locator, element)))
            # action = ActionChains(self.driver)
            if clear_text:
                item.send_keys(Keys.CONTROL + "a")
                item.send_keys(Keys.DELETE)

            item.send_keys(keys)
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise
        except exceptions.ElementClickInterceptedException:
            self._get_exception_message('click_intercepted')
            raise

    def get_number_of_elements(self, locator='xpath', element=None, wait_time=True):
        """Returns number of common elements.
        :param wait_time: ADDITIONAL: Set wait time to false to not wait at all
        """
        try:
            locator = self._get_locator(locator)

            if type(wait_time) is int or type(wait_time) is float or wait_time is True:
                if wait_time is True:
                    wait_time = self.timeout_value

                WebDriverWait(self.driver, float(wait_time)).until(
                    EC.presence_of_element_located((locator, element)))
            elif wait_time is False:
                # Do not wait
                pass

            return len(self.driver.find_elements_by_xpath(element))
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise
        except exceptions.ElementClickInterceptedException:
            self._get_exception_message('click_intercepted')
            raise

    def get_inner_html(self, locator='xpath', element=None, wait_time=True):
        """Get the inner html of an element, or the text."""
        try:
            locator = self._get_locator(locator)

            if wait_time is True:
                wait_time = self.timeout_value

            item = WebDriverWait(self.driver, float(wait_time)).until(
                EC.presence_of_element_located((locator, element)))
            # time.sleep(0.15)
            return item.get_attribute('innerHTML')
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise
        except exceptions.ElementClickInterceptedException:
            self._get_exception_message('click_intercepted')
            raise

    def get_element_html(self, locator='xpath', element=None, wait_time=True):
        """Get the the html itself of the given element"""
        try:
            locator = self._get_locator(locator)

            if wait_time is True:
                wait_time = self.timeout_value

            item = WebDriverWait(self.driver, float(wait_time)).until(
                EC.presence_of_element_located((locator, element)))
            time.sleep(0.15)
            return item.get_attribute('outerHTML')
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise
        except exceptions.ElementClickInterceptedException:
            self._get_exception_message('click_intercepted')
            raise

    def hover_over_element(self, locator='xpath', element=None, wait_time=True):
        """Hover over given element"""
        try:
            locator = self._get_locator(locator)

            if wait_time is True:
                wait_time = self.timeout_value

            item = WebDriverWait(self.driver, float(wait_time)).until(
                EC.presence_of_element_located((locator, element)))
            time.sleep(0.15)
            action = ActionChains(self.driver)
            action.move_to_element(item).move_by_offset(1, 1).pause(0.5).perform()
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise
        except exceptions.ElementClickInterceptedException:
            self._get_exception_message('click_intercepted')
            raise

    def page_end(self):
        """Immediately go the page end"""
        try:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise

    def page_top(self):
        """Immediately go the the top of the page"""
        try:
            action = ActionChains(self.driver)
            action.send_keys(Keys.HOME).perform()
        except exceptions.TimeoutException:
            self._get_exception_message('timeout')
            raise

    @staticmethod
    def _get_locator(locator):
        """Used internally to set selenium By attribute used for locating elements"""
        if locator.lower() == 'xpath': locator = By.XPATH
        elif locator.lower() == 'css_selector': locator = By.CSS_SELECTOR
        elif locator.lower() == 'link_text': locator = By.LINK_TEXT
        elif locator.lower() == 'id': locator = By.ID
        else:
            logger.warning('Invalid locator. Using XPATH')
            locator = By.XPATH
        return locator

    @staticmethod
    def _get_exception_message(type):
        """Logs a warning for a selenium exceptions
        :param type: a lowercase underscore seperated string that describes the selenium exception"""
        if type == 'timeout':
            logger.warning('TimeoutException :: A Selenium error occured. Explicit wait failed. The requested element '
                           'was most likely not present')
        if type == 'click_intercepted':
            logger.warning('ElementClickInterceptedException :: A Selenium error occured. Click was intercepted by '
                           'another element')




class _wait_for_all:
    """class for waiting for multiple elements to appear. It can be used to see if elements on a page are loading.
    See wait_for_items_in_wrapper() to see how to implement"""

    def __init__(self, *args):
        self.methods = args

    def __call__(self, driver):
        try:
            for method in self.methods:
                if not method(driver):
                    return False
            return True
        except exceptions.StaleElementReferenceException:
            return False


class _wait_for_any:
    """class for waiting for any element to appear. Used the same way that _wait_for_all is used"""
    def __init__(self, *args):
        self.methods = args
    def __call__(self, driver):
        for method in self.methods:
            try:
                if method(driver):
                    return True
            except:
                pass

