import importlib
config = importlib.import_module('config_02')
lib = importlib.import_module('lib_common')

import time
from selenium import webdriver


url_list = lib.read_url()

# driver = lib.init_webdriver()
driver = webdriver.Chrome()

for url in enumerate(url_list):
    print("Loading URL ({}/{}) from URLs.txt ...".format(url[0] + 1, len(url_list)))
    driver.get(url[1])
    for xpath in enumerate(config.XPathFiles):
        element_founds = driver.find_elements_by_xpath(xpath[1])
        for element in element_founds:
            element.click() # download
            # todo: should I wait until download is completed or can I bulk download all together?
            # todo: Add Result Description FilesLog.txt (print and log into file)

        # todo: Add Result Description URLsLog.txt (print and log into file)

    if url[0] % config.URLCountToSwitch:
        # todo: switch account and restart
        driver = lib.init_webdriver(driver)

print("Done.")

