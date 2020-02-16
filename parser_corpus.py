import string
from bs4 import BeautifulSoup
import requests
import io
import xml.etree.ElementTree as ET
import os


# from HTMLParser import HTMLParser
# from lxml import etree


def xml_out(out):
    from xml.sax.saxutils import escape

    inner_template = string.Template("""<Document>${num}
            <DocID> ${Doc_ID} </DocID>
            <Title>  ${Title} </Title>
            <Description> ${Desr} </Description>
    </Document>""")

    outer_template = string.Template("""<root>
    ${document_list}  
</root>""")
    data = []
    for i in range(len(out)):
        dat = [[i, out[i][0], out[i][1], out[i][2]]]
        data = data + dat

    inner_contents = [inner_template.substitute(num=num, Doc_ID=Doc_ID, Title=Title, Desr=Desr) for
                      (num, Doc_ID, Title, Desr) in data]
    result = outer_template.substitute(document_list='\n'.join(inner_contents))
    result = result.replace("&", "&amp;")
    f = open("corpus_csi.xml", "w+")
    f.write(result.encode('gbk', errors='ignore').decode('utf-8', errors='ignore'))


def parser(soup):
    results = soup.find_all('div', attrs={'class': 'courseblock'})
    output = []
    for i in range(len(results)):
        course = []
        docID = results[i].find('strong').text
        title = docID[9:]
        docID = docID[0:8]

        node = results[i].find('p', attrs={'class': 'courseblockdesc noindent'})
        if node is not None:
            description = node.text
        else:
            description = 'None'
        course.append(docID)
        course.append(title)
        course.append(description)
        output.append(course)
    return output


def split_docs():
    context = ET.iterparse('corpus_csi.xml', events=('end',))
    for event, elem in context:
        if elem.tag == 'Document':
            title = elem.text.strip()
            title = title + ".xml"
            filename = format(title)
            with open(os.getcwd() + "/documents/" + filename, 'wb') as f:
                f.write(ET.tostring(elem))


def mainFun():
    url = 'https://catalogue.uottawa.ca/en/courses/csi/'

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    out = parser(soup)
    xml_out(out)
    # split documents to multiple dos
    split_docs()


if __name__ == '__main__':
    # main start function
    mainFun()
