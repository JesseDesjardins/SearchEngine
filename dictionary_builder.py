# Import libraries
import json

# Import local files
from word_processing_modules import case_fold, normalize, tokenize, remove_stopwords, stem, lemmatize


def build_dict_with_json_file(filename, useStemmer=False, useLemmatization=False):
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

if __name__ == "__main__":
    build_dict_with_json_file("courses_data.json")