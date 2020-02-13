# import bs4 as bs
from bs4 import BeautifulSoup
import urllib
import codecs


f = open("corpus.html")
content = f.read()
soup = BeautifulSoup(content, 'html.parser')

print(soup.prettify())

