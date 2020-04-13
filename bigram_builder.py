from nltk import bigrams
from collections import defaultdict
import json
import time

from word_processing import remove_stopwords, case_fold, tokenize, normalize

def build_bigram_lm():
    """ Creates a list of bigrams from both corpuses """
    bigram_lm = defaultdict(lambda: defaultdict(int))
    with open("courses_data.json") as courses, open("reuters_data.json") as reuters:
        courses_docs = json.load(courses)
        reuters_docs = json.load(reuters)
    
    print("Generating bigram language model...")
    start_time = time.time()
    # Run through the courses
    for doc in courses_docs["documents"]:
        main_body = remove_stopwords(normalize(case_fold(tokenize(doc['description']))))

        for word_1, word_2 in bigrams(main_body):
            bigram_lm[word_1][word_2] += 1

        for word_1 in bigram_lm:
            count = float(sum(bigram_lm[word_1].values()))
            for word_2 in bigram_lm[word_1]:
                    bigram_lm[word_1][word_2] /= count
    
    # Run through the Reuters documents
    for doc in reuters_docs["documents"]:
        main_body = remove_stopwords(normalize(case_fold(tokenize(doc['body']))))

        for word_1, word_2 in bigrams(main_body):
            bigram_lm[word_1][word_2] += 1

        for word_1 in bigram_lm:
            count = float(sum(bigram_lm[word_1].values()))
            for word_2 in bigram_lm[word_1]:
                    bigram_lm[word_1][word_2] /= count

    print("Bigram language model built in %s seconds" % (time.time() - start_time))
    print("Dumping bigram language model to json file...")
    with open('bigram_language_model.json', 'w') as outfile:
            json.dump(bigram_lm, outfile)
    print("Bigram language model built!")
            
if __name__ == "__main__":
    build_bigram_lm()