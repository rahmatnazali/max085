import importlib
config = importlib.import_module('config_02')

import time
import os

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

