# Import libraries
import json
import time

# Import local files
from word_processing import case_fold, normalize, tokenize, remove_stopwords, stem, lemmatize


def build_courses_dict_with_json_file(filename, useStemmer=True, useLemmatization=False):
    """ Builds a dictionary of terms out of the given json file

    Parses a json file with specific format {{docId}, {title}, {description}}
    and creates a dict populated with every term from the json file. It
    will also apply certain word processing modules during the dict creation
    process. It will then write a json file generated from that dict.

    Parameters
    ----------
    filename: str
        Name of the json file
    useStemmer: bool
        Optional flag to use stemming
    useLemmatization: bool
        Optional flag to use lemmatization
    """

    dictionary = {}
    dictionary['words'] = []

    with open(filename) as json_file:
        documents = json.load(json_file)
        
    print('Building dictionary...')
    for doc in documents['documents']:
        docId = doc['docId']

        # Add title tokens
        title_tokens = tokenize(doc['title'])
        title_tokens = case_fold(title_tokens)
        title_tokens = remove_stopwords(title_tokens)
        title_tokens = normalize(title_tokens)
        if useStemmer:
            title_tokens = stem(title_tokens)
        if useLemmatization:
            title_tokens = lemmatize(title_tokens)

        for token in title_tokens:
            dictionary['words'].append({
                'word' : token,
                'docid' : docId
            })
        
        # Add description tokens
        description_tokens = tokenize(doc['description'])
        description_tokens = case_fold(description_tokens)
        description_tokens = remove_stopwords(description_tokens)
        description_tokens = normalize(description_tokens)
        if useStemmer:
            description_tokens = stem(description_tokens)
        if useLemmatization:
            description_tokens = lemmatize(description_tokens)

        for token in description_tokens:
            dictionary['words'].append({
                'word' : token,
                'docid' : docId
            })
            
    with open('courses_dictionary.json', 'w') as outfile:
        json.dump(dictionary, outfile)
    print('Dictionary built!')

def build_reuters_dict_with_json_file(filename, useStemmer=True, useLemmatization=False):
    """ Builds a dictionary of terms out of the given json file

    Parses a json file with specific format {{docId}, {title}, {body}, {topics}}
    and creates a dict populated with every term from the json file. It
    will also apply certain word processing modules during the dict creation
    process. It will then write a json file generated from that dict.

    Parameters
    ----------
    filename: str
        Name of the json file
    useStemmer: bool
        Optional flag to use stemming
    useLemmatization: bool
        Optional flag to use lemmatization
    """

    dictionary = {}
    dictionary['words'] = []

    with open(filename) as json_file:
        documents = json.load(json_file)
        
    print('Building dictionary...')
    start_time = time.time()
    for doc in documents['documents']:
        docId = doc['docId']

        # Add title tokens
        title_tokens = tokenize(doc['title'])
        title_tokens = case_fold(title_tokens)
        title_tokens = remove_stopwords(title_tokens)
        title_tokens = normalize(title_tokens)
        if useStemmer:
            title_tokens = stem(title_tokens)
        if useLemmatization:
            title_tokens = lemmatize(title_tokens)

        for token in title_tokens:
            dictionary['words'].append({
                'word' : token,
                'docid' : docId
            })
        
        # Add body tokens
        body_tokens = tokenize(doc['body'])
        body_tokens = case_fold(body_tokens)
        body_tokens = remove_stopwords(body_tokens)
        body_tokens = normalize(body_tokens)
        if useStemmer:
            body_tokens = stem(body_tokens)
        if useLemmatization:
            body_tokens = lemmatize(body_tokens)

        for token in body_tokens:
            dictionary['words'].append({
                'word' : token,
                'docid' : docId
            })
        
        # Add topics tokens
        topics_tokens = tokenize(doc['topics'])
        topics_tokens = case_fold(topics_tokens)
        topics_tokens = remove_stopwords(topics_tokens)
        topics_tokens = normalize(topics_tokens)
        if useStemmer:
            topics_tokens = stem(topics_tokens)
        if useLemmatization:
            topics_tokens = lemmatize(topics_tokens)

        for token in topics_tokens:
            dictionary['words'].append({
                'word' : token,
                'docid' : docId
            })
    print("Dictionary Built in %s seconds" % (time.time() - start_time))
    print("Dumping dictionary to json file...")
    with open('reuters_dictionary.json', 'w') as outfile:
        json.dump(dictionary, outfile)
    print('Dictionary built!')

if __name__ == "__main__":
    build_reuters_dict_with_json_file("reuters_data.json")