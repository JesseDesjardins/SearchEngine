import json

def add_doc(docId, corpus):
    """ Adds the document to the relevant corpuses' relevant documents file """
    if corpus=="courses":
        with open("courses_relevance_feedback.json", 'r') as infile:
            docs = json.load(infile)
        if docId not in docs["docs"] : 
            docs["docs"].append(docId)
            with open('courses_relevance_feedback.json', 'w') as outfile:
                json.dump(docs, outfile)
    elif corpus=="reuters":
        with open("reuters_relevance_feedback.json", 'r') as infile:
            docs = json.load(infile)
        if docId not in docs["docs"] : 
            docs["docs"].append(docId)
            with open('reuters_relevance_feedback.json', 'w') as outfile:
                json.dump(docs, outfile)
    else:
        None

def remove_doc(docId, corpus):
    """ Removes the document from the relevant corpuses' relevant documents file """
    if corpus=="courses":
        with open("courses_relevance_feedback.json", 'r') as infile:
            docs = json.load(infile)
        if docId in docs["docs"] : 
            docs["docs"].remove(docId)
            with open('courses_relevance_feedback.json', 'w') as outfile:
                json.dump(docs, outfile)
    elif corpus=="reuters":
        with open("reuters_relevance_feedback.json", 'r') as infile:
            docs = json.load(infile)
        if docId in docs["docs"] : 
            docs["docs"].remove(docId)
            with open('reutere_relevance_feedback.json', 'w') as outfile:
                json.dump(docs, outfile)
    else:
        None

if __name__ == "__main__":
    add_doc(2, "courses")