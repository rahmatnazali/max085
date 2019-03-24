import importlib
config = importlib.import_module('config_01')

import os
import requests
import re

# todo: test
def compile_regex():
    regex_instance = []
    for regex in config.Regex:
        regex_instance.append({
            'regex_instance': re.compile(regex[0]),
            'regex_string': regex[1]
        })
    return regex_instance

def bulk_regex(string, regex_instance_list):
    for regex in regex_instance_list:
        string = re.sub(regex['regex_instance'], regex['regex_string'], string)
    return string

def readUrl(filename = "URLS.txt"):
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
    request_result = requests.get(url)
    if requests.status_codes == 200:
        return request_result.text


from lxml import html
def scrap_html(html_page):
    tree = html.fromstring(html_page)
    result_elements = tree.xpath(config.XPath)
    return result_elements
