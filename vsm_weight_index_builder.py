import math
import json
from collections import defaultdict

from db_operations import retrieve_courses_all_terms_and_doc_freqs, retrieve_courses_all_document_ids, retrieve_courses_all_documents_count, retrieve_courses_all_terms_count, retrieve_reuters_all_documents_count, retrieve_reuters_all_terms_count, retrieve_reuters_all_terms_and_doc_freqs

def build_weighted_index():
    """ Builds a weighted index matrix using terms (sorted alphabetically) as columns and documents
    (sorted in increasing order) as rows """

    total_document_count = retrieve_courses_all_documents_count()
    total_term_count = retrieve_courses_all_terms_count()
    terms_and_freqs = retrieve_courses_all_terms_and_doc_freqs()

    total_document_count_reuters = retrieve_reuters_all_documents_count()
    total_term_count_reuters = retrieve_reuters_all_terms_count()
    terms_and_freqs_reuters = retrieve_reuters_all_terms_and_doc_freqs()

    idf_values = {}
    idf_values["values"] = build_idf_values(total_term_count, terms_and_freqs, total_document_count)
    weighted_index = {}
    weighted_index["index"] = build_tf_idf_matrix(idf_values["values"], "courses")

    with open("courses_idf_values.json", 'w') as outfile:
        json.dump(idf_values, outfile)

    with open("courses_weighted_index.json", 'w') as outfile:
        json.dump(weighted_index, outfile)

    idf_values = {}
    idf_values["values"] = build_idf_values(total_term_count_reuters, terms_and_freqs_reuters, total_document_count_reuters)
    weighted_index = {}
    weighted_index["index"] = build_tf_idf_matrix(idf_values["values"], "reuters")

    with open("reuters_idf_values.json", 'w') as outfile:
        json.dump(idf_values, outfile)

    with open("reuters_weighted_index.json", 'w') as outfile:
        json.dump(weighted_index, outfile)
    return weighted_index

def build_idf_values(total_term_count, term_and_freqs, total_document_count):
    """ returns a dict of terms and their respective idf values """
    return {term: math.log10(total_document_count / freq) for term, freq in term_and_freqs}

def build_tf_idf_matrix(idf, collection):
    """ returns tf-idf matrix represented as a dictionary of dictionaries. 
    The outer dictionary will be indexed on the terms and the inner 
    dictionary will be indexed on the documents. 
    
    Uses the raw term frequency. """

    inverted_index = {}
    if collection == "courses":
        with open("courses_inverted_index.json") as infile:
            inverted_index = json.load(infile)
    elif collection == "reuters":
        with open("reuters_inverted_index.json") as infile:
            inverted_index = json.load(infile)

    tf_idf = defaultdict(lambda: defaultdict(int)) # essentailly 2D dictionarry with a default value of 0 for any missing keys
    for term in inverted_index["index"]:
        term_row = defaultdict(int) # Will hold all docs and values, in reference to one term
        for doc in term["postings_list"]:
            term_row[doc[0]] = doc[1] * idf[term["term"]] # doc[0] is docId, doc[1] is raw term frequency
        tf_idf[term["term"]] = term_row

    return tf_idf

def get_doc_term_scores(tf_idf, docId):
    """ Returns a dict of all terms present in a given doc and their respective tf-idf scores """
    doc_scores = defaultdict(int)
    for term in tf_idf.keys():
        for doc_id in tf_idf[term]:
            if doc_id == docId : doc_scores[term] = tf_idf[term][doc_id]
    return doc_scores

    
if __name__ == "__main__":
    build_weighted_index()
    