import re
import json
import time
import allure
import logging
import requests

from selenium.common.exceptions import NoSuchElementException


class AllureLogger(logging.Handler):
    def emit(self, record):
        with allure.step(f'{record.levelname}: {record.getMessage()}'):
            pass


logger = logging.getLogger('global')
logger.setLevel(logging.DEBUG)
allure_logger = AllureLogger()
logger.addHandler(allure_logger)


def __assert(browser, condition, message):
    try:
        assert condition, message
    except AssertionError:
        if browser:
            c_screeshot(browser)
        raise


def __search(browser, selector):
    result = re.search(r'^(?:(xpath|css|name|link|id)=)?(.*)', selector)
    stype = result.group(1) or 'xpath'
    selector = result.group(2) or '/'

    if stype == 'xpath':
        return browser.find_element_by_xpath(selector)
    elif stype == 'css':
        return browser.find_element_by_css_selector(selector)
    elif stype == 'name':
        return browser.find_element_by_name(selector)
    elif stype == 'id':
        return browser.find_element_by_id(selector)
    elif stype == 'link':
        return browser.find_element_by_link_text(selector)


def __searchs(browser, selector):
    result = re.search(r'^(?:(xpath|css|name|link|id)=)?(.*)', selector)
    stype = result.group(1) or 'xpath'
    selector = result.group(2) or '/'

    if stype == 'xpath':
        return browser.find_elements_by_xpath(selector)
    elif stype == 'css':
        return browser.find_elements_by_css_selector(selector)
    elif stype == 'name':
        return browser.find_elements_by_name(selector)
    elif stype == 'id':
        return browser.find_elements_by_id(selector)
    elif stype == 'link':
        return browser.find_elements_by_link_text(selector)


# COMMON METHODS

def c_log(severity, message):
    """
    Prints log message to allure report
    :param severity: one of the available logging levels {error, warning, info, debug}
    :param message: printable message
    """
    if severity == 'error':
        logger.error(message)
    elif severity == 'warning':
        logger.warning(message)
    elif severity == 'info':
        logger.info(message)
    else:
        logger.debug(message)


def c_screeshot(browser, name='Screenshot'):
    """
    Takes screenshot and attaches it to allure report
    :param browser: webdriver instance
    :param name: screenshot name
    """
    allure.attach(browser.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)


def c_wait(delay):
    """
    Waits specified number of seconds for something incredible
    :param delay: time to wait in seconds
    """
    c_log('info', f'Wait for [{delay}] seconds')
    time.sleep(int(delay))


def c_store(store, variable, value):
    """
    Saves value to variable in store
    :param store: store where to save
    :param variable: variable when to save
    :param value: value to be saved
    """
    c_log('info', f'Saves value [{value}] to variable [{variable}] in store')
    store[variable] = value


def c_assert_condition(condition, message):
    """
    Checks that condition is true
    :param condition: condition to check
    :param message: printable message
    """
    c_log('info', f'Checks that [{condition}] is true')
    __assert(
        None,
        condition,
        message
    )


def c_assert_equals(expected, real, message):
    """
    Checks that expected value equals to real value
    :param expected: value that we expect
    :param real: actual value
    :param message: printable message
    """
    c_log('info', f'Checks that expected [{expected}] value equals to real [{real}] value')
    __assert(
        None,
        str(expected) == str(real),
        message
    )


def c_assert_contains(needle, haystack, message):
    """
    Checks that substring contains in string
    :param needle: substring to contain
    :param haystack: string that should contain
    :param message: printable message
    """
    c_log('info', f'Checks that needle [{needle}] contains in haystack [{haystack}]')
    __assert(
        None,
        str(needle) in str(haystack),
        message
    )


def c_assert_matches(string, regex, message):
    """
    Checks that string matches regular expression
    :param string: string that should match
    :param regex: regular expression to search
    :param message: printable message
    """
    c_log('info', f'Checks that string [{string}] matches regex [{regex}]')
    __assert(
        None,
        re.compile(regex).search(string),
        message
    )


def c_assert_json_valid(jsonData, message):
    """
    Checks that the JSON is valid
    :param jsonData: checked JSON
    """
    c_log('info', f'Check that JSON is valid')
    allure.attach(
        json.dumps(jsonData),
        'JSON',
        attachment_type=allure.attachment_type.TEXT
    )
    try:
        jsonData = str(jsonData) \
            .replace('\'', '"') \
            .replace(': False', ': false') \
            .replace(': True', ': true') \
            .replace(': None', ': null')
        json.loads(str(jsonData))
        status = True
    except ValueError:
        status = False

    __assert(
        None,
        status,
        message
    )


# FRONTEND METHODS

def f_open(browser, url):
    """
    Opens specified url
    :param browser: webdriver instance
    :param url: url to open
    """
    c_log('info', f'Open [{url}] in browser')
    browser.get(url)


def f_click(browser, selector):
    """
    Clicks on LMB over element
    :param browser: webdriver instance
    :param selector: selector to the element
    """
    c_log('info', f'Click on element [{selector}]')
    __search(browser, selector).click()


