from bs4 import BeautifulSoup
import json

def preprocess_courses_corpus():
    soup = None
    with open('courses_corpus.html', 'r') as infile:
        content = infile.read()

    soup = BeautifulSoup(content, 'html.parser')

    docid = 0
    data = {}
    data['documents'] = []

    main_table = soup.find_all("div", attrs={'class': 'courseblock'})
    for course in main_table:
        docid += 1
        title = course.find_all('p', attrs={'class':'courseblocktitle noindent'})[0].text.lstrip('\n') if len(course.find_all('p', attrs={'class':'courseblocktitle noindent'}))!=0 else ''
        description = (course.find_all('p', attrs={'class':'courseblockdesc noindent'})[0].text.lstrip('\n') if len(course.find_all('p', attrs={'class':'courseblockdesc noindent'}))!=0 else '') + ' ' + (course.find_all('p', attrs={'class':'courseblockextra noindent'})[0].text if len(course.find_all('p', attrs={'class':'courseblockextra noindent'}))!=0 else '')

        data['documents'].append({
            'docId' : docid,
            'title' : title.strip(),
            'description' : description.strip()
        })

    with open('courses_data.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
    preprocess_courses_corpus()