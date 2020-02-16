import psycopg2
import json
from config import config

def get_connection():
    """ Returns a connection to the database """
    conn = None
    try:
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**config())
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn

def get_db_version():
    """ Used as a donnection test; prints DB version """
    # create a cursor
    conn = get_connection()
    cur = conn.cursor()
    # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)
    
    # close the communication with the PostgreSQL
    cur.close()

def insert_courses_corpus_into_db(json_file):
    """ Inserts the courses corpus JSON file into the DB """
    connection = get_connection()
    cursor = connection.cursor()

    insert_command = 'INSERT INTO corpus_u_of_o_courses.documents(docid, title, description) values '
    with open(json_file) as file:
        data = json.load(file)
        for doc in data['documents']:
            doc_id = doc['docId']
            title = doc['title'] if doc['title'] != "" else None
            description = doc['description'].replace("'", "''") if doc['description'] != "" else None
            insert_command = insert_command + """({0}, '{1}', '{2}'),""".format(doc_id, title, description)
        insert_command = insert_command[:-1] + ';' # Removes trailing comma
    
    try:
        print('Inserting courses into db...')
        cursor.execute(insert_command)
        cursor.close()
        connection.commit()
        print('Success!')
    except(Exception) as error:
        print(error)

def insert_courses_dictionary_into_db(json_file):
    """ Inserts the courses dictionary JSON file into the DB """
    connection = get_connection()
    cursor = connection.cursor()

    insert_command = 'INSERT INTO corpus_u_of_o_courses.dictionary(word, docid) values '
    with open(json_file) as infile:
        data = json.load(infile)
        for doc in data['words']:
            insert_command = insert_command + """('{0}', {1}),""".format(doc['word'], doc['docid'])
        insert_command = insert_command[:-1] + ';' # Removes trailing comma
    
    try:
        print('Inserting courses dictionary into db...')
        cursor.execute(insert_command)
        cursor.close()
        connection.commit()
        print('Success!')
    except(Exception) as error:
        print(error)

def insert_courses_inverted_index_into_db(json_file):
    """ Inserts the courses inverted index JSON file into the DB """
    connection = get_connection()
    cursor = connection.cursor()

    insert_postings_command = 'INSERT INTO corpus_u_of_o_courses.inverted_matrix_postings(posting_id, doc_id, term_freq) values '
    insert_terms_command = 'INSERT INTO corpus_u_of_o_courses.inverted_matrix_terms(term_id, term, doc_freq) values '
    insert_foreign_keys_command = 'INSERT INTO corpus_u_of_o_courses.inverted_matrix_terms_postings(term_id, posting_id) values '
    postings_id = 0
    term_id = 0
    data = {}
    with open(json_file) as infile:
        data = json.load(infile)
    for term in data['index']:
        term_id += 1
        insert_terms_command = insert_terms_command + "({0}, '{1}', {2}),".format(term_id, term['term'], term['doc_freq'])
        term_postings = []
        for posting in term['postings_list']:
            postings_id += 1
            insert_postings_command = insert_postings_command + "({0}, {1}, {2}),".format(postings_id, posting[0], posting[1])
            term_postings.append(postings_id)
        for posting_id in term_postings:
            insert_foreign_keys_command = insert_foreign_keys_command + "({0}, {1}),".format(term_id, posting_id)
    insert_terms_command = insert_terms_command[:-1] + ';'
    insert_postings_command = insert_postings_command[:-1] + ';'
    insert_foreign_keys_command = insert_foreign_keys_command[:-1] + ';'
        
    try:
        print('Inserting inverted index data into db...')
        cursor.execute(insert_terms_command)
        cursor.execute(insert_postings_command)
        cursor.execute(insert_foreign_keys_command)
        cursor.close()
        connection.commit()
        print('Success!')
    except(Exception) as error:
        print(error)

def retrieve_courses_documents(doc_ids):
    """ Retrieves the course documents associated with the given list of IDs """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT docid, title, description FROM corpus_u_of_o_courses.documents WHERE docid IN ('
    for id in doc_ids:
        select_command = select_command + '{},'.format(id)
    select_command = select_command[:-1] + ');'
    print(select_command)

    try:
        cursor.execute(select_command)
        docs = cursor.fetchall()
    except(Exception) as error:
        docs = None
        print(error)
    
    return docs

def retrieve_courses_documents_not(doc_ids):
    """ Retrieves all the course documents not associated with the given list of IDs """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT docid, title, description FROM corpus_u_of_o_courses.documents WHERE docid NOT IN ('
    for id in doc_ids:
        select_command = select_command + '{},'.format(id)
    select_command = select_command[:-1] + ');'

    try:
        cursor.execute(select_command)
        docs = cursor.fetchall()
        cursor.close()
    except(Exception) as error:
        docs = None
        print(error)
    
    return docs

def retrieve_courses_doc_ids_from_term(term):
    """ Returns all doc_ids for docs where term is present """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = """SELECT p.doc_id from corpus_u_of_o_courses.inverted_matrix_terms t, 
                                            corpus_u_of_o_courses.inverted_matrix_postings p,
                                            corpus_u_of_o_courses.inverted_matrix_terms_postings tp
                        WHERE t.term = '{0}' AND tp.term_id = t.term_id AND p.posting_id = tp.posting_id;""".format(term)
    try:
        cursor.execute(select_command)
        doc_ids = cursor.fetchall()
        cursor.close()
    except(Exception) as error:
        doc_ids = None
        print(error)
    
    return [doc_id[0] for doc_id in doc_ids] # doc_ids is list of tuples of 1 int; simplyfy to a list of ints

def retrieve_courses_doc_ids_not_from_term(term):
    """ Returns all doc_ids for docs where term is not present """
    doc_ids = retrieve_courses_doc_ids_from_term(term)

    connection = get_connection()
    cursor = connection.cursor()

    select_command = "SELECT docid from corpus_u_of_o_courses.documents WHERE docid NOT IN ("
    for id in doc_ids:
        select_command = select_command + '{},'.format(id)
    select_command = select_command[:-1] + ');'

    try:
        cursor.execute(select_command)
        doc_ids = cursor.fetchall()
        cursor.close()
    except(Exception) as error:
        doc_ids = None
        print(error)
    
    return [doc_id[0] for doc_id in doc_ids] # doc_ids is list of tuples of 1 int; simplyfy to a list of ints

def retrieve_courses_doc_ids_not_from_set(doc_ids):
    """ Returns all doc_ids for docs that aren't associated with doc_ids """

    connection = get_connection()
    cursor = connection.cursor()

    select_command = "SELECT docid from corpus_u_of_o_courses.documents WHERE docid NOT IN ("
    for id in doc_ids:
        select_command = select_command + '{},'.format(id)
    select_command = select_command[:-1] + ');'

    try:
        cursor.execute(select_command)
        doc_ids = cursor.fetchall()
        cursor.close()
    except(Exception) as error:
        doc_ids = None
        print(error)
    
    return [doc_id[0] for doc_id in doc_ids] # doc_ids is list of tuples of 1 int; simplyfy to a list of ints

if __name__ == "__main__":
    get_db_version()
    print(retrieve_courses_doc_ids_not_from_term('&'))
