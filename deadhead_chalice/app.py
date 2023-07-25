from chalice import Chalice
import requests
import random
import pymysql
import os
#https://www.youtube.com/watch?v=RerDL93sBdY

app = Chalice(app_name='deadhead_chalice')

def get_connection():
   connection = pymysql.connect(host='deadhead-db.cplvgriavgfs.us-east-1.rds.amazonaws.com',
                             user=os.environ['DB_USERNAME'],
                             password=os.environ['DB_PASSWORD'],
                             database='deadhead',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
   return connection

@app.route("/concert", cors=True)
def get_concert():
  conn = get_connection()
  with conn:
     with conn.cursor() as cursor:
        query = "SELECT * FROM concert ORDER BY RAND() LIMIT 1"
        cursor.execute(query)
        concert = cursor.fetchone()
        print(concert)
        return concert

@app.route("/song", cors=True)
def get_song():
    request = app.current_request
    params = request.query_params
    concert_id = params.get('concert')
    conn = get_connection()
    with conn:
      with conn.cursor() as cursor:
          query = "SELECT * FROM song WHERE `concert_id` = {} ORDER BY RAND() LIMIT 1".format(concert_id)
          cursor.execute(query)
          song = cursor.fetchone()
          if song is None:
             raise Exception("Concert has no available songs")
          print(song)
          return song