import mysql.connector
import os

#The funtion that return the connection to the database according to the name of it
def get_connection(db_name):
    conn=mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.getenv("db_pass"),
        database=db_name
    )

    return conn