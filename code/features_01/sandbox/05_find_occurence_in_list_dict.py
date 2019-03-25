a = [{"title": "title 1", "link": "link 1"}, {"title": "title 2", "link": "link 2"}]


# list(filter(lambda x: x['title'] == 'title 1', a))
print(list(filter(lambda x: x.get('title', None) == 'title 1' or x.get('link', None) == 'link 2', a)))
