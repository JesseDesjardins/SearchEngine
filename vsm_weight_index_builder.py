import math
import json

from db_operations import retrieve_courses_all_terms_and_doc_freqs, retrieve_courses_all_document_ids, retrieve_courses_all_documents_count, retrieve_courses_all_terms_count

def build_weighted_index():
    """ Builds a weighted index matrix using terms (sorted alphabetically) as columns and documents
    (sorted in increasing order) as rows """
    # use inverted matrix --> index of all term/document weights
    # total number of docs = N
    # idf = N/doc_freq
    # tf = tf from postings table or 0

    total_document_count = retrieve_courses_all_documents_count()
    total_term_count = retrieve_courses_all_terms_count()
    terms_and_freqs = retrieve_courses_all_terms_and_doc_freqs()
    # Create idf scores list
    idf = build_idf_values(total_term_count, terms_and_freqs, total_document_count)
    # Create tf-idf matrix
    tf = build_tf_idf_matrix(total_term_count, total_document_count, idf)
    # Multiply tf scores by idf values
    for doc in range(len(tf)):
        for term in range(len(tf[doc])):
            tf[doc][term] *= idf[term]
    return tf

def build_idf_values(total_term_count, term_and_freqs, total_document_count):
    """ returns a list of terms and their respective idf values """
    return {term: math.log10(total_document_count / freq) for term, freq in term_and_freqs}

def build_tf_idf_matrix(num_of_terms, num_of_docs, idf):
    """ returns tf-idf matrix represented as a dictionary of dictionaries. 
    The outer dictionary will be indexed on the documents and the inner 
    dictionary will be indexed on the terms. 
    
    Uses the raw term frequency. """
    with open("courses_inverted_index.json") as infile:
        inverted_index = json.load(infile)
    
    # return {doc + 1: {term["term"]: freq * idf[term["term"]] if doc + 1 == docId else 0 
    # for term in inverted_index["index"] 
    # for docId, freq in term["postings_list"]} 
    # for doc in range(num_of_docs)}

    # TODO: Incomplete
    tf_idf = {}
    for doc in range(num_of_docs):
        tf_idf[doc + 1] = {}
        for term in inverted_index["index"]:
            for docId, freq in term["postings_list"]:
                if doc + 1 == docId:
                    new_freq = freq
                else:
                    new_freq = 0
                tf_idf[doc + 1][term["term"]] = new_freq * idf[term["term"]]
    return tf_idf

    
if __name__ == "__main__":
    # print(build_idf_values(retrieve_courses_all_terms_count(), retrieve_courses_all_terms_and_doc_freqs(), retrieve_courses_all_documents_count()))
    # print(build_weighted_index())
    idf = build_idf_values(retrieve_courses_all_terms_count(), retrieve_courses_all_terms_and_doc_freqs(), retrieve_courses_all_documents_count())
    print(idf["knowledge"])
    tf_idf_mat = build_tf_idf_matrix(retrieve_courses_all_terms_count(), retrieve_courses_all_documents_count(), idf)
    # x = [term + ' ,' + value for term, value in tf_idf_mat[3] if value !=0]
    for key, value in tf_idf_mat[1].items():
        # print(key, value) if key == "knowledge" else None
        print(key, value) if value != 0 else None
    print(tf_idf_mat[1])