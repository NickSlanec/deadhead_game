from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import sqlite3
from sqlite3 import Error
import json
import hashlib

import requests
import pandas as pd
import random
import re

app = Flask(__name__)
cors = CORS(app)

@app.route("/concert")
def get_concert():
  r = requests.get("https://archive.org/advancedsearch.php?q=collection%3A%22GratefulDead%22&output=json")
  data = r.json()['response']['docs']
  df = pd.DataFrame(data)
  concert = df.sample()
  return(concert.to_json(orient='records'))

@app.route("/song")
def get_song():
    concert_url = request.args.get('concert')
    url = "https://archive.org/details/{}".format(concert_url)
    songs = requests.get(url+'?output=json')
    songjson = songs.json()

    songs = []
    for key, value in songjson['files'].items():
        if value['format'] == 'Flac' or value['format'] == 'VBR MP3':
          songs.append({'id':key, 'data': value})
          print(key, value)
    try:
      del songs[0] # Get rid of the tuning song
    except Exception:
      print('Concert doesnt have a song')

    song = random.choice(songs)
    song['url'] = "https://ia804601.us.archive.org/0/items/{}/{}".format(concert_url, song['id'])

    return song