import importlib
config = importlib.import_module('config_02')

import time
import os

import requests


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


import re
import datetime


"""
Regarding Logging instance

There are two type of logger
1. Logger that logs message with prefix of timestamp (good for error log)
2. Logger that only logs message without timestamp (good for logging URL that already done
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

def setup_message_logger(name, log_file, level=logging.INFO):
    """
    Function to set Message logger
    Similar with function above, but this logger did not log timestamp.
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
Code about reading local .txt configuration
"""

def read_url(filename = "URLS.txt"):
    """
    Open file that contains the URL, and obtains all valid URL.
    It also open URLsDone.txt

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


def read_proxy(logger_proxy_error, filename = "Proxies.txt"):
    """
    Open file that contains the URL, and obtains all valid URL.

    :param filename: filename to look for URL
    :return: the url_list (list    or   False (boolean) if empty
    """

    proxy_list = []
    if os.path.isfile(filename):
        with open(filename) as url_file:
            if config.DebugMode:
                print("Reading Proxy:")

            for line in url_file:
                if not line.startswith("#") and not line.strip() == '':
                    # insert the URL ito url_list
                    proxy_list.append(line.strip())
                    if config.DebugMode:
                        print(line.strip())

    """
    Here we check if the proxy is valid.
    The proxy is considered valid if we can successfully request a random link that is supposed to succeed with the proxy.

    If proxy is valid, but the link is blocked, the request will still be 200 code (request OK).
    If proxy is invalid, it tends to take a long time to open the link before it throws error code, 
    so we will also describe a timeout here.
    """
    checked_proxy_list = []
    print('Checking all proxies')
    for proxy in proxy_list:
        check_result = check_proxy(proxy, timeout=3)
        if check_result:
            checked_proxy_list.append({
                'proxy': proxy,
                'proxy_instance': check_result
            })
        else:
            logger_proxy_error.warn("Invalid Proxy: {}".format(proxy))
            print("Found invalid proxy. Logged into ProxyError.txt: {}".format(proxy))

    return checked_proxy_list









