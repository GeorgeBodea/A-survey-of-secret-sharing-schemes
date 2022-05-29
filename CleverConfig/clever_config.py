import mysql.connector

def initialize_clevercloud(key):
    db_connection = mysql.connector.connect(
        database = key[0]["value"],
        host = key[1]["value"],
        password= key[2]["value"],
        user = key[5]["value"]
    )

    db = db_connection.cursor()
    return (db, db_connection)