import psycopg2
import json
from config import config

# Courses functions

def get_connection():
    """ Returns a connection to the database """
    conn = None
    try:
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**config())
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    if conn != None : print("Connected!")
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
    """ Retrieves the course documents associated with the given list of IDs 
    
    Return
    ------
    list of tuple
        A list of tuples of docid, title and description
    """

    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT docid, title, description FROM corpus_u_of_o_courses.documents WHERE docid IN ('
    for id in doc_ids:
        select_command = select_command + '{},'.format(id)
    if select_command[-1] == ',':
        select_command = select_command[:-1] + ');'
    else:
        select_command = select_command + ');'

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

def retrieve_courses_doc_ids_from_terms(terms):
    """ Returns all doc_ids for docs where any terms in the list are present """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = """SELECT p.doc_id from corpus_u_of_o_courses.inverted_matrix_terms t, 
                                            corpus_u_of_o_courses.inverted_matrix_postings p,
                                            corpus_u_of_o_courses.inverted_matrix_terms_postings tp
                        WHERE t.term in ("""
    for term in terms:
        select_command = select_command + "'{}',".format(term)
    if select_command[-1] == ',':
        select_command = select_command[:-1] + ') AND tp.term_id = t.term_id AND p.posting_id = tp.posting_id;'
    else:
        select_command = select_command + ') AND tp.term_id = t.term_id AND p.posting_id = tp.posting_id;'

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
    
    return [doc_id[0] for doc_id in doc_ids] # doc_ids is list of tuples of 1 int; simplify to a list of ints

def retrieve_courses_all_terms():
    """ Retrieves a list of all terms from the inverted matrix index """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT term FROM corpus_u_of_o_courses.inverted_matrix_terms;'

    try:
        cursor.execute(select_command)
        terms = cursor.fetchall()
    except(Exception) as error:
        terms = None
        print(error)
    
    return [term[0] for term in terms] # terms is list of tuples of 1 string; simplify to a list of strings

def retrieve_courses_all_terms_and_doc_freqs():
    """ Retrieves a list of tuples all terms and their doccument frequencies from the inverted matrix index """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT term, doc_freq FROM corpus_u_of_o_courses.inverted_matrix_terms;'

    try:
        cursor.execute(select_command)
        pairs = cursor.fetchall()
    except(Exception) as error:
        pairs = None
        print(error)
    
    return pairs

def retrieve_courses_all_documents_count():
    """ Retrieves a count of all documents in the corpus """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT COUNT(*) FROM corpus_u_of_o_courses.documents;'

    try:
        cursor.execute(select_command)
        count = cursor.fetchone()
    except(Exception) as error:
        count = None
        print(error)
    
    return count[0]

def retrieve_courses_all_terms_count():
    """ Retrieves a count of all unique terms in the corpus """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT COUNT(*) FROM corpus_u_of_o_courses.inverted_matrix_terms;'

    try:
        cursor.execute(select_command)
        count = cursor.fetchone()
    except(Exception) as error:
        count = None
        print(error)
    
    return count[0]

def retrieve_courses_all_document_ids():
    """ Retrieves all document ids in the corpus """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT docid FROM corpus_u_of_o_courses.documents;'

    try:
        cursor.execute(select_command)
        doc_ids = cursor.fetchall()
    except(Exception) as error:
        doc_ids = None
        print(error)
    
    return [doc_id[0] for doc_id in doc_ids]

# Reuters Functions

def insert_reuters_corpus_into_db(json_file):
    """ Inserts the reuters documents corpus JSON file into the DB """
    connection = get_connection()
    cursor = connection.cursor()

    insert_command = 'INSERT INTO corpus_reuters.documents(docid, title, body, topics) values '
    with open(json_file) as file:
        data = json.load(file)
        for doc in data['documents']:
            doc_id = doc['docId']
            title = doc['title'].replace("'", "''") if doc['title'] != "" else None
            body = doc['body'].replace("'", "''") if doc['body'] != "" else None
            topics = doc['topics'].replace("'", "''") if doc['topics'] != "" else None
            insert_command = insert_command + """({0}, '{1}', '{2}', '{3}'),""".format(doc_id, title, body, topics)
        insert_command = insert_command[:-1] + ';' # Removes trailing comma
    
    try:
        print('Inserting documents into db...')
        cursor.execute(insert_command)
        cursor.close()
        connection.commit()
        print('Success!')
    except(Exception) as error:
        print(error)

def insert_reuters_dictionary_into_db(json_file):
    """ Inserts the reuters dictionary JSON file into the DB """
    connection = get_connection()
    cursor = connection.cursor()

    insert_command = 'INSERT INTO corpus_reuters.dictionary(word, docid) values '
    with open(json_file) as infile:
        data = json.load(infile)
        for doc in data['words']:
            insert_command = insert_command + """('{0}', {1}),""".format(doc['word'], doc['docid'])
        insert_command = insert_command[:-1] + ';' # Removes trailing comma
    
    try:
        print('Inserting reuters dictionary into db...')
        cursor.execute(insert_command)
        cursor.close()
        connection.commit()
        print('Success!')
    except(Exception) as error:
        print(error)

def insert_reuters_inverted_index_into_db(json_file):
    """ Inserts the reuters inverted index JSON file into the DB """
    connection = get_connection()
    cursor = connection.cursor()

    print("Generating insert query...")
    insert_index_command = 'INSERT INTO corpus_reuters.inverted_matrix_terms_postings(term_id, term, doc_freq, doc_id_term_freq_tuple) values '
    postings_id = 0
    term_id = 0
    data = {}
    with open(json_file) as infile:
        data = json.load(infile)
    for term in data['index']:
        term_id += 1
        insert_index_command = insert_index_command + "({0}, '{1}', {2}, '{{".format(term_id, term['term'], term['doc_freq'])
        term_postings = []
        for posting in term['postings_list']:
            insert_index_command = insert_index_command + """{{"{0}", "{1}"}},""".format(posting[0], posting[1])
        insert_index_command = insert_index_command[:-1] + "}')," # closes array insert
    insert_index_command = insert_index_command[:-1] + ";" # removes trailing comma
        
    try:
        print('Inserting inverted index data into db...')
        cursor.execute(insert_index_command)
        cursor.close()
        connection.commit()
        print('Success!')
    except(Exception) as error:
        print(error)

def retrieve_reuters_documents(doc_ids):
    """ Retrieves the reuter documents associated with the given list of IDs 
    
    Return
    ------
    list of tuple
        A list of tuples of docid, title, body and topics
    """

    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT docid, title, body, topics FROM corpus_reuters.documents WHERE docid IN ('
    for id in doc_ids:
        select_command = select_command + '{},'.format(id)
    if select_command[-1] == ',':
        select_command = select_command[:-1] + ');'
    else:
        select_command = select_command + ');'
    try:
        cursor.execute(select_command)
        docs = cursor.fetchall()
    except(Exception) as error:
        docs = None
        print(error)
    
    return docs

def retrieve_reuters_all_terms():
    """ Retrieves a list of all terms from the inverted matrix index """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT term FROM corpus_reuters.inverted_matrix_terms;'

    try:
        cursor.execute(select_command)
        terms = cursor.fetchall()
    except(Exception) as error:
        terms = None
        print(error)
    
    return [term[0] for term in terms] # terms is list of tuples of 1 string; simplify to a list of strings

def retrieve_reuters_doc_ids_from_terms(terms):
    """ Returns all doc_ids for docs where any terms in the list are present """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = "SELECT doc_id_term_freq_tuple from corpus_reuters.inverted_matrix_terms_postings WHERE term in ("
    for term in terms:
        select_command = select_command + "'{}',".format(term)
    if select_command[-1] == ',':
        select_command = select_command[:-1] + ');'
    else:
        select_command = select_command + ');'
    try:
        cursor.execute(select_command)
        doc_id_term_freq_tuples = cursor.fetchall()
        cursor.close()
    except(Exception) as error:
        doc_id_term_freq_tuples = None
        print(error)
    doc_ids = []
    for tpl in doc_id_term_freq_tuples:
        for inner_tpl in tpl:
            for more_inner_tpl in inner_tpl:
                doc_ids.append(more_inner_tpl[0])
    return doc_ids

def retrieve_reuters_doc_ids_not_from_set(doc_ids):
    """ Returns all doc_ids for docs that aren't associated with doc_ids """

    connection = get_connection()
    cursor = connection.cursor()

    select_command = "SELECT docid from corpus_reuters.documents WHERE docid NOT IN ("
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
    
    return [doc_id[0] for doc_id in doc_ids] # doc_ids is list of tuples of 1 int; simplify to a list of ints

def retrieve_reuters_all_documents_count():
    """ Retrieves a count of all documents in the corpus """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT COUNT(*) FROM corpus_reuters.documents;'

    try:
        cursor.execute(select_command)
        count = cursor.fetchone()
    except(Exception) as error:
        count = None
        print(error)
    
    return count[0]

def retrieve_reuters_all_terms_count():
    """ Retrieves a count of all unique terms in the corpus """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT COUNT(*) FROM corpus_reuters.inverted_matrix_terms_postings;'

    try:
        cursor.execute(select_command)
        count = cursor.fetchone()
    except(Exception) as error:
        count = None
        print(error)
    
    return count[0]

def retrieve_reuters_all_terms_and_doc_freqs():
    """ Retrieves a list of tuples all terms and their doccument frequencies from the inverted matrix index """
    connection = get_connection()
    cursor = connection.cursor()

    select_command = 'SELECT term, doc_freq FROM corpus_reuters.inverted_matrix_terms_postings;'

    try:
        cursor.execute(select_command)
        pairs = cursor.fetchall()
    except(Exception) as error:
        pairs = None
        print(error)
    
    return pairs

if __name__ == "__main__":
    get_db_version()
    # insert_reuters_dictionary_into_db("reuters_dictionary.json")
    # insert_reuters_inverted_index_into_db("reuters_inverted_index.json")
    print(retrieve_reuters_documents([133, 1]))
