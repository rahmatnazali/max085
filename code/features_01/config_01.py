"""
Cofiguration File for F1
"""

"""
XPath

This variable will let the code know "What attribute is" and "How to Find it"

Format:

XPath = {
    'ATTRIBUTE_TITLE' : 'XPATH_FOR_FINDING_IT',
    'ATTRIBUTE_TITLE' : 'XPATH_FOR_FINDING_IT',
    'ATTRIBUTE_TITLE' : 'XPATH_FOR_FINDING_IT',
}


----------------------------------------------------
There is some note before using XPATH variable.

What you should know is that XPATH also have version. The older version is around 1.x (used by majority of browser).
The newest one are XPATH version 2.0, which is prettier but not all webdriver are able to support it.

--Example--
You gave an XPath example like so: /html/body/div[1]/div/a/(@title|@href)
This XPATH is in version 2.0. So, should any error happens, you must convert the XPATH to version 1.x, which is actually pretty simple, like so:

v1.x: /html/body/div[1]/div/a/(@title|@href)
v2.0: /html/body/div[1]/div/a/[@title|@href]
*notice the bracket changes from () to []. For old version, you should really use [] rather than ()



You will also notice that majority of browser are still not suppurting XPATH v2.0. 
This might be a consideration for your future affair regarding web automation with XPATH.

Further reference: 
https://stackoverflow.com/questions/1936301/can-i-use-xpath-2-0-with-firefox-and-selenium
https://stackoverflow.com/questions/55319552/python-selenium-how-to-make-webdriver-use-xpath-version-2-0

"""

XPath = {
    'Tite': '//div[3]/div[2]/div[1]/div/div[2]/a',
    'Price': '//*[@id="store_form"]/div/div[2]/div/div[1]/div[2]',
    'ImageURL': '//div[3]/div[2]/div[1]/div/div[1]/a/img/@src',
    'Link': '//div[3]/div[2]/div[1]/div/div[1]/a/@href',
    'ReleaseDate' : '//div[3]/div[2]/div[1]/div/div[2]/div[1]/div[2]',
    'Another example field': '//div[3]/div[2]/div[1]/div[14]/div[2]/div[1]/div[2]'

    # 'Product Title' : '//*[@id="app"]/div/div[2]/div/div/div[3]/div[1]/section[*]/div/div[2]/a[1]/section/p[1]',
    # 'Image URL'     : '//*[@id="app"]/div/div[2]/div/div/div[3]/div[1]/section[*]/div/a/div/div/img/@src',
    # 'Model Number'  : '//*[@id="app"]/div/div[2]/div/div/div[3]/div[1]/section[*]/div/div[2]/a[1]/section/p[2]',
    # 'Link'          : '//*[@id="app"]/div/div[2]/div/div/div[3]/div[1]/section[*]/div/div[2]/a[1]/@href',
}


"""
List of Regex that will be used.

This is a tuple of tuple type. Make sure to wrap each elements with bracket.

Format:

Regex = (
    ("REGEX_PATTERN", "REPLACE_WITH_WHAT"),
    ("REGEX_PATTERN", "REPLACE_WITH_WHAT"),
    ("REGEX_PATTERN", "REPLACE_WITH_WHAT"), # a comma at the end of last element is fine
)

^ don't forget the closing bracket for Regex variable

"""

Regex = (
    ("(?<=\/)en\/", ""),
    ("TESTNOMATCH", ""),
    ("Call of Duty", "COD"),
    ("REGEXTHATWILLNEVERMATCH", " XYZ"),

    # ("(?<=\d\/).+", ""),
    # ("(\/([ab])\/)", "/x/"),
    # ("EFG ?(?="")", " XYZ"),
    # ("REGEXTHATWILLNEVERMATCH", " XYZ"),
)




"""
Place your column that you did not want it to be multiple-occurred

For example, we want so that "Link" is not multiple-occurred, so we put "Link" in the Column below.

Note:
1. The attribute listed on the Column *must also be defined in XPath*, if not, the code will got confused because
he seeks something that did not there
2. the Done.csv *should also* contains the same attributes that defined in XPath

Important: the Columns is tuple type, so you should put a comma if you only insert one attribute. like this --> ("attribute", )

If Columns is empty (i.e. empty tuple () ), then no occurence will be evaluated --> multiple occurence is possible
"""
Columns = (
    'Link', # this means "Links" will be evaluated should multi occurrence happens
)


"""
To Test 
(Not actually requesting. just use the samsung.com's html you gave as an html_page)
value: True | False
"""

TestMode = False




"""
To Debug
Will print every data verbosely
value: True | False
"""

DebugMode = False



"""
This is a fix for

True -> the software as it is, no change.
False -> instead of creating new output-time.csv files on every run, append all results to the end or begening of output.csv

"""
GenerateNewFiles = True



RequestHeader = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}