"""
Main code for F1
"""
import importlib
import re
import pandas as pd

lib = importlib.import_module('lib_common')
config = importlib.import_module('config_01')

url_list = lib.readUrl()
if not url_list:
    print("URLS.txt not found.")
    exit(1)

list_data = []
regex_instance_list = lib.compile_regex(config.Regex)
list_attribute = lib.regex_xpath_to_attribute(config.XPath)



for url in enumerate(url_list):
    print("Scraping URL ({}/{}) from URLs.txt Using XPath ...".format(url[0] + 1, len((url_list))))

    # todo: request the url
    # html_page = lib.get_page(url)

    # todo: scrap for any links
    with open("example.html") as html_file:
        html_page = html_file.read()

    # print(html_page)
    links_found = lib.scrap_html(html_page)


    if links_found:
        # todo: CSV Operation. store title and the link on csv
        # todo IMPORTANT: it should be able to get the @attribute, maybe should have been built using class

        print("\tAdding Results to Output.csv ...  ({} link(s) found)".format(len(links_found)))
        for link in links_found:

            a_row = {}
            for attribute in list_attribute:
                a_row[attribute] = link.get(attribute, '')

            list_data.append(a_row)

        for i in list_data:
            print(i)

        # todo: the csv can be saved now with the code below, but it is better to evaluate regex, find occurence, etc first, and then be saved to csv. This will improve the speed better.
        # lib.write_csv(list_data, columns = list_attribute)

        # fixme: remove break after testing
        break

    else:
        print("\tNo links found. The XPATH might be wrong or the page did not contains given XPATH.")

    # todo: should initiate the csv here
    # todo: might be better to evalate all the given condition before saving the csv. e.g. better to regex it first, then remove multiple occurence, and finaly save it. will be much efficient.
    # insert


# todo
print("Regex Search & Replace in Output.csv ...")
# make a function that if called, will iterate each row and re.sub the title and links
for row in list_data:
    for attribute in list_attribute:
        row[attribute] = lib.regex_string(row[attribute], regex_instance_list)

# at this point, all the element should be replaced with regex. to check it, run the code below
for row in list_data:
    print(row)

exit()


# todo
print("Removing Rows In Output.csv If The Row Also In Done.csv ...")
# check if Done.csv is there
# if yes, read it and evaluate the occurrence. remove the duplicate of list_data, and add(append) the list_data to Done.scv
# if no, create empty Done.csv

# todo
print("Removing Rows With Same Column # Values Except 1st Occurrence In Output.csv ...")


# save csv
lib.write_csv(list_data, columns=list_attribute)


