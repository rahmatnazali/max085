import importlib
config = importlib.import_module('config_02')

import time
import os



"""
Regarding Logging instance
"""
import logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """
    Function to set multiple logger instance
    :param name: name of logger instance
    :param log_file: path to the log file
    :param level: minimum level of considered logging | how logging level works ? https://docs.python.org/2/howto/logging.html#logging-levels
    :return: the logger instance
    """
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


"""
Regarding reading URL
"""

def read_url(filename = "URLS.txt"):
    """
    Open file that contains the URL, and obtains all valid URL
    :param filename: filename to look for URL
    :return: the url_list (list    or   False (boolean) if empty
    """
    url_list = []
    if os.path.isfile(filename):
        with open(filename) as url_file:
            if config.DebugMode:
                print("Reading URLS:")

            for line in url_file:
                if not line.startswith("#") and not line.strip() == '':
                    # insert the URL ito url_list
                    url_list.append(line.strip())
                    if config.DebugMode:
                        print(line.strip())
        return url_list
    return False


# pop a credential
def credential_pop(credentials):
    if len(credentials):
        c = credentials.pop()
        if not isinstance(c, str) or not ':' in c:
            print("Invalid credentials format")
            exit(1)
        username, password = c.split(":")
        return credentials, username, password
    print("No credentials left")
    exit(1)




from selenium import webdriver
def initialization_process(driver = None):

    config.Credentials, username, password = credential_pop(config.Credentials)


    if  driver is None:
        # todo: add profile/options here
        # headless
        # proxy
        # default download directory
        driver = webdriver.Chrome(config.WebDriverPath)

    # Clear cookies (logout)
    driver.delete_all_cookies()

    # Set Proxy to Next Proxy From Proxies.txt
    # todo

    # Loading Login Page ...
    driver.get(config.LoginPage)

    # Clicking On Username/Email Input -> Filling Next Username/Email ...
    # Clicking On Password Input -> Filling Next Password ...

    driver.find_element_by_xpath(config.XPathFormUserOrEmail).send_keys(username)
    driver.find_element_by_xpath(config.XPathFormPassword).send_keys(password)

    # If reCaptcha found -> Solving reCaptcha ...
    recaptcha_element = driver.find_element_by_xpath(config.XPathRecaptcha)
    if recaptcha_element:
        time.sleep(60) # wait 1 minute for user to solve captcha
        # todo: or anti-captcha.com services will be called here

    # Clicking on Login Button ...
    driver.find_element_by_xpath(config.XPathLoginButton).click()


    # todo: check if succeed logged in. with webdriver
    # web driver wait few secs, if there, return true, else false
    is_successfully_login = False

    # todo: else will login again (?)

    return driver, is_successfully_login


def wait_download(directory, timeout, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    :param directory: The path to the folder where the files will be downloaded.
    :param timeout: How many seconds to wait until timing out.
    :param nfiles: If provided, also wait for the expected number of files.
    :return:
    """
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in directory:
            if fname.endswith('.crdownload'):
                dl_wait = True

        seconds += 1
    return seconds


import requests
def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    :param url:
    :return: boolean if url is downloadable, and its header
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower() or 'html' in content_type.lower():
        return False, h
    return True, h

def download_binnary(url):
    return requests.get(url, allow_redirects=True)


# todo: check if link have param https://images.pexels.com/photos/658687/pexels-photo-658687.jpeg?cs=srgb&dl=beautiful-bloom-blooming-658687.jpg&fm=jpg
# url.split('?')[0]


def limit_size(url):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_length = header.get('content-length', None)
    if content_length and content_length > 2e8:  # 200 mb approx
        return False

import re
import datetime
def seek_filename(header):
    """
    Get possible filename from header

    :param header: request header
    :return: filename or None
    """
    content_disposistion = header.get('content-disposition', None)
    if content_disposistion:
        result_list = re.findall('filename=(.+)', content_disposistion)
        if result_list:
            return True, result_list[0]
    return False, str(datetime.datetime.now())[:19].replace(":", '_')

