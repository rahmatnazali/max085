import re

xpath = "/html/body/div[1]/div/a/(@title|@href)"
xpath_2 = "/html/body/div[1]/div/(@class)/a/(@title|@href)"

# print(xpath.split("/")[-1])
# print(re.findall("/([@])\w+/g", xpath)) # should have been worked

# print(re.findall("@\w+", xpath)) # should have been worked

# print(re.findall("@\w+", xpath_2))
print(re.findall("@\w+", xpath_2.split("/")[-1]))

# todo: should compile it first, for efficiency boost
regex = re.compile("@\w+")
print(re.findall(regex, xpath_2.split("/")[-1]))
