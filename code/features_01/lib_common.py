import importlib
config = importlib.import_module('config_01')

import os
import requests

def readUrl(filename = "URLS.txt"):
    """

    :param filename:
    :return:
    """
    url_list = []
    if os.path.isfile(filename):
        with open(filename) as url_file:
            for line in url_file:
                if not line.startswith("#"):
                    url_list.append(line.strip())
                    if config.DebugMode:
                        print(line.strip())
        return url_list
    return False

def get_page(url):
    """

    :param url:
    :return: string
    """
    request_result = requests.get(url)
    if requests.status_codes == 200:
        return request_result.text


from lxml import html
def scrap_html(html_page):
    tree = html.fromstring(html_page)
    result_elements = tree.xpath(config.XPath)
    return result_elements
