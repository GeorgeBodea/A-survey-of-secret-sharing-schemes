import pymongo

def initialize_cosmos(key):
    client = pymongo.MongoClient(key["URI"])
    db = client["ShamirSecretSharing"]
    col = db["Share"]
    return col