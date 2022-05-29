import dropbox

def initialize_dropbox(key):
    APP_KEY = key["app_key"]
    # key["app_key"]
    ACCESS_TOKEN = key["temporary_token"]
    # key["refresh_token"]

    db = dropbox.Dropbox(app_key=APP_KEY, oauth2_access_token=ACCESS_TOKEN)
    return db