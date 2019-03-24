"""
Main code for F1
"""
import importlib
lib = importlib.import_module('lib')

url_list = lib.readUrl()
if not url_list:
    print("URLS.txt not found.")
    exit(1)

for url in enumerate(url_list):
    print("Scraping URL ({}/{}) from URLs.txt Using XPath ...".format(url[0] + 1, len((url_list))))

    # todo: request the url
    html_page = lib.get_page(url)

    # todo: scrap for any links
    links_found = lib.scrap_html(html_page)

    if links_found:
        # todo: CSV Operation. store title and the link on csv
        print("\tAdding Results to Output.csv ...")
    else:
        print("\tNo links found. The XPATH might be wrong or the page did not contain given XPATH.")

# todo
print("Regex Search & Replace in Output.csv ...")
print("Removing Rows In Output.csv If The Row Also In Done.csv ...")
print("Removing Rows With Same Column # Values Except 1st Occurrence In Output.csv ...")

