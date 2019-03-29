import importlib
config = importlib.import_module('config_02')
lib = importlib.import_module('lib_common')

import time
import os

logger_url = lib.setup_logger('logger_url', 'log/URLsLog.txt')
logger_file = lib.setup_logger('logger_file', 'log/FilesLog.txt')
logger_error = lib.setup_logger('logger_error', 'log/ErrorLog.txt')

url_list = lib.read_url()

driver = lib.init_webdriver()

for url in enumerate(url_list):
    print("Loading URL ({}/{}) from URLs.txt ...".format(url[0] + 1, len(url_list)))
    driver.get(url[1])
    for xpath in enumerate(config.XPathFiles):
        element_founds = driver.find_elements_by_xpath(xpath[1])

        if config.SequentialFiles:
            """
            Downloading sequentially with request method (in the background)
            After a completed download, it will wait for interval between files
            """

            complete_download = 0
            for element in element_founds:
                file_url = element['href']
                if file_url:
                    is_downloadable, header = config.is_downloadable(file_url)
                    if is_downloadable:
                        is_filename_available, filename = config.seek_filename(header)
                        if not is_filename_available:
                            logger_file.info('Url {} : File name is not found. Autogenerate it with no extension'.format(file_url))

                        # download the file
                        request_result = config.download_binary(file_url)

                        # save the content to file (binary writing)
                        if request_result.status_code == 200:
                            open(os.path.join(config.SaveDirectory if config.SaveDirectory else config.DefaultSaveDirectory, filename), 'wb').write(request_result.content)
                            complete_download += 1
                            logger_file.info('Downloaded in background : {}'.format(filename))
                            print("File {} downloaded successfully. Waiting for {} secon(s)".format(filename, config.IntervalsBetweenFiles))
                            time.sleep(config.IntervalsBetweenFiles)
                        else:
                            logger_file.error('Error download in background: {}'.format(filename))
                            print("File {} : Download error.".
                                  format(filename, config.IntervalsBetweenFiles))

                    else:
                        logger_file.info('Url {} : File {} is not downloadable')
                        continue
                else:
                    logger_file.info('Url for element {} is not found'.format(str(element)))

            logger_url.info('Scrapped {}. {} file(s) downloaded from link'.format(url[1], complete_download))


        else:
            """
            Downloading with Selenium without checking if the file is completely downloaded
            After a click, it will wait for interval between files
            """

            # will NOT check for file completion. Just wait for interval. Download is made by selenium
            element_clicked = 0
            for element in element_founds:

                # scroll to the element
                driver.execute_script("arguments[0].scrollIntoView(true);", element)

                # wait a bit to avoid processing error (i.e. browser might be slower at the time, so scrolling will be lagged, etc)
                time.sleep(0.5)
                element.click()
                element_clicked += 1

                logger_file.info('Selenium download : ' + element.text)
                print("Element clicked successfully. Waiting for {} secon(s)".format(element.text,
                                                                                        config.IntervalsBetweenFiles))

                time.sleep(config.IntervalsBetweenFiles)

            logger_url.info('URL {} : {} element(s) clicked with Selenium'.format(url[1], element_clicked))

    if isinstance(config.IntervalsBetweenUrls, int):
        print('Waiting {} second(s) for the next URL'.format(config.IntervalsBetweenUrls))
        time.sleep(config.IntervalsBetweenUrls)

    if url[0] % config.URLCountToSwitch:
        # switch account and restart
        driver = lib.init_webdriver(driver)

print("Done.")

