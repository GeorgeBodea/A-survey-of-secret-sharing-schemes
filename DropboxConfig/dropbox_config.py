import dropbox
import DropboxConfig.keys as keys

APP_KEY = keys.app_key
REFRESH_TOKEN = keys.refresh_token

dbx = dropbox.Dropbox(oauth2_refresh_token=REFRESH_TOKEN, app_key=APP_KEY)