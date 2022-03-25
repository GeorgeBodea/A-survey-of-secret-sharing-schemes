import mysql.connector
import CleverConfig.key as key

dbx_connection = mysql.connector.connect(
    host = key.host,
    user = key.user,
    password= key.password,
    database = key.database
)

dbx = dbx_connection.cursor()