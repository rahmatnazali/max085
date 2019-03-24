import importlib
config = importlib.import_module('config_01')

import os
import requests
import re


"""
Regarding reading URL, HTML request, and scrapping
"""

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


"""
Regarding regex
"""



def regex_string(string, regex_instance_list):
    for regex in regex_instance_list:
        string = re.sub(regex['regex_instance'], regex['regex_string'], string)
    return string

def compile_regex(regex_tuple):
    regex_instance = []
    for regex in regex_tuple:
        regex_instance.append({
            'regex_instance': re.compile(regex[0]),
            'regex_string': regex[1]
        })
    return regex_instance

def regex_xpath_to_attribute(xpath_string):
    # todo: should compile it first, for efficiency boost
    # regex = re.compile("@\w+")
    # print(re.findall(regex, xpath_2.split("/")[-1]))

    xpath_string = xpath_string.split("/")[-1] if "/" in xpath_string else xpath_string
    result = re.findall("@\w+", xpath_string)
    return [attribute.replace('@', '') for attribute in result]




"""
Regarding CSV operation
"""

import pandas as pd
def write_csv(list_data, columns, filename = 'result.csv'):
    # todo: tested, but column is in sorted format . should research how to not auto-order
    df = pd.DataFrame(list_data, columns=columns)
    df.to_csv(filename, index=False)
list_data = [{"title": "title 1", "links": "link 1"}, {"title": "title 1", "links": "link 1"}]


# test here
# print(regex_xpath_to_attribute("//a[@title|@href]"))
# write_csv(list_data, ['title', 'links'])
