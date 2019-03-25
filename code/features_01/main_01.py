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



# todo: populate link_list with href from Done.csv
link_list = lib.read_done_csv() # each link from Done.csv AND links found from current scraps will be stored here. It is guaranteed that no duplicate link exist here

list_data = [] # list of row data to be converted to CSV later

regex_instance_list = lib.compile_regex(config.Regex) # compiled regex

list_attribute = lib.regex_xpath_to_attribute(config.XPath) # list of attributes



for url in enumerate(url_list):
    print("Scraping URL ({}/{}) from URLs.txt Using XPath ...".format(url[0] + 1, len((url_list))))

    # get url page. commented for now for testing purpose.
    # html_page = lib.get_page(url)

    # for testing purpose
    with open("example.html") as html_file:
        html_page = html_file.read()

    # scrap the html based on its xpath
    links_found = lib.scrap_html(html_page, config.XPath)


    if links_found:
        print("\tAdding Results to Output.csv ...  ({} link(s) found)".format(len(links_found)))
        for link in links_found:

            a_row = {}
            for attribute in list_attribute:
                an_attribute = link.get(attribute, '')
                regexed_attribute = lib.regex_string(an_attribute, regex_instance_list)
                a_row[attribute] = regexed_attribute

            """
            An occurrence is evaluated here.
            If href is in link_list, then ignored it.
            If href is not in link_list, add it
            """
            # print("Regex Search & Replace in Output.csv ...")
            if a_row['href'] not in link_list:
                link_list.append(a_row['href'])
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

# [DONE] Regex is already done in iteration. This will be more efficient
print("Regex Search & Replace in Output.csv ...")

# to check, at this point all the element should be replaced with regex at iteration, run the code below
# for row in list_data:
#     print(row)


# [DONE] multiple occurrence in Rows is already evaluated in iteration. This will be more efficient
print("Removing Rows In Output.csv If The Row Also In Done.csv ...")


# todo: should evaluate config.column
print("Removing Rows With Same Column # Values Except 1st Occurrence In Output.csv ...")


# save csv
lib.write_csv(list_data, columns=list_attribute)


