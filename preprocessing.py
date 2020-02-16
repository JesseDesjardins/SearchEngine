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
file1 = open('test.txt', 'w')

main_table = soup.find_all("div", attrs={'class': 'courseblock'})
for course in main_table:

    data[str(docid)] = []
    course_name = course.find_next("p", attrs={'class': 'courseblocktitle'})
    course_desc = course.find_next("p", attrs={'class': 'courseblockdesc'})
    course_extra = course.find_all("p", attrs={'class': 'courseblockextra'})
    course_extra_string = ""
    for extras in course_extra:
        course_extra_string = course_extra_string + extras.text + " "

    # data[str(docid)].append(str(course_name))
    # data[str(docid)].append(str(course_desc))
    # data[str(docid)].append(course_extra_string)

    data[str(docid)] = {
        'name': str(course_name),
        'desc': str(course_desc),
        'extra': course_extra_string
    }

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

    print("------")
    print(course.text)
    docid += 1

file1.close()
docnum = docid

print(docnum)

