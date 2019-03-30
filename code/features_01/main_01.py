"""
Main code for F1
"""

import importlib
import logging

lib = importlib.import_module('lib_common')
config = importlib.import_module('config_01')


"""
Reading URLS.txt

If no URLS.txt was given, the code will end.
"""
url_list_succeed = 0
url_list, url_done_list = lib.read_url()
if not url_list:
    print("URLS.txt not found.")
    exit(1)


"""
Creating logging instance
"""
# logger for Links-Errors.txt
logger_link = lib.setup_logger("logger_link", 'log/Links-Errors.txt')
logger_link_count = 0

# logger for LinkDone
logger_link_done = lib.setup_link_done_logger('logger_link_done', 'log/URLsDone.txt')

# logger for XPaths-error.txt
logger_xpath = lib.setup_logger("logger_xpath", 'log/XPaths-Errors.txt')
logger_xpath_count = 0


"""
List of attributes to be evaluated

for config.XPath like these:
XPath = {
    'Product Title' : '//*[@id="app"]/div/div[2]/div/div/div[3]/div[1]/section[*]/div/div[2]/a[1]/section/p[1]',
    'Image URL'     : '//*[@id="app"]/div/div[2]/div/div/div[3]/div[1]/section[*]/div/a/div/div/img/@src',
    'Model Number'  : '//*[@id="app"]/div/div[2]/div/div/div[3]/div[1]/section[*]/div/div[2]/a[1]/section/p[2]',
    'Link'          : '//*[@id="app"]/div/div[2]/div/div/div[3]/div[1]/section[*]/div/div[2]/a[1]/@href',
}

this variable will holds array ['Product Title', 'Image URL', 'Model Number', 'Link']
"""

list_attribute = list(config.XPath.keys())







"""
Dictionary of occured data (occured_data_dict)

This dictionary will store appearance of data.
If Done.csv is there, code will import all the content from Done.csv (marked it as "occured").
If Done.csv is not given, code will return empty list (means no occurrence happened yet)

Before insertion of an element to the final dictionary, code will check IF it is already in this dict.
If there is (means multi occured), code will ignore it and continue
If there is not (means no occurrence happened yet), code will append it, and add to this dictionary to marked it as "occurred"

It is guaranteed that no duplicate elements per attribute exist here because code 
will only append element to the attribute if no elements was found inside.
"""

occured_data_dict = lib.read_done_csv(list_attribute)





"""
List of row data to be logged in CSV.

At first it was emtpy list []
It will get populated once elements is found.
In the end it will be written to CSV
"""

csv_data = []





"""
Compiling Regex

We can have a lot of regex, and we will use it for every elements.
So first we need to compile it so that later we don't need to compile it anymore.
Here we are reusing regex instead of deleting it and keep instantiating it every regex operation.
"""

regex_instance_list = lib.compile_regex(config.Regex)


"""
Initializing data_found_dict
This variable will need to be initialized because we want to know later how much regex is matched

this is fix for F1-Testing_01-Notes.txt: 
* Regex Search & Replace in Output.csv ... (#/# Regex Matched) -> example: if I entered 4 regex in config and the software matched 3 of them in output.csv (3/4 Regex Matched)
"""
data_found_dict = {}





"""
this is fix for F1-Testing_01-Notes.txt: 
* Removing Rows In Output.csv If The Row Also In Done.csv ... (# Rows Removed)
"""
rows_removed_due_to_appearance_in_done_csv = 0




"""
this is fix for F1-Testing_01-Notes.txt: 
* Removing Rows With Same Column # Values Except 1st Occurrence In Output.csv ... (# Rows Removed)
"""
rows_removed_due_to_duplicate_in_output_csv = 0





"""
Main Code

This marks the main operation code.

The logical is like this:

    for every url that we got:
        request the url's page and save the HTML Page
        for every cofig.XPath attribute we have:
            search for it
            if found:
                regex it
                then merrge all the result to each of its row (so that say, 'Product Title', 'Image URL', 'Model Number', 'Link' of a same row is merged to form a row)
                for every row:
                    check if row is already in occured_data_dict
                    if not there (means not occured) --> insert to data csv --> mark this occurrence in occured_data_dict
                    else just ignore and continue
    
    if csv_data is filled with data --> write it to csv
        
"""

number_of_regex = len(config.Regex)
number_of_regex_found = 0

