# To do an inital load of the db
from preprocessing import preprocess_courses_corpus, preprocess_reuters_corpus
from dictionary_builder import build_courses_dict_with_json_file, build_reuters_dict_with_json_file
from inverted_index_builder import build_courses_inverted_index, build_reuters_inverted_index
from db_operations import insert_courses_corpus_into_db, insert_courses_dictionary_into_db, insert_courses_inverted_index_into_db, insert_reuters_corpus_into_db, insert_reuters_dictionary_into_db, insert_reuters_inverted_index_into_db

def process_and_load_courses():
    preprocess_courses_corpus()
    insert_courses_corpus_into_db("courses_data.json")
    build_courses_dict_with_json_file("courses_data.json")
    insert_courses_dictionary_into_db("courses_dictionary.json")
    build_courses_inverted_index("courses_dictionary.json")
    insert_courses_inverted_index_into_db("courses_inverted_index.json")

def process_and_load_reuters():
    preprocess_reuters_corpus()
    insert_reuters_corpus_into_db("reuters_data.json")
    build_reuters_dict_with_json_file("reuters_data.json")
    insert_reuters_dictionary_into_db("reuters_dictionary.json")
    build_reuters_inverted_index("reuters_dictionary.json")
    insert_reuters_inverted_index_into_db("reuters_inverted_index.json")

if __name__ == "__main__":
    process_and_load_courses()