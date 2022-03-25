import Shamir_Secret_Sharing_Scheme as SSSS
from CleverConfig.clever_config import dbx, dbx_connection

def cleanup_clever():
    dbx.execute("DROP TABLE IF EXISTS shares")

def download_clever():
    sql_command = "SELECT * FROM shares"
    dbx.execute(sql_command)
    share_list = dbx.fetchall()
    return share_list

def upload_clever(share_list):
    dbx.execute("CREATE TABLE shares (x BIGINT(255), y BIGINT(255))")

    length = len(share_list)
    for i in range(0, length):
        share = share_list[i]
        data = (str(share[0]), str(share[1]))
        sql_command = "INSERT INTO shares (x, y) VALUES (%s, %s)"
        dbx.execute(sql_command, data) 
    dbx_connection.commit()

def start_clever(share_list):
    cleanup_clever()
    upload_clever(share_list)
    downloaded_shares = download_clever()
    print("Downloaded shares from Clevercloud: " + str(downloaded_shares))
    return downloaded_shares