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
logger_proxy_error = lib.setup_message_logger('logger_proxy_error', 'log/ProxyError.txt')


"""
Read URL and Proxy from txt
"""
url_list, url_done_list = lib.read_url()

if config.UseProxies:
    proxy_list = lib.read_proxy(logger_proxy_error)
    print(proxy_list)

    proxy_counter = 0

if config.RequireLogin:
    account_counter = 0


# initialize driver with an empty variable
driver = None

for url in enumerate(url_list):

    """
    If config.RequireLogin is true but no accounts left
    """
    if config.RequireLogin and account_counter > len(account_counter):
        print("No accounts left")
        exit()


    """
    Creating new browser instance, if driver is None
    """
    if driver is None:
        driver = lib.init_webdriver(proxy_list[proxy_counter] if config.UseProxies else None,
                                    config.Credentials[account_counter] if config.RequireLogin else None)

        if config.UseProxies:
            # increment proxy with mod, so it scycles
            proxy_counter = (proxy_counter + 1) % len(proxy_counter)

        if config.RequireLogin:
            # increment account. the code will stop if not accounts left
            account_counter += 1

    """
    Starts to get the URL
    """
    print("Loading URL ({}/{}) from URLs.txt ...".format(url[0] + 1, len(url_list)))
    driver.get(url[1])



    """
    Finding all elements by XPath, and click/downlaod it one by one
    """

    for xpath in enumerate(config.XPathFiles):

        # find all elements by its xpath
        element_founds = driver.find_elements_by_xpath(xpath[1])
        print("\tScrapping by XPath: Found {} element(s) from XPath: {}".format(len(element_founds), xpath[1]))

        if config.DebugMode:
            # to print the title and href
            for l in element_founds:
                print(l.get_attribute('title').strip())
                print(l.get_attribute('href').strip())
                print()


        # todo: test this
        if config.SequentialFiles:

            """
            This marks the download mode that done with requests module.
            After a completed download, it will wait for interval between files

            For now, I am upset to say that apkpure.com can not be downloaded using requests module yet.
            I think it must be possible, I just did not find the way yet.
            
            Other common case like github etc is fine with this code, I just still don't know why.
            
            Warning: not tested yet
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
                    is_downloadable, header = lib.is_downloadable(file_url, cookies = cookies, header = config.RequestHeader, proxy = proxy_list[proxy_counter])


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
                        request_result = lib.download_binary(file_url, cookies = cookies, header = config.RequestHeader, proxy = proxy_list[proxy_counter])

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
            This marks the code for Downloading with Selenium
            After a click, it will wait for interval between files

            Note that this will *not* check for file completion. 
            The code will wait for interval only.
            After interval time is over, browser will continue to click again.
            """

            element_clicked = 0
            # todo: make the code below to be adaptive according to the xpath attribute (see F1 lib's)
            element_as_string = [(element.get_attribute('title'), element.get_attribute('href')) for element in element_founds]
            for index, (title, link) in enumerate(element_as_string):

                if isinstance(config.IntervalsBetweenFiles, tuple):
                    wait_time = randint(config.IntervalsBetweenFiles[0], config.IntervalsBetweenFiles[1])
                else:
                    wait_time = config.IntervalsBetweenFiles

                print("\t\t [{}/{}] {} | and wait for {} second(s)".format(index + 1, len(element_as_string), title, wait_time))


                """
                Here, we are actually opening the link instead of clicking it.
                
                I tested with each of pros and cons, and as far as I see with apkpure.com, it is better to open it than clicking it.
                
                click -> if element is not visible, it will produce an error (I just feel that it is too risky for error compared to visiting it)
                """
                driver.get(link)
                element_clicked += 1
                logger_file.info('Selenium download : ' + title)
                driver.implicitly_wait(wait_time)

            # log the report of each xpath found on the link
            logger_url.info('URL {}, XPath {}: | {}/{} element(s) clicked with Selenium'.format(url[1], xpath[1], element_clicked, len(element_as_string)))

    # log the successful link
    logger_link_done.info(url[1])

    if isinstance(config.IntervalsBetweenFiles, tuple):
        link_wait_time = randint(config.IntervalsBetweenFiles[0], config.IntervalsBetweenFiles[1])
    else:
        link_wait_time = config.IntervalsBetweenFiles

    print('Waiting {} second(s) for the next URL'.format(link_wait_time))
    time.sleep(link_wait_time)

    """
    If it is the time to renew session/proxy, close the old driver
    """
    if url[0] % config.URLCountToSwitch == 0:

        # quit is better than close, as close maybe left background task
        # driver.close()
        driver.quit()
        driver = None


print("Done.")

