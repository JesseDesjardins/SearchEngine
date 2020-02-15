# import bs4 as bs
from bs4 import BeautifulSoup
import urllib
import codecs
import json

f = open("corpustest.html")
content = f.read()
soup = BeautifulSoup(content, 'html.parser')

# print(soup.prettify())

docid = 0
data = {}


main_table = soup.find_all("div", attrs={'class': 'courseblock'})
for course in main_table:
    docid += 1
    test = course.text
    data[str(docid)] = []
    data[str(docid)].append(course.text)
    print("------")
    print(course.text)

docnum = docid

print(docnum)

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
