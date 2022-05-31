from CosmosConfig.cosmos_config import initialize_cosmos

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

# key = { "URI" : "mongodb://george:7YTdTHRD5yaxD5vXtNrkhuecmhwZzMAXlnarKPFRe7fWvcC0NftV0H3S9rK0dBSu79uBxakynE0VZBpAb8ABDw==@george.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@george@"}
# col = access_cosmos(key)
# upload_cosmos(col, (101, 54))
# print(download_cosmos(col))

def start_cosmos(db, share_list):
    cleanup_cosmos(db)
    upload_cosmos(share_list)
    downloaded_shares = download_cosmos(db)
    print("Downloaded shares from cosmos: " + str(downloaded_shares))
    return downloaded_shares