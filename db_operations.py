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

def make_new_table(sql_command):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(sql_command)
        cursor.close()
        connection.commit()
    except(Exception, psycopg2.ProgrammingError) as error:
        print(error)

def insert_courses_corpus_into_db(json_file):
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

if __name__ == "__main__":
    get_db_version()
    insert_courses_corpus_into_db('courses_data.json')