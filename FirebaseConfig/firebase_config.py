import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def initialize_firebase(key, app_name):
    cred = credentials.Certificate(key)
    if app_name == "app0":
        try:
            app = firebase_admin.get_app(name='[DEFAULT]')
            firebase_admin.delete_app(app)
        except:
            pass 
        default_app = firebase_admin.initialize_app(cred)
        db = firestore.client(default_app)
    else:
        try:
            app = firebase_admin.get_app(name=app_name)
            firebase_admin.delete_app(app)
        except:
            pass 
        other_app = firebase_admin.initialize_app(cred, name=app_name)
        db = firestore.client(other_app)

    return db