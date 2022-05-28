import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

import tkinter as tk

def initialize_firebase(key, app_name):
    key = json.loads(key)
    cred = credentials.Certificate(key)
    if app_name == "app0":
        default_app = firebase_admin.initialize_app(cred)
        db = firestore.client(default_app)
    else:
        other_app = firebase_admin.initialize_app(cred, name=app_name)
        db = firestore.client(other_app)

    return db