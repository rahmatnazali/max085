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
    else:
        print("Request failed. The link might be wrong, or there is no internet connection")
        exit()

from lxml import html
def scrap_html(html_page, Xpath):
    """
    A function to scrap html based on its XPath
    :param html_page: the html page
    :return: a list of element found. if no elements found, it will return empty list []
    """
    tree = html.fromstring(html_page)
    result_elements = tree.xpath(Xpath)
    return result_elements


"""
Regarding regex
"""

def compile_regex(regex_tuple):
    """
    A function to compile regex
    because we will use this regex multiple time, we should compile it first for efficiency boost
    :param regex_tuple: Regex variable from config_01.py
    :return: list or compiled regex instance
    """

    regex_instance = []
    for regex in regex_tuple:
        regex_instance.append({
            'regex_instance': re.compile(regex[0]),
            'regex_string': regex[1]
        })
    return regex_instance

def regex_content(list_data, list_attribute, regex_instance_list):
    """
    A function that, given the list_data, list_attribute, and compiled regex instance,
    will iterate to each content and replace it with each compiled regex
    :param list_data:
    :param list_attribute:
    :param regex_instance_list:
    :return: list_data that already replaced with regex
    """
    for row in list_data:
        for attribute in list_attribute:
            row[attribute] = regex_string(row[attribute], regex_instance_list)
    return list_data

def regex_string(string, regex_instance_list):
    """
    A function, given string and list of compiled regex,
    will replace the string with each of compiled regex

    This function will be run several times, called by regex_content
    :param string:
    :param regex_instance_list:
    :return:
    """
    for regex in regex_instance_list:
        string = re.sub(regex['regex_instance'], regex['regex_string'], string)
    return string


# todo: this is unused
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
import datetime
import pandas as pd
def write_csv(list_data, columns, filename = 'result.csv'):

    filename = filename.replace('.csv', '') if filename.endswith('.csv') else filename
    filename = filename + '_' + str(datetime.datetime.now())[:19].replace(":", '_') +'.csv'

    df = pd.DataFrame(list_data, columns=columns)
    df.to_csv('result/' + filename, index=False)
    return filename
#
# list_data = [{"title": "title 1", "links": "link 1"}, {"title": "title 1", "links": "link 1"}]
# columns = ['title', 'links']
# write_csv(list_data, columns)


# fix me: reading Done.csv in dataframe result somethink like this
"""
           href
title          
title 1  link 1
title 1  link 1

it should be like this

title    href
title 1  link 1
title 1  link 1

"""
def read_done_csv():
    return []
    if os.path.isfile("result/Done.csv"):
        df = pd.DataFrame.from_csv("result/Done.csv", sep=',')
        print(df)
        return df
    else:
        return []

# todo: write the unittest
import unittest
import os
class LibCommonTest(unittest.TestCase):
    def test_write_csv_can_produce_csv(self):
        list_data = [{"title": "title 1", "links": "link 1"}, {"title": "title 1", "links": "link 1"}]
        columns = ['title', 'links']
        result_filename = write_csv(list_data, columns)
        is_file_there = os.path.isfile('result/' + result_filename)
        self.assertTrue(is_file_there)
        try:
            os.remove(result_filename)
        except OSError:
            pass

    def test_regex_path_attribute_can_retrieve_attribute_correctly(self):
        self.assertEqual(['title', 'href'], regex_xpath_to_attribute("//a[@title|@href]"))

    def test_obtain_done_csv_data(self):
        read_done_csv()
