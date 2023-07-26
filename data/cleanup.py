import pymysql
import pandas as pd
import requests
import os
from sqlalchemy import create_engine

# EXTRACT
def get_connection():
  connection = pymysql.connect(host='deadhead-db.cplvgriavgfs.us-east-1.rds.amazonaws.com',
                            user=db_username,
                            password=db_password,
                            database='deadhead',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
  return connection

def get_all_songs():
conn = get_connection()
with conn:
    with conn.cursor() as cursor:
      query = "SELECT * FROM song"
      cursor.execute(query)
      songs = cursor.fetchall()
      return songs

songs = get_all_songs()

# TRANSFORM
def find_bad_urls(songs):
  working = 0
  broken = 0
  for song in songs:
    # print(song['url'])
    r = requests.head(song['url'], allow_redirects=True) # the limitation here is that if the link is valid and the song is a normal length, it takes a long time for the request to complete
    if r.status_code == 403:
      broken = broken + 1
      song['corrupted'] = 'BadUrl'
    elif r.status_code == 200: 
      working = working + 1
    # print(r.status_code)
    print('{} working. {} broken'.format(working, broken), end='\r')
  return songs

tested_songs = find_bad_urls(songs)

# LOAD
stuff_df = pd.DataFrame(stuff)

engine = create_engine("mysql+pymysql://{}:{}@deadhead-db.cplvgriavgfs.us-east-1.rds.amazonaws.com:3306/deadhead".format(db_username,db_password))

stuff_df.to_sql('song',engine, if_exists='replace', index_label='song_id')