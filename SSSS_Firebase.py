import Shamir_Secret_Sharing_Scheme as SSSS
from FirebaseConfig.firebase_config import db

def download_firebase(length):
    share_list = []
    for i in range(0, length):
        doc = db.collection("Shares").document(str(i)).get()
        doc = doc.to_dict()
        share = (doc["x"], doc["y"])
        share_list.append(share)
    return share_list

def upload_firebase(share_list):
    length = len(share_list)
    for i in range(0, length):
        share = share_list[i]
        data = {"x": share[0], "y": share[1]}
        db.collection("Shares").document(str(i)).set(data)    

def cleanup_firebase():
    share_docs = db.collection("Shares").get()
    for share_doc in share_docs:
        key = share_doc.id
        db.collection("Shares").document(key).delete()

def start_firebase(share_list):
    cleanup_firebase()
    upload_firebase(share_list)
    print("Uploaded shares to firebase: " + str(download_firebase(len(share_list))))