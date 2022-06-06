from .clever_config import initialize_clevercloud

def access_clevercloud(key):
    db, db_connection = initialize_clevercloud(key)
    return (db, db_connection)

def cleanup_clever(db):
    db.execute("DROP TABLE IF EXISTS shares")

def download_clever(db):
    sql_command = "SELECT * FROM shares"
    db.execute(sql_command)
    share_list_string = db.fetchall()
    share_list = []
    for x,y in share_list_string:
        share_list.append((int(x), int(y)))
    return share_list[0]

def upload_clever(db, db_connection, share):
    cleanup_clever(db)
    db.execute("CREATE TABLE shares (x VARCHAR(256), y VARCHAR(256))")
    data = (str(share[0]), str(share[1]))
    sql_command = "INSERT INTO shares (x, y) VALUES (%s, %s)"
    db.execute(sql_command, data) 
    db_connection.commit()