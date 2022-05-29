from DropboxConfig.dropbox_config import initialize_dropbox
from ast import literal_eval

def access_dropbox(key):
    db = initialize_dropbox(key)
    return db

def load_shares_file(share_list):
    f = open("./DropboxConfig/content_upload.txt", "w")
    f.write(str(share_list))
    f.close()

def clear_shares_file():
    f = open("./DropboxConfig/content_upload.txt", "w")
    f.close()

def cleanup_dropbox(db):
    root_path_dropbox = "/Shares"
    db.files_delete_v2(root_path_dropbox)    

def upload_dropbox(db, share_list):
    cleanup_dropbox(db)
    load_shares_file(share_list)
    file_to_upload = open("./DropboxConfig/content_upload.txt", "rb")
    file_to_upload = file_to_upload.read()
    shares_path_dropbox = "/Shares/content_upload.txt"
    db.files_upload(file_to_upload, shares_path_dropbox)
    clear_shares_file()

def download_dropbox(db):
    shares_path_dropbox = "/Shares/content_upload.txt"
    metadata, res = db.files_download(path= shares_path_dropbox )
    share_list = res.content.decode('UTF-8')
    share_list = literal_eval(share_list)
    return share_list

def start_dropbox(db, share_list):
    upload_dropbox(db, share_list)
    clear_shares_file(db)
    downloaded_shares = download_dropbox()
    print("Downloaded shares from Dropbox: " + str(downloaded_shares))
    return downloaded_shares
