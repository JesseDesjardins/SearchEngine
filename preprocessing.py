from bs4 import BeautifulSoup
import os
import json

def preprocess_courses_corpus():
    """ Runs the pre-processing on the Courses corpus """
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

def preprocess_reuters_corpus():
    """ Runs the pre-processing on the Reuters corpus 
    
    Saves the title, body and topics of each Reuters article"""

    soup = None
    data = {}
    data['documents'] = []

    infile_directory = os.path.join(os.getcwd(), "reuters21578")
    last_index = 1
    for reutersFile in os.listdir(infile_directory):
        if reutersFile != ".DS_Store":
            with open(os.path.join(infile_directory, reutersFile), 'rb') as infile:
                content = infile.read()

            print("Processing " + reutersFile + ":")

            soup = BeautifulSoup(content, 'html.parser')

            documents = soup.find_all("reuters")

            for docId, doc in enumerate(documents, last_index):
                title = doc.find("title").text if doc.find("title") != None else ""
                body = doc.find("body").text if doc.find("body") != None else ""
                topics = doc.find("topics").find_all("d")[0].text if doc.find("topics").find("d") != None else ""
                data["documents"].append({
                    "docId" : docId,
                    "title" : title.strip(),
                    "body" : body.strip(),
                    "topics" : topics.strip()
                })
            last_index = docId + 1 # to maintain docID's when switching to a new doc
        
    with open('reuters_data.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
    preprocess_reuters_corpus()
