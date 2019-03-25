"""
Cofiguration File for F1
"""

"""
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

XPath = "//a[@title|@href]"
# XPath = "/html/body/div[1]/div/a/[@title|@href]"



"""
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
    ("(?<=\d\/).+", ""),
    ("(\/([ab])\/)", "/x/"),
    ("EFG ?(?="")", " XYZ"),
)

# todo: make sure to clarify how should the logic works if multiple column is given
Column = (
    'B',
    'C',
    'D'
)


DebugMode = True