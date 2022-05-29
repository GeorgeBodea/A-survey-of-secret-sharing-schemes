import Shamir_Secret_Sharing_Scheme as SSSS
import SSSS_Firebase
import SSSS_Dropbox
import SSSS_Clever

def input_api(secret, shares_number, threshold):
    secret = int.from_bytes(secret.encode('ASCII'), 'little')

    if threshold > shares_number:
        raise ValueError("The threshold should be lower than the number of total shares")
    if threshold < 1:
        raise ValueError("The threshold should be higher than 0")
    if shares_number < 1:
        raise ValueError("The number of total shares should be higher than 0")
    if SSSS.MAX_BOUND < shares_number:
        raise ValueError("The number of total shares should be lower than the possible maximum number of shares")

    share_list = SSSS.create_shares(secret, threshold, shares_number)
    return share_list

def distribution_firebase_api(key, app_name, share):
    print("Share: " + str(share))
    db = SSSS_Firebase.access_firebase(key, app_name)
    SSSS_Firebase.upload_firebase(db, share)

def retrival_firebase_api(key, app_name):
    db = SSSS_Firebase.access_firebase(key, app_name)
    share = SSSS_Firebase.download_firebase(db)
    print("Share downloaded: " + str(share))
    return share

def distribution_clevercloud_api(key, share):
    print("Share: " + str(share))
    db, db_connection = SSSS_Clever.access_clevercloud(key)
    SSSS_Clever.upload_clever(db, db_connection, share)    

def retrival_clevercloud_api(key):
    db, db_connection = SSSS_Clever.access_clevercloud(key)
    share = SSSS_Clever.download_clever(db)  
    print("Share downloaded: " + str(share)) 
    return share 

def distribution_dropbox_api(key, share):
    print("Share: " + str(share))
    db = SSSS_Dropbox.access_dropbox(key)
    SSSS_Dropbox.upload_dropbox(db, share)    

def retrival_dropbox_api(key):
    db = SSSS_Dropbox.access_dropbox(key)
    share = SSSS_Dropbox.download_dropbox(db)
    print("Share downloaded: " + str(share))
    return share 

def reconstruction_api(shares_list):
    secret = SSSS.reconstruct_secret(shares_list)
    
    print("The secret reconstructed is: " + secret)
    return secret

