from lxml import html

with open('../example.html') as html_file:
    html_data = html_file.read()

webpage = html.fromstring(html_data)

result = webpage.xpath("//a[@title|@href]")
print(len(result))
for link in result:
    print(link, link.get('title'), link.get('href'))