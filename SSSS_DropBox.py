import Shamir_Secret_Sharing_Scheme as SSSS
from DropboxConfig.dropbox_config import dbx

def load_shares_file(share_list):
    f = open("./DropboxConfig/content_upload.txt", "w")
    f.write(str(share_list))
    f.close()

def clear_shares_file():
    f = open("./DropboxConfig/content_upload.txt", "w")
    f.close()

def upload_dropbox(share_list):
    load_shares_file(share_list)
    file_to_upload = open("./DropboxConfig/content_upload.txt", "rb")
    file_to_upload = file_to_upload.read()
    shares_path_dropbox = "/Shares/content_upload.txt"
    dbx.files_upload(file_to_upload, shares_path_dropbox)

def cleanup_dropbox():
    root_path_dropbox = "/Shares"
    dbx.files_delete_v2(root_path_dropbox)

def download_dropbox():
    shares_path_dropbox = "/Shares/content_upload.txt"
    metadata, res = dbx.files_download(path= shares_path_dropbox )
    share_list = res.content.decode('UTF-8')
    return share_list

def start_dropbox(share_list):
    cleanup_dropbox()
    upload_dropbox(share_list)
    clear_shares_file()
    print("Uploaded shares to dropbox: " + str(download_dropbox()))