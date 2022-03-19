import Shamir_Secret_Sharing_Scheme as SSSS
from CloudFirebase.firebase_config import db

def reconstruct_secret_cloud():
    return 1

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

def start_cloud():
    share_list = SSSS.start()
    len_share_list = len(share_list)
    half_share_list = int(len_share_list/2)
    upload_firebase(share_list, half_share_list)
    print(download_firebase(half_share_list))

if __name__ == '__main__':
    start_cloud()