for url in enumerate(url_list):
    if url[1] in url_done_list:
        print('Skipping already done link: {}'.format(url[1]))
        print()
        continue

    print("Scraping URL ({}/{}) from URLs.txt Using XPath ... | {}".format(url[0] + 1, len((url_list)), url[1]))

    if config.TestMode:
        # for testing purpose
        with open("example_2.html", encoding='utf-8') as html_file:
            html_page = html_file.read()
    else:
        request_result = lib.get_page(url[1])

        if request_result.status_code == 200:
            html_page = request_result.text
        else:
            if request_result.status_code == 404:
                print("\t[404] Request failed. Link not found")
                print()
            else:
                print("\t[{}] Request failed. The link might be wrong, or there is no internet connection".format(request_result.status_code))
                print()

            logger_link.warn("[{}] Get Request failed for link: {}".format(request_result.status_code, url[1]))
            logger_link_count += 1
            continue


    """
    Scrap the html based on its xpath, and return two things:
    
    data_found_dict     : the dictionary of elements found (it is still raw. not regexed, not checked for occurrence)
    data_found_length   : the length of the data found (i.e. rows found). Zero means no data found. 11 means 11 rows is found
    """
    data_found_dict, data_found_length = lib.scrap_html(html_page, list_attribute, config.XPath)

    if data_found_length:
        print("\tAdding Results to Output.csv ...  ({} row(s) of data found)".format(data_found_length))
        if config.DebugMode:
            print()
            print('below is all the elements found (regexed, but not evaluated for multi occurence)')

        """
        Each attribte is obtained and merged into one row each
        Then each of it is cleaned with regex
        """
        for i in range(data_found_length):
            a_row = {}

            regex_found_per_row = 0
            for attribute in list_attribute:
                a_row[attribute], regex_found_per_attribute = lib.regex_string(data_found_dict[attribute][i], regex_instance_list)
                regex_found_per_row += regex_found_per_attribute

            # Before, we get 1/4 instead of 2/4 because I minimzie it. Now it will be maximized
            number_of_regex_found = max(number_of_regex_found, regex_found_per_row)

            if config.DebugMode:
                # print string that is regexed, but not yet evaluated for occurence (so multi occurence is possible)
                print(a_row)

            """
            An occurrence is evaluated here.
            If columns specified in config_01.py.Columns is found duplicated, it will not be inserted.
            If attribute is not in occured_data_dict, add it to the dict, so that no occurence of this element will appear.
            """
            # if occurrence appears according to config.Columns, mark as duplicate and break
            is_duplicate = False
            for attribute in config.Columns:
                if a_row[attribute] in occured_data_dict[attribute]:
                    is_duplicate = True
                    rows_removed_due_to_appearance_in_done_csv += 1
                    break

            # if not marked as duplicate, then insert the row to csv_data. Also record this row as "occurred"
            if not is_duplicate:
                for attribute in list_attribute:
                    occured_data_dict[attribute].append(a_row[attribute])

                # add the data to csv_data
                csv_data.append(a_row)

        if config.DebugMode:
            # print processed element (string is regexed and multi occurence will not exist)
            print()
            print("belows print unique data, ready to be inserted to CSV")
            for element in csv_data:
                print(element)

            print()
            print('below is the dictionary of occurence at the end of process')
            print(occured_data_dict)
            print()

        # if the link have successfully requested and scrapped for result, log it into URLSDone.txt and increment the URL Done counter
        logger_link_done.info(url[1])
        url_list_succeed += 1
    else:
        print("\tNo data found. The XPATH might be wrong or the page did not contains given XPATH.")
        print()

        logger_xpath.error("XPath not found for link: " + url[1])
        logger_xpath_count += 1

        continue

    if config.TestMode:
        break

    print("\tRegex Search & Replace in Output.csv ... ({}/{} Regex Matched)".format(number_of_regex_found,
                                                                                    number_of_regex))

    # cosmetic
    print()

# [DONE] Regex is already done in iteration. This will be more efficient
# We already printed in every row, so for now I will comment this
# print("Regex Search & Replace in Output.csv ... ({}/{} Regex Matched)".format(number_of_regex_found, number_of_regex))

# [DONE] multiple occurrence in Rows is already evaluated in iteration. This will be more efficient
print("Removing Rows In Output.csv If The Row Also In Done.csv ... ({} Rows Removed)".format(rows_removed_due_to_appearance_in_done_csv))


"""
[DONE] Saving CSV

Default filename is Output_datetime.csv

You can modify the filename by calling below function like so:
lib.write_csv(csv_data, columns=list_attribute, filename = "My Custom Output Name")

that will generate file with name: My Custom Output Name_datetime.csv

"""
rows_removed_due_to_duplicate_in_output_csv = lib.write_csv(csv_data, columns=list_attribute)


# [DONE] multiple occurrence in Rows regarding specified Columns is already evaluated in iteration. This will be more efficient
print("Removing Rows With Same Column # Values Except 1st Occurrence In Output.csv ... ({} Rows Removed)".format(rows_removed_due_to_duplicate_in_output_csv))




print("\n\n\n")
print("URLs Completed Logged in (URLsDone.txt): {}/{} TotalURLs".format(url_list_succeed, len(url_list)))
print("Errors Logged in (Links-Errors.txt): {}".format(logger_link_count))
print("Errors Logged in (XPaths-Errors.txt): {}".format(logger_xpath_count))