"""
Regarding webdriver


webdriver: the driver to control a browser
Options: option for the webdriver
NoSuchElementException: exception throwed if no elements found
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def init_webdriver(proxy_dict = None, account_credentials = None):
    """
    Here, we are configure and intitialize webdriver

    :param proxy_dict: proxy dictionary
    :param account_credentials: account credentials
    :return:
    """

    """
    Webdriver's Load Strategy
    
    In majority of cases, you might want to make the load strategy to "none" to greatly improve
    the scrapping. Doing so will not run any JS/other script, so selenium will be much faster.
    
    In apkpure.com's case though, or in other case when you need JS/Script to load, it should be set to "normal".
    
    If no mode is set (i.e. all commented out) then the default will be "normal"
    
    More about loading strategy: https://stackoverflow.com/a/44771628/6558550
    """

    # webdriver.DesiredCapabilities.CHROME['pageLoadStrategy'] = "none"
    # webdriver.DesiredCapabilities.CHROME['pageLoadStrategy'] = "normal"

    if config.UseProxies:
        """
        Here we set the proxy
        """
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": proxy_dict.get('httpProxy', ''),
            "ftpProxy": proxy_dict.get('ftpProxy', ''),
            "sslProxy": proxy_dict.get('sslProxy', ''),
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
    Setting Webdriver's Preferences

    All of the codes below are experimental preference that worked for my system.
    It should be good for you to run. But you can turn it off by commenting it should you need any adjustment.

    
    - Setting the default download directory
        'download.default_directory': 'your/download/path',
        Note that if same filename already in directory, browser will automatically append with counter (like "files (1).zip" )

    - Disable Chrome Harm file detector
        'safebrowsing.enabled': True,
        Disable chrome popup asking that file downloaded might be harm. The pop up is preventing the download to start.

    - disable image load 
        'profile.managed_default_content_settings.images': 2,
        This will greatly increase the bot speed, but the images will not be loaded

    - Force webdriver to use diskcache. 
        'disk-cache-size': 4096
        This will force webdriver to save browser's cache on disk. So we did not loading everytime we start the browser.
        4096 is for 4gb and , you can configure yours. The bigger the better, but as high as 8gb would be wasteful I think.
        But we do need as high as 8gb if say you want to scrap it to download entire night.
        
    - Allow/prevent downloading multiple files
        'profile.default_content_setting_values.automatic_downloads': 1,
        'download.prompt_for_download': False
        Two lines above will automatically download without prompting a new window for saving the file.
        For now, I did not require these codes so I commented it and it worked on apkpure.com.
        You might need to turn it on should you find a problem regarding downloading

    - Disable download protection
        chrome_options.add_argument('--safebrowsing-disable-download-protection')
        This code is neraly have same functionality with "Disable Chrome Harm file detector" above.

    """

    preferences = {
        'download.default_directory': config.SaveDirectory if config.SaveDirectory else config.DefaultSaveDirectory,

        'safebrowsing.enabled': True,

        'profile.managed_default_content_settings.images': 2,

        'disk-cache-size': 4096

        # For now, I did not use this
        # 'profile.default_content_setting_values.automatic_downloads': 1,
        # 'download.prompt_for_download': False
    }

    chrome_options.add_argument('--safebrowsing-disable-download-protection')

    # and then we register the preference to the options
    chrome_options.add_experimental_option('prefs', preferences)

    # create the webdriver according to its path and options, then the browser will appears
    driver = webdriver.Chrome(config.WebDriverPath, chrome_options=chrome_options)

    if config.TestMode:
        # for testing, it will download a notepad++ installer and then exit
        driver.get('https://notepad-plus-plus.org/repository/7.x/7.6.5/npp.7.6.5.bin.minimalist.7z')
        input()
        exit()



    """
    Clearing Cookies
    
    We seem did not need to clear the cookies, because everytime we close a driver
    and re-instantiating it, it is a brand new clean web driver with no default configuration.
    
    But should that requirements really necessary, we can always uncomment the code below
    """
    # driver.delete_all_cookies()


    """
    If Login is required, the code will perform a login action
    """
    if config.RequireLogin:
        # get the credentials
        if ':' not in account_credentials:
            print("Credentials is not valid")
            exit()

        username, password = account_credentials.split(':')

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
            print('either username or password input form is not found by xpath. Please check the XPath '
                  'for the username and password form in configuration.')
            if config.DebugMode:
                print(e)
            exit()


        """
        ReCaptcha 
    
        If reCaptcha found -> Solving reCaptcha ...
        """

        recaptcha_element = driver.find_element_by_xpath(config.XPathRecaptcha)
        if recaptcha_element:
            """
            For now we have 2 options, according to config_02.py/ReCaptchaOption:
            1. Wait for certain seconds to solve recaptcha
            2. CLI will ask for input (it will wait forever). So user can take time to solve captcha, 
               and after that user will need to go to CLI and press any key (say, enter)
            3. Requesting anti-captcha service (for now it is not available because we need the 
            documentation of the API service. Feel free to inform me about this)
            """

            if config.ReCaptchaOption == 1:
                # option 1
                time.sleep(60) # wait 1 minute / any given time for user to solve captcha
            elif config.ReCaptchaOption == 2:
                # option 2
                input("Captcha found. Please solve it on the browser then press any key here to continue..")
            elif config.ReCaptchaOption == 3:
                # todo: or anti-captcha.com services will be called here
                # requirements: what anti-captcha services are? and We should need the documentation for the API
                pass


        print('Clicking on Login Button ...')
        try:
            driver.find_element_by_xpath(config.XPathLoginButton).click()
        except NoSuchElementException as e:
            print('Login button not found by Xpath. Please check the XPath for the login button in confugiration.', e)
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

        if not is_successfully_login:
            # todo: need variety of error case to be coded more specifically
            print('Login/get sessions seems to be failed')
            exit()

        return driver

    else:
        return driver




