import psycopg2
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
    

if __name__ == "__main__":
    get_db_version()