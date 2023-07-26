import requests
import pandas as pd
import IPython
import random
import re
import mysql.connector
from sqlalchemy import create_engine

# === Concerts ===
# EXTRACT
rows = 500
r = requests.get("https://archive.org/advancedsearch.php?q=collection%3A%22GratefulDead%22&rows={}&output=json".format(rows))
data = r.json()['response']['docs']
raw_concert_df = pd.DataFrame(data)
# TRANSFORM
clean_concert_df = raw_concert_df[['title', 'year', 'coverage', 'identifier','date']]
clean_concert_df = clean_concert_df.rename(columns={"title":"concert_title", "identifier":"concert_archive_id"})
# LOAD
engine = create_engine("mysql+pymysql://{}:{}@deadhead-db.cplvgriavgfs.us-east-1.rds.amazonaws.com:3306/deadhead".format(db_username, db_password))
clean_concert_df.to_sql('concert',engine, if_exists='replace',index_label='concert_id')

# === Songs ===
def getSongs(concert_id, concert_identifier):
  url = "https://archive.org/details/{}".format(concert_identifier)
  songs = requests.get(url+'?output=json')
  songjson = songs.json()

  songs = []
  for key, value in songjson['files'].items():
      if value['format'] == 'Flac' or value['format'] == 'VBR MP3':
        value['song_archive_id'] = key
        value['url'] = "https://ia804601.us.archive.org/0/items/{}{}".format(concert_identifier, key)
        songs.append(value)
  try:
    del songs[0] # Get rid of the tuning song
  except Exception:
    raise Exception('Concert doesnt have a song')

  songs_df = pd.DataFrame(songs)
  try:
    songs_df = songs_df[['title','format','song_archive_id', 'url']]
  except Exception:
    raise Exception('No Title')
  songs_df['concert_id'] = concert_id
  songs_df['corrupted'] = 'No'
  return songs_df

for ind in clean_concert_df.index:
  # print('ID:',ind, "Getting songs for", clean_concert_df['concert_title'][ind], 'concert_archive_id:',clean_concert_df['concert_archive_id'][ind], end='\r')
  print(ind, end='\r')
  try:
    df = getSongs(ind, clean_concert_df['concert_archive_id'][ind])
  except Exception:
    continue
  df = df.rename(columns={"title":"song_title","url":"song_url"})

  df.to_sql('song',engine, if_exists='append',index=False)