def f_send_keys(browser, selector, value):
    """
    Types text or hits control keys over the element
    :param browser: webdriver instance
    :param selector: selector to the element
    :param value: input text or control key
    """
    c_log('info', f'Input text [{value}] to the element [{selector}]')
    __search(browser, selector).send_keys(value)


def f_assert_enabled(browser, selector):
    """
    Checks that the element is enabled
    :param browser: webdriver instance
    :param selector: selector to the element
    """
    __assert(
        browser,
        __search(browser, selector).is_enabled(),
        f'The element is not enabled'
    )


def f_assert_not_enabled(browser, selector):
    """
    Checks that the element is not enabled
    :param browser: webdriver instance
    :param selector: selector to the element
    """
    __assert(
        browser,
        not __search(browser, selector).is_enabled(),
        f'The element is enabled but it should not'
    )


def f_assert_displayed(browser, selector):
    """
    Checks that the element is visible
    :param browser: webdriver instance
    :param selector: selector to the element
    """
    __assert(
        browser,
        __search(browser, selector).is_displayed(),
        f'The element is not visible'
    )


def f_assert_not_displayed(browser, selector):
    """
    Checks that the element is not visible
    :param browser: webdriver instance
    :param selector: selector to the element
    """
    __assert(
        browser,
        not __search(browser, selector).is_displayed(),
        f'The element is visible but it should not'
    )


def f_assert_exists(browser, selector):
    """
    Checks that the element is presented
    :param browser: webdriver instance
    :param selector: selector to the element
    """
    __assert(
        browser,
        __search(browser, selector),
        f'The element is not presented'
    )


def f_assert_not_exists(browser, selector):
    """
    Checks that the element is not presented
    :param browser: webdriver instance
    :param selector: selector to the element
    """
    status = None
    try:
        __search(browser, selector)
        status = False
    except NoSuchElementException:
        status = True
        pass
    finally:
        __assert(
            browser,
            status,
            f'The element is presented but it should not'
        )


def f_assert_equals(browser, selector, attr, expected):
    """
    Checks that the attribute of the element equals to the expected value
    :param browser: webdriver instance
    :param selector: selector to the element
    :param attr: checked attribute
    :param expected: expected value
    """
    real = None
    if attr == 'text':
        real = __search(browser, selector).text
    elif attr == 'value':
        real = __search(browser, selector).value

    __assert(
        browser,
        expected == real,
        f'The real {attr} [{real}] not equals to the expected {attr} [{expected}]'
    )


def f_assert_not_equals(browser, selector, attr, expected):
    """
    Checks that the attribute of the element not equals to the expected value
    :param browser: webdriver instance
    :param selector: selector to the element
    :param attr: checked attribute
    :param expected: expected value
    """
    real = None
    if attr == 'text':
        real = __search(browser, selector).text
    elif attr == 'value':
        real = __search(browser, selector).value

    __assert(
        browser,
        expected != real,
        f'The real {attr} [{real}] equals to the expected {attr} [{expected}] but it should not'
    )


def f_assert_contains(browser, selector, attr, expected):
    """
    Checks that the attribute of the element contains the expected value
    :param browser: webdriver instance
    :param selector: selector to the element
    :param attr: checked attribute
    :param expected: expected value
    """
    real = None
    if attr == 'text':
        real = __search(browser, selector).text
    elif attr == 'value':
        real = __search(browser, selector).value

    __assert(
        browser,
        expected in real,
        f'The real {attr} [{real}] not contains the expected {attr} [{expected}]'
    )


def f_assert_not_contains(browser, selector, attr, expected):
    """
    Checks that the attribute of the element is not contains the expected value
    :param browser: webdriver instance
    :param selector: selector to the element
    :param attr: checked attribute
    :param expected: expected value
    """
    real = None
    if attr == 'text':
        real = __search(browser, selector).text
    elif attr == 'value':
        real = __search(browser, selector).value

    __assert(
        browser,
        expected not in real,
        f'The real {attr} [{real}] contains the expected {attr} [{expected}] but it should not'
    )


# BACKEND METHODS

def b_request(method, url, **kwargs):
    """
    Sends request to specified api with specified params
    :param method: one of the available methods {get, post, put, patch, delete}
    :param url: url to request
    :param data: (optional) Dictionary or list of tuples
    :param headers: (optional) Dictionary of HTTP Headers to send
    :param files: (optional) Dictionary of ``'name': file-like-objects``
    :return: :class:`Response <Response>` object
    """
    c_log('info', f'Send {method.upper()} request to {url}')
    kwargs_str = '\n\n'.join('{}={}'.format(k, v) for k, v in kwargs.items())
    if len(kwargs_str):
        allure.attach(
            kwargs_str,
            'Request params',
            attachment_type=allure.attachment_type.TEXT
        )

    if method == 'get':
        return requests.get(url, **kwargs)
    elif method == 'post':
        return requests.post(url, **kwargs)
    elif method == 'put':
        return requests.post(url, **kwargs)
    elif method == 'patch':
        return requests.patch(url, **kwargs)
    elif method == 'delete':
        return requests.delete(url, **kwargs)
    else:
        raise ValueError(f'Wrong request type [{method}]')
