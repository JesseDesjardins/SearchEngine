import json

def build_courses_inverted_index(json_file):
    """ Builds an inverted index using standard term frequency (# of occurences of term in doc) """
    with open(json_file) as infile:
        dictionary = json.load(infile)

    print('Building inverted index...')
    sorted_dictionary = sorted(dictionary['words'], key=lambda k: k['word'])
    inverted_index = {}
    inverted_index['index'] = []

    for word in sorted_dictionary:
        if inverted_index['index'] == []: # in index is empty (inital state)
            inverted_index['index'].append({
                'term' : word['word'],
                'doc_freq' : 1,
                'postings_list' : [[word['docid'], 1]]
            })
        elif inverted_index['index'][-1].get('term') == word['word']: # if the word matches the last term in the index
            if inverted_index['index'][-1]['postings_list'][-1][0] != word['docid']: # if the docid of the word is not the same as the last docid in the index
                inverted_index['index'][-1]['doc_freq'] = inverted_index['index'][-1]['doc_freq'] + 1
                inverted_index['index'][-1]['postings_list'].append([word['docid'], 1])
            else: # if the docid of the word is the same as the last docid in the index
                inverted_index['index'][-1]['postings_list'][-1][1] = inverted_index['index'][-1]['postings_list'][-1][1] + 1 # increment term frequency
        else:
            inverted_index['index'].append({
                'term' : word['word'],
                'doc_freq' : 1,
                'postings_list' : [[word['docid'], 1]]
            })
    
    with open('courses_inverted_index.json', 'w') as outfile:
        json.dump(inverted_index, outfile)
    print('Inverted index complete!')

def build_reuters_inverted_index(json_file):
    """ Builds an inverted index using standard term frequency (# of occurences of term in doc) """
    with open(json_file) as infile:
        dictionary = json.load(infile)

    print('Building inverted index...')
    sorted_dictionary = sorted(dictionary['words'], key=lambda k: k['word'])
    inverted_index = {}
    inverted_index['index'] = []

    for word in sorted_dictionary:
        if inverted_index['index'] == []: # in index is empty (inital state)
            inverted_index['index'].append({
                'term' : word['word'],
                'doc_freq' : 1,
                'postings_list' : [[word['docid'], 1]]
            })
        elif inverted_index['index'][-1].get('term') == word['word']: # if the word matches the last term in the index
            if inverted_index['index'][-1]['postings_list'][-1][0] != word['docid']: # if the docid of the word is not the same as the last docid in the index
                inverted_index['index'][-1]['doc_freq'] = inverted_index['index'][-1]['doc_freq'] + 1
                inverted_index['index'][-1]['postings_list'].append([word['docid'], 1])
            else: # if the docid of the word is the same as the last docid in the index
                inverted_index['index'][-1]['postings_list'][-1][1] = inverted_index['index'][-1]['postings_list'][-1][1] + 1 # increment term frequency
        else:
            inverted_index['index'].append({
                'term' : word['word'],
                'doc_freq' : 1,
                'postings_list' : [[word['docid'], 1]]
            })
    
    with open('reuters_inverted_index.json', 'w') as outfile:
        json.dump(inverted_index, outfile)
    print('Inverted index complete!')

if __name__ == "__main__":
    build_reuters_inverted_index('reuters_dictionary.json')
