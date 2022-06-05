from FirebaseConfig.firebase_config import initialize_firebase

def access_firebase(key, app_name):
    db = initialize_firebase(key, app_name)
    return db 

def download_firebase(db):
    share_list = []
    docs = db.collection(u'Shares').stream()
    for doc in docs:
        doc = doc.to_dict()
        share = (int(doc["x"]), int(doc["y"]))
        share_list.append(share)
    return share_list[0]

def upload_firebase(db, share):
    cleanup_firebase(db)
    data = {"x": str(share[0]), "y": str(share[1])}
    db.collection("Shares").document().set(data)    

def cleanup_firebase(db):
    share_docs = db.collection("Shares").get()
    for share_doc in share_docs:
        key = share_doc.id
        db.collection("Shares").document(key).delete()