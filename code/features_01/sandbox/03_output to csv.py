"""
import pandas as pd
df = pd.DataFrame(columns=['Title', "Links"])
df.head()
Empty DataFrame
Columns: [Title, Links]
Index: []
a = [{"title": "title 1", "links": "link 1"}, {"title": "title 1", "links": "link 1"}]
a
[{'title': 'title 1', 'links': 'link 1'}, {'title': 'title 1', 'links': 'link 1'}]
df = pd.DataFrame(a)
df.head()
    links    title
0  link 1  title 1
1  link 1  title 1
df.to_csv("result.csv")
df.to_csv("result.csv", index = False)


"""