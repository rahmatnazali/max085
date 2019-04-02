import importlib
config = importlib.import_module('config_02')
lib = importlib.import_module('lib_common')

import time
import os
from random import randint

# for storing links that already done
logger_link_done = lib.setup_message_logger('logger_link_done', 'log/URLsDone.txt')

# for logging each url's description/status
logger_url = lib.setup_logger('logger_url', 'log/URLsLog.txt')

# for logging the status of each files downloaded/clicked/
logger_file = lib.setup_logger('logger_file', 'log/FilesLog.txt')

# for logging an error
logger_error = lib.setup_logger('logger_error', 'log/ErrorLog.txt')

# for logging false proxies
logger_proxy_error = lib.setup_message_logger('logger_link_done', 'log/ProxyError.txt')


"""
Read URL and Proxy from txt
"""
url_list, url_done_list = lib.read_url()
proxy_list = lib.read_proxy()


"""
Check if the proxy is valid
"""
# todo: check if proxy is valid. if not, log into error
# todo: code is worked, but took so long
checked_proxy_list = []
for proxy in proxy_list:
    print('checking', proxy)
    if lib.check_proxy(proxy):
        checked_proxy_list.append(proxy)
    else:
        logger_proxy_error.warn("Invalid Proxy: {}".format(proxy))
        print("Found invalid proxy. Logged into ProxyError.txt: {}".format(proxy))
proxy_list = checked_proxy_list


print(proxy_list)
exit()

driver, is_successfully_login = lib.init_webdriver()

for url in enumerate(url_list):
    print("Loading URL ({}/{}) from URLs.txt ...".format(url[0] + 1, len(url_list)))
    driver.get(url[1])

    """
    Assuming that we got the page that we can not access this without session (logged in),
    the code then will try to find all elements by XPath, and click it one by one
    """
    for xpath in enumerate(config.XPathFiles):

        # find all elements by its xpath
        element_founds = driver.find_elements_by_xpath(xpath[1])

        """
        This marks the download mode that done with requests module
        """
        if config.SequentialFiles:
            """
            Downloading sequentially with request method (in the background)
            After a completed download, it will wait for interval between files
            """

            # first, we will obtain the cookies from browser
            cookies = driver.get_cookies()

            complete_download = 0
            for element in element_founds:
                file_url = element['href']
                if file_url:

                    """
                    Here we will check if URL is downloadable.
                    Code will keep following the link until no redirects occurrs,
                    and evaluate wether a file is exist in the far end.
                    
                    If a link is downloadable, it is very likely that it also contains the filename.
                    So we return the whole header object too for further evaluation regarding it.
                    """
                    is_downloadable, header = lib.is_downloadable(file_url, cookies = cookies, header = config.RequestHeader)


                    """
                    If the link is do downloadable, 
                    we will evaluate the filename from the header we got, and then download it
                    """
                    if is_downloadable:
                        """
                        Here, we pass the header to the function that find the filename

                        There are rare case when the URL is downloadable yet sites did not offer a filename.
                        So if that case happens, code will autogenerate filename so that it show when it is downloaded.
                        """
                        is_filename_available, filename = lib.seek_filename(header)

                        # just if the filename is not available, code will generate a logger to notify user.
                        if not is_filename_available:
                            logger_file.info('Url {} : File name is not found. Code will autogenerate random name with no extension.'.format(file_url))

                        """
                        Code then download the file
                        
                        Note that we pass a cookies and a header.
                        These two parameters will be used to make the request looks like it was from your very own browser.
                        """
                        request_result = lib.download_binary(file_url, cookies = cookies, header = config.RequestHeader)

                        """
                        If download is succeed (indicated by status code of 200), 
                        we will save the downloaded binary data to a filename.
                        """
                        if request_result.status_code == 200:

                            """
                            We join a path to the downloaded directory with os.path.join.
                            
                            We use os.path.join() because it will automatically adapt according to the OS we use.
                            example:
                            - in windows it will be C://
                            - in *nix it will be /some/path/ahead
                            
                            We did not need to worry about the system, let os modules handles it.
                            
                                                        
                            - After a successful path join, we then write the binary to the specified directory
                            - Increment the counter
                            - Log it,
                            - And importantly, sleep according to the given interval
                            """
                            directory_path = os.path.join(config.SaveDirectory if config.SaveDirectory else config.DefaultSaveDirectory, filename)
                            open(directory_path, 'wb').write(request_result.content)
                            complete_download += 1
                            logger_file.info('Downloaded in background : {}'.format(filename))

                            if isinstance(config.IntervalsBetweenFiles, tuple):
                                wait_time = randint(config.IntervalsBetweenFiles[0], config.IntervalsBetweenFiles[1])
                            else:
                                wait_time = config.IntervalsBetweenFiles

                            print("File {} downloaded successfully. Waiting for {} secon(s)".format(filename, wait_time))
                            time.sleep(wait_time)
                        else:
                            logger_file.error('Error download in background: {}'.format(filename))
                            print("Download error. Error obtaining File {} from Link {}".
                                  format(filename, file_url))
                            # we can then try to download it directly using file_url variable to know what exactly the error is

                    else:
                        logger_file.info('Download error. The file can not be downloaded from Link: {}'.format(file_url))
                        continue
                else:
                    logger_file.info('Request error. Code cannot find the source link for element: {}'
                                     .format(element.get_attribute('outerHTML')))

            logger_url.info('Scrapped {}. {} file(s) downloaded from link'.format(url[1], complete_download))


        else:
            """
            Downloading with Selenium
            After a click, it will wait for interval between files

            Note that this will *not* check for file completion. 
            The code will wait for interval only.
            After interval time is over, browser will continue to click again.

            """

            element_clicked = 0
            for element in element_founds:

                """
                Scroll to the element.
                
                For the browser to be able to do a valid click, the clicked element must always visible.
                When the elements is too many, the page might got scrolled and so we need to scroll to the element we want to click.
                
                The code below, in my experience, will rarely fails. But I do face an experience on certain project
                where this code fails for no reason.
                Let me know if it is failed on your system.
                """
                driver.execute_script("arguments[0].scrollIntoView(true);", element)

                # wait a bit to avoid processing error (i.e. browser might be slower at the time, so scrolling will be lagged, etc)
                time.sleep(0.5)
                element.click()
                element_clicked += 1

                logger_file.info('Selenium download : ' + element.text)

                if isinstance(config.IntervalsBetweenFiles, tuple):
                    wait_time = randint(config.IntervalsBetweenFiles[0], config.IntervalsBetweenFiles[1])
                else:
                    wait_time = config.IntervalsBetweenFiles

                print("Element clicked successfully. Waiting for {} second(s)".format(wait_time))
                time.sleep(wait_time)

            logger_url.info('URL {} : {} element(s) clicked with Selenium'.format(url[1], element_clicked))

    logger_link_done.info(url[1])

    if isinstance(config.IntervalsBetweenFiles, tuple):
        link_wait_time = randint(config.IntervalsBetweenFiles[0], config.IntervalsBetweenFiles[1])
    else:
        link_wait_time = config.IntervalsBetweenFiles

    print('Waiting {} second(s) for the next URL'.format(link_wait_time))
    time.sleep(link_wait_time)

    if url[0] % config.URLCountToSwitch:
        # switch account and restart
        driver = lib.init_webdriver()

print("Done.")

