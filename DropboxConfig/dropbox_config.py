import dropbox
from DropboxConfig.keys import app_key, refresh_token

APP_KEY = app_key
REFRESH_TOKEN = refresh_token

dbx = dropbox.Dropbox(oauth2_refresh_token=REFRESH_TOKEN, app_key=APP_KEY)