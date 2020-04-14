from collections import defaultdict
import operator
import json
import math

from db_operations import retrieve_courses_all_documents_count, retrieve_reuters_all_documents_count
from vsm_weight_index_builder import get_doc_term_scores

def execute_vsm_query(query, collection):
    """ return docId's relevant to the the query """
    if collection == "courses":
        with open("courses_weighted_index.json", 'r') as json_file:
            tf_idf = json.load(json_file)

    elif collection == "reuters":
        with open("reuters_weighted_index.json", 'r') as json_file:
            tf_idf = json.load(json_file)

    query_tokens = query.split(' ')
    tokens = defaultdict(int)
    for token in query_tokens:
        tokens[token] += 1

    # calculate tf-idf values of query
    max_freq = max(tokens.items(), key=operator.itemgetter(1))[1]
    tf_idf_query = defaultdict(int)

    idf_values = {}
    if collection == "courses":
        with open("courses_idf_values.json", 'r') as json_file:
            idf_values = json.load(json_file)
    elif collection == "reuters":
        with open("reuters_idf_values.json", 'r') as json_file:
            idf_values = json.load(json_file)

    for token in tokens:
        tf_idf_query[token] = (tokens[token] / max_freq) * idf_values["values"][token]

    # Get all doc lengths
    document_values = {}
    length = 0
    if collection == "courses":
        length = retrieve_courses_all_documents_count()
    elif collection == "reuters":
        length = retrieve_reuters_all_documents_count()
    for i in range(length):
        document_values[i] = get_doc_term_scores(tf_idf["index"], str(i+1))
    
    document_lengths = {}
    for doc in document_values:
        document_lengths[doc] = math.sqrt(sum(x**2 for x in document_values[doc].values()))
        
    # Get query length
    query_length = math.sqrt(sum(x**2 for x in tf_idf_query.values()))

    # Doc Cosine Simularities
    document_cos_sims = {}
    for doc in document_values:
        x = sum(tf_idf_query[term] * document_values[doc][term] for term in tf_idf["index"])
        document_cos_sims[doc] = x / (document_lengths[doc]*query_length) if (document_lengths[doc]*query_length) != 0 else 0

    # Select top 15 documents
    return dict(sorted(document_cos_sims.items(), key = operator.itemgetter(1), reverse = True)[:15])

if __name__ == "__main__":
    print(execute_vsm_query("class student", "reuters"))