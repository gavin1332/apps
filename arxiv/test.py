import requests
import re

url = 'http://arxiv.org/list/cs.CV/recent'
html = requests.get(url).content
print html

def paper_title(page):
    myItems = re.findall('<span class="descriptor">Title:</span>(.*?)</div>',page,re.S)

    for item in myItems:
        print(item)

paper_title(html)
