import os

tg_token = os.environ['TG_TOKEN']
lastfm_api_key = os.environ['LASTFM_API_KEY']
lastfm_secret_key = os.environ['LASTFM_SECRET_KEY']


db = {"user": os.environ['DB_USER'],
      "password": os.environ['DB_PASS'],
      "address": os.environ['DB_ADDRESS'],
      "port": os.environ['DB_PORT'],
      "db_name": os.environ['DB_NAME']}
