import mysql.connector
import os

def get_connection(db_name):
    conn=mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.getenv("db_pass"),
        database=db_name
    )

    return conn