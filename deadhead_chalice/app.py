from chalice import Chalice, Response
import requests
import random
import pymysql
import os
#https://www.youtube.com/watch?v=RerDL93sBdY

app = Chalice(app_name='deadhead_chalice')

def get_connection():
   connection = pymysql.connect(host=os.environ['DB_HOSTNAME'],
                             user=os.environ['DB_USERNAME'],
                             password=os.environ['DB_PASSWORD'],
                             database='deadhead',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
   return connection

@app.route("/song", methods=["GET"], cors=True) 
def get_song():
    print("Getting Song")
    conn = get_connection()
    with conn:
      with conn.cursor() as cursor:
          query = "SELECT * FROM song WHERE `corrupted` = 'NO' ORDER BY RAND() LIMIT 1"
          cursor.execute(query)
          song = cursor.fetchone()
          
          query = "SELECT * FROM concert WHERE `concert_id` = {} ".format(song['concert_id'])
          cursor.execute(query)
          concert = cursor.fetchone()
          data = {**song, **concert}
          return data

@app.route("/song/api", methods=["GET"], cors=True) 
def proxy_audio():
    print("Getting Proxy Audio")
    url = app.current_request.query_params.get('url')
    print("URL:", url)
    if not url:
        return Response(body={'error': 'Missing audio URL'}, status_code=400)
    try:
        response = requests.get(url)
        print(response)
        if response.status_code == 200:
            data = response.content
            # print(data)
            return Response(body=data, status_code=200, headers={'Content-Type': 'audio/mp3'})
        else:
            print("NON-200")
            return Response(body={'error': 'Failed to fetch audio file'}, status_code=500)
    except requests.RequestException as e:
        print("FAILED.", e)
        return Response(body={'error': 'Failed to fetch audio file'}, status_code=500)

@app.route("/song/{id}", methods=["PUT"], cors=True)
def update_song(id):
   print("Updating Song")
   request = app.current_request
   body = request.json_body
   print(body)
   query = "UPDATE song SET corrupted = '{}' WHERE song_id = {}".format(body['corrupted'], id)
   print(query)
   conn = get_connection()
   with conn:
      with conn.cursor() as cursor:
         cursor.execute(query)
      conn.commit()

@app.route("/guess", methods=["PUT"], cors=True)
def record_guess():
  print("Recording Guess")
  request = app.current_request
  body = request.json_body
  
  query = "INSERT INTO guess (song_id, guess_year, correct) VALUES ('{}','{}',{});".format(body['song_id'], body['guess'], body['correct'])
  conn = get_connection()
  with conn:
    with conn.cursor() as cursor:
      cursor.execute(query)
    conn.commit()