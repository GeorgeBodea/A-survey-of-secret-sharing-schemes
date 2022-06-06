from .cosmos_config import initialize_cosmos

def access_cosmos(key):
    collection = initialize_cosmos(key)
    return collection 

def cleanup_cosmos(col):
    for data in col.find():
        id = data["_id"]
        col.delete_one({"_id": id})

def download_cosmos(col):
    for data in col.find():
        share = (int(data["x"]), int(data["y"]))
    return share

def upload_cosmos(col, share):
    cleanup_cosmos(col)
    data = { "x": str(share[0]), "y": str(share[1]) }
    col.insert_one(data) 