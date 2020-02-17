# import math

# from db_operations import retrieve_courses_all_terms_and_doc_freqs, retrieve_courses_all_document_ids

# def build_weighted_index():
#     # use inverted matrix --> index of all term/document weights
#     # total docs = td
#     # idf = td/doc_freq
#     # tf = tf from postings table or 0
#     total_document_count = retrieve_courses_all_documents_count()
#     idf = {}
#     tf = {}
#     tf['term_freq'] = []
#     for term in retrieve_courses_all_terms_and_doc_freqs():
#         idf[term[0]] = math.log10(total_document_count / term[1])
#         for doc_id in retrieve_courses_all_document_ids():
#             tf['term_freq'].append({
#                 'term' : term

#             })
    