"""
Regarding Requests Module
"""

def check_proxy(proxy, timeout = 5):
    """
    Code to check if proxy is valid.
    Here, we accessing google.com using given proxy.
    If request succeed -> then proxy is valid.

    Feel free to change the link from google.com to something else.
    For example, you might want to open a localhost link or so,
    or a link that guaranteed to be successfully opened only by using the proxy.
    :param proxy: the proxy
    :return: is the proxy valid?
    """

    """
    For timeout:
        Set the time to wait before declaring that the proxy is invalid. The default is 5 secs
        This is a trade-off between speed and validity.
        give it too long and the proxy check might be more accurate, but it will takes time
        give it too small and the valid proxy might be declared invalid due to timeout, but the code will be faster
    """

    try:
        requests.get(
            # feel free to cahnge this link
            "http://example.com",

            proxies = {
                # you can also comment the unused (e.g. You may only need the http one)
                'http': proxy,
                'htts': proxy,
                'ftp': proxy,
            },

            timeout = timeout
        )
    except IOError:
        # proxy is not valid
        return False
    else:
        # proxy is valid
        # return True
        return {
            # you can also comment the unused (e.g. You may only need the http one)
            'http': proxy,
            'htts': proxy,
            'ftp': proxy,

        }



def is_downloadable(url, cookies = (), header = None, proxy = None):
    """
    Does the url contain a downloadable resource?

    Simply calling, a URL can be considered webpage if its 'Content-Type' is 'text', 'html', or 'text/html'
    Any value except said type is actually a file (or as far we call it "direct link')

    So code need to get the url and keep tracing it until it leads to a URL where the content-type is a file.
    Else, then the URL is not downloadable.

    :param url: url to be downloaded
    :param cookies: cookies
    :return: boolean if url is downloadable, and its header
    """

    """
    Here we declare that the request will have session from webdriver's cookies.
    We will also add user agent later to this request instance.
    
    Now, the target server is actually thinks that it came from the same connection/source.
    """
    request_session = requests.Session()
    for cookie in cookies:
        request_session.cookies.set(cookie['name'], cookie['value'])

    """
    We just need the header, so don't waste bandwith by downloading all the content.
    Also we are enabling allow_redirects so that the requests module will keep linking any URL 
    it founds until no redirects happen.
    """

    h = requests.head(url, allow_redirects=True, header = header, proxies = proxy)
    header = h.headers
    content_type = header.get('content-type', header = header, proxies = proxy)
    if 'text' in content_type.lower() or 'html' in content_type.lower():
        return False, h
    return True, h


def download_binary(url, cookies = (), header = None, proxy = None):
    """
    Like the funciton name said, this download the binary file contained in URL.
    :param url: url
    :return: request result
    """

    """
    Here we declare that the request will have session from webdriver's cookies.
    We will also add user agent later to this request instance.

    Now, the target server is actually thinks that it came from the same connection/source.
    """
    request_session = requests.Session()
    for cookie in cookies:
        request_session.cookies.set(cookie['name'], cookie['value'])

    return requests.get(url, allow_redirects=True, header = header, proxies = proxy)



def seek_filename(header):
    """
    Get possible filename from header.
    If no filename found on header, code will autogenerate it with timestamp

    :param header: request header
    :return: filename or None
    """
    content_disposistion = header.get('content-disposition', None)
    if content_disposistion:
        result_list = re.findall('filename=(.+)', content_disposistion)
        if result_list:
            return True, result_list[0]
    return False, 'unnamed_file_' + str(datetime.datetime.now())[:19].replace(":", '_')










"""
All of these codes below are experimental and currently unused.
Maybe it will help us later time.
"""

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
    This only works with Chrome (.crdownload)

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
