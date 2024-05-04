import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn

def setup_database():
    database = "habits.db"

    sql_create_habits_table = """ CREATE TABLE IF NOT EXISTS habits (
                                        id integer PRIMARY KEY,
                                        habit text NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_create_habits_table)
        except Exception as e:
            print(e)
    else:
        print("Error! cannot create the database connection.")

    if conn:
        conn.close()

setup_database()
