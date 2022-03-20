import Shamir_Secret_Sharing_Scheme as SSSS
from FirebaseConfig.firebase_config import db

def download_firebase(max_length):
    share_list = []
    for i in range(0, max_length):
        doc = db.collection("Shares").document(str(i)).get()
        doc = doc.to_dict()
        share = (doc["x"], doc["y"])
        share_list.append(share)
    return share_list

def upload_firebase(share_list, max_length):
    for i in range(0, max_length):
        share = share_list[i]
        data = {"x": share[0], "y": share[1]}
        db.collection("Shares").document(str(i)).set(data)    

def cleanup_firebase():
    share_docs = db.collection("Shares").get()
    for share_doc in share_docs:
        key = share_doc.id
        db.collection("Shares").document(key).delete()

def start_cloud():
    share_list = SSSS.start()
    len_share_list = len(share_list)
    first_third_list = int(len_share_list/3)
    cleanup_firebase()
    upload_firebase(share_list, first_third_list)
    print("Uploaded shares to firebase: " + str(download_firebase(first_third_list)))

if __name__ == '__main__':
    start_cloud()