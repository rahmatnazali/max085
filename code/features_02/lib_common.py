import importlib
config = importlib.import_module('config_02')

import time
import os

import requests


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


import re
import datetime


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

link_done_logger_formatter= logging.Formatter('%(message)s')

def setup_link_done_logger(name, log_file, level=logging.INFO):
    """
    Function to set Link Done logger
    :param name: name of logger instance
    :param log_file: path to the log file
    :param level: minimum level of considered logging | how logging level works ? https://docs.python.org/2/howto/logging.html#logging-levels
    :return: the logger instance
    """
    handler = logging.FileHandler(log_file)
    handler.setFormatter(link_done_logger_formatter)

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

    # check any url that is already Done in URLsDone.txt
    url_done_list = []
    if os.path.isfile('log/URLsDone.txt'):
        url_done_list = [line.rstrip('\n') for line in open('log/URLsDone.txt')]

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
    return url_list, url_done_list


def credential_pop(credentials):
    """
    Code will pop one element from list of credentials,
    return the popped credential and the remain lists
    :param credentials:
    :return: list_of_remaining_credentials, username, password
    """

    for i in range(len(credentials)):
        c = credentials.pop()
        if not isinstance(c, str) or not ':' in c:
            print("Invalid credentials format:", c)
            continue
        username, password = c.split(":")
        return credentials, username, password
    print("No credentials left")
    exit(1)






"""
Regarding webdriver
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def init_webdriver():
    """
    Code to generate a Chrome webdriver.
    If given driver is None, it will create a webdriver.
    If given driver is there, it will only restart it (clear all cookies, etc)

    :param driver: the webdriver
    :return: the webdriver
    """
    config.Credentials, username, password = credential_pop(config.Credentials)

    proxy = "149.215.113.110:70"

    # todo: add profile/options here
    # default download directory
    if config.UseProxies:
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": proxy,
            "ftpProxy": proxy,
            "sslProxy": proxy,
            "noProxy": None,
            "proxyType": "MANUAL",
            "class": "org.openqa.selenium.Proxy",
            "autodetect": False
        }

    # declare an options object
    chrome_options = Options()

    # setting the browser visibility mode
    chrome_options.headless = not config.ShowBrowserWindows

    """
    setting the default download directory
    not that if same filename already in directory, browser will automatically append with counter (like "files (1).zip" )
    """
    prefs = {'download.default_directory': 'result'}
    chrome_options.add_experimental_option('prefs', prefs)

    # executing the webdriver
    driver = webdriver.Chrome(config.WebDriverPath, chrome_options=chrome_options)

    if config.TestMode:
        # for testing, it will download a notepad++ installer
        driver.get('https://notepad-plus-plus.org/repository/7.x/7.6.5/npp.7.6.5.bin.minimalist.7z')


    """
    Clearing Cookies
    
    We seems did not need to clear the cookies, because everytime we close a driver
    and re-instantiating it, it is a brand new clean web driver with no default configuration.
    
    But should that requirements appears, we can always uncomment the code below
    """
    # driver.delete_all_cookies()



    # get loading page
    print('Loading Login Page ...')
    driver.get(config.LoginPage)

    """
    Form filling
    
    Clicking On Username/Email Input -> Filling Next Username/Email ...
    Clicking On Password Input -> Filling Next Password ...
    """
    try:
        driver.find_element_by_xpath(config.XPathFormUserOrEmail).send_keys(username)
        driver.find_element_by_xpath(config.XPathFormPassword).send_keys(password)
    except NoSuchElementException as e:
        print('either username or password input form is not found by xpath. Please check the XPath in configuration.', e)
        exit()


    """
    ReCaptcha 

    If reCaptcha found -> Solving reCaptcha ...
    """

    recaptcha_element = driver.find_element_by_xpath(config.XPathRecaptcha)
    if recaptcha_element:
        """
        For now we have 2 options:
        1. Wait for certain seconds to solve recaptcha
        2. CLI will ask for input (it will wait forever). So user can take time to solve captcha, 
           and after that user will need to go to CLI and press any key (say, enter)
        """
        # option 1
        # time.sleep(60) # wait 1 minute / any given time for user to solve captcha

        # option 2
        input("Captcha found. Please solve it on the browser then press any key here to continue")


        # todo: or anti-captcha.com services will be called here

    # click login button
    print('Clicking on Login Button ...')
    try:
        driver.find_element_by_xpath(config.XPathLoginButton).click()
    except NoSuchElementException as e:
        print('Login button not found by Xpath. Please check the XPath in confugiration.', e)
        exit()




    """
    Then the code will check if a certain XPath that will be always appear after successful login, appears.
    If appears, it is guaranteed that the login process is success.
    If not, it may be also running well, but are suspected for error in long term 
    (e.g. browser will keep access something when the login process is failed).
    
    If login is done via requests method, we can easily see the status_code to determine if login was successful.
    But because login process must be done via HTML Form, this is considered the best practice to check if login is succesful or not.
    """
    is_successfully_login = False
    print('Waiting until login is succeed ...')
    try:
        login_timeout = config.LoginTimeout
        WebDriverWait(driver, login_timeout).until(EC.presence_of_element_located((By.XPATH, config.LoggedInXPath)))
        is_successfully_login = True
    except TimeoutException:
        print("Login takes too much time. Code can not tell if browser is logged in or not."
              "This is not an error statement but a warning, as in some case this may lead to an error."
              "This is because the code did not know if browser is successfully logged or not")

    return driver, is_successfully_login


def is_downloadable(url):
    """
    Does the url contain a downloadable resource?

    Simply calling, a URL can be considered webpage if its 'Content-Type' is 'text', 'html', or 'text/html'
    Any value except said type is actually a file (or as far we call it "direct link')

    So code need to get the url and keep tracing it until it leads to a URL where the content-type is a file.
    Else, then the URL is not downloadable.

    :param url: url to be downloaded
    :return: boolean if url is downloadable, and its header
    """

    """
    We just need the header, so don't waste bandwith by downloading all the content.
    Also we are enabling allow_redirects so that the requests module will keep linking any URL 
    it founds until no redirects happen.
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower() or 'html' in content_type.lower():
        return False, h
    return True, h

def download_binary(url):
    """
    Like the funciton name said, this download the binary file contained in URL.
    :param url: url
    :return: request result
    """
    return requests.get(url, allow_redirects=True)



def seek_filename(header):
    """
    Get possible filename from header.

    :param header: request header
    :return: filename or None
    """
    content_disposistion = header.get('content-disposition', None)
    if content_disposistion:
        result_list = re.findall('filename=(.+)', content_disposistion)
        if result_list:
            return True, result_list[0]
    return False, 'unnamed_file_' + str(datetime.datetime.now())[:19].replace(":", '_')









# experimental code. currently not used

"""
All of these codes below are experimental and currently unused.
Maybe it will help us later time.
"""

def limit_size(url):
    """
    Evaluate wether a file size is inside the size limit length
    :param url:
    :return:
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_length = header.get('content-length', None)
    if content_length and content_length > 2e8:  # approximately 200 mb
        return False

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
