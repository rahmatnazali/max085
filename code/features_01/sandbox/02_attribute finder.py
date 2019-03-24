import re

xpath = "/html/body/div[1]/div/a/(@title|@href)"

print(re.findall("/([@])\w+/g", xpath)) # should have been worked