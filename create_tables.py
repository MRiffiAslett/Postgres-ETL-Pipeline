from Queries import create_table_queries, drop_table_queries
import psycopg2


def create_tables(cur, conn):
    """
    Creates individual tables by executing the queries from the create_table_queries list.    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    """
    Drops the sparkify database if it exists, and then creates a new instance of the sparkify database.
    Establishes a connection to the sparkify database and retrieves a cursor object for executing SQL queries.
    Drops all existing tables in the sparkify database.
    Creates all the necessary tables in the sparkify database.
    Closes the connection to the sparkify database.
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()




def drop_tables(cur, conn):
    """
    Drops each table using the queries in the `drop_table_queries` list.

    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def create_database():
    """
    Initiates a connection to the database server.
    Deletes any existing sparkifydb database and creates a new one.
    Returns the connection and cursor objects associated with the sparkifydb database.
    """
    
    # Connect to the default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=Datascience1*")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # Create the sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # Close the connection to the default database
    conn.close()    
    
    # Connect to the sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=Datascience1*")
    cur = conn.cursor()
    
    return cur, conn





if __name__ == "__main__":
    main()
