from chalice import Chalice
import requests
import random

app = Chalice(app_name='deadhead_chalice')


@app.route("/concert", cors=True)
def get_concert():
  r = requests.get("https://archive.org/advancedsearch.php?q=collection%3A%22GratefulDead%22&output=json")
  data = r.json()['response']['docs']
  return(random.choice(data))

@app.route("/song", cors=True)
def get_song():
    request = app.current_request
    params = request.query_params
    concert_url = params.get('concert')
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