import importlib
config = importlib.import_module('config_01')

import requests
import re
from lxml import html
import datetime
import pandas as pd
import unittest
import os



"""
Regarding reading URL, HTML request, and scrapping
"""

def read_url(filename = "URLS.txt"):
    """
    Open file that contains the URL, and obtains all valid URL
    :param filename: filename to look for URL
    :return: the url_list (list    or   False (boolean) if empty
    """
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
        return url_list
    return False


def get_page(url):
    """
    Get the URL's HTML by doing a GET Request
    :param url: url to be fetched
    :return: The HTML (string)
    """
    request_result = requests.get(url)
    if requests.status_codes == 200:
        return request_result.text
    else:
        print("Request failed. The link might be wrong, or there is no internet connection")
        exit()


def scrap_html(html_page, list_attribute, Xpath):
    """
    Scrap html based on given XPath
    :param html_page: string of HTML page
    :param list_attribute: list of attribute. Obtained from config.XPath.keys()
    :param Xpath: the XPath(s)
    :return: result_dict (dictionary): A dictionary that contains the list of results    and    data_found_length (integer): number of row found
    """
    data_found_length = 0
    tree = html.fromstring(html_page)
    result_dict = {}

    # for every attributes, find it all by xpath
    for attribute in list_attribute:
        result_dict[attribute] = tree.xpath(Xpath[attribute])
        if len(result_dict[attribute]) > data_found_length:
            data_found_length = len(result_dict[attribute])

    # check if there is still an lxml <Element> type (not string). If so, convert it to string
    for attribute in list_attribute:
        if len(result_dict[attribute]) and not isinstance(result_dict[attribute][0], str):
            result_dict[attribute] = [x.text_content() for x in result_dict[attribute]]
    return result_dict, data_found_length






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
    :param list_data: list of raw data
    :param list_attribute: list of attribute
    :param regex_instance_list: compiled regex
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


"""
Regarding CSV operation
"""

def write_csv(list_data, columns, filename = 'Output.csv'):
    """
    Write list_data to CSV with columns as attribute and filename as the filename
    :param list_data: list of row to be inserted (list of dict)
    :param columns: list of attribute to be shown as column (list of string)
    :param filename: csv file name
    :return: csv filename (should any caller needed)
    """
    filename = filename.replace('.csv', '') if filename.endswith('.csv') else filename
    filename = filename + '_' + str(datetime.datetime.now())[:19].replace(":", '_') +'.csv'

    data_frame = pd.DataFrame(list_data, columns=columns)
    data_frame.to_csv('result/' + filename, index=False)
    return filename


def read_done_csv(list_attribute):
    """
    Will read Done.csv if given, and store the occurred value into it
    If Done.csv is not given, the default value is empty list []
    :param list_attribute: list of attributes
    :return: dicitonary of list contains occurred elements
    """
    result_dict = {}
    for attribute in list_attribute:
        result_dict[attribute] = []

    if os.path.isfile("result/Done.csv"):
        df = pd.read_csv("result/Done.csv", sep=',')

        for attribute in list_attribute:
            if attribute in df.columns:
                result_dict[attribute] = df[attribute].to_list()

    return result_dict

# todo: write the unittest
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
