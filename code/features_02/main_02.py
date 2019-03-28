import importlib
config = importlib.import_module('config_02')
lib = importlib.import_module('lib_common')

import time
from selenium import webdriver

logger_url = lib.setup_logger('logger_url', 'log/URLsLog.txt')
logger_file = lib.setup_logger('logger_file', 'log/FilesLog.txt')
logger_error = lib.setup_logger('logger_error', 'log/ErrorLog.txt')

url_list = lib.read_url()

# driver = lib.init_webdriver()
driver = webdriver.Chrome()

for url in enumerate(url_list):
    print("Loading URL ({}/{}) from URLs.txt ...".format(url[0] + 1, len(url_list)))
    driver.get(url[1])
    for xpath in enumerate(config.XPathFiles):
        element_founds = driver.find_elements_by_xpath(xpath[1])

        if config.SequentialFiles:
            complete_download = 0
            for element in element_founds:
                file_url = element['href']
                if file_url:
                    is_downloadable, header = config.is_downloadable(file_url)
                    if is_downloadable:
                        is_filename_available, filename = config.seek_filename(header)
                        if not is_filename_available:
                            logger_file.info('Url {} : File name is not found. Autogenerate it with no extension'.format(file_url))

                        # todo: download
                        # todo: save
                        request_result = config.download_binary(file_url)
                        open('file/{}'.format(filename), 'wb').write(request_result.content)
                        complete_download += 1
                        logger_file.info('Downloaded in background : ' + str(element))
                        time.sleep(config.IntervalsBetweenFiles)

                    else:
                        logger_file.info('Url {} : File {} is not downloadable')
                        continue
                else:
                    logger_file.info('Url for element {} is not found'.format(str(element)))

            logger_url.info('Scrapped {}. {} file(s) downloaded from link'.format(url[1], complete_download))

        else:
            # will NOT check for file completion. Just wait for interval. Download is made by selenium
            element_clicked = 0
            for element in element_founds:

                # todo: scroll to element

                element.click() # download
                element_clicked += 1

                logger_file.info('selenium download : ' + str(element))
                time.sleep(config.IntervalsBetweenFiles)

            logger_url.info('{} element(s) clicked with Selenium: {}'.format(element_clicked, url[1]))





    if url[0] % config.URLCountToSwitch:
        # todo: switch account and restart
        driver = lib.init_webdriver(driver)

print("Done.")

