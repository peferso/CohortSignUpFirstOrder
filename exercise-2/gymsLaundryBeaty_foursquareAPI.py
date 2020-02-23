import json, requests
import foursquare as fs
import pandas as pd
from foursquare_api_tools import foursquare_api_tools as ft
import os

CLIENT_ID = os.environ.get('user1')
CLIENT_SECRET = os.environ.get('pass1')


VERSION = '20180323'
client = fs.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, version=VERSION)

# cities with around 500k population
# Germany:
#   * Duesseldorf 573,057: 51.2385861,6.6742681
#   * Bremen 546,501: 53.1201552,8.5962039
latD ='51.2385861'
lonD ='6.6742681'
latB ='53.1201552'
lonB ='8.5962039'
latL ='45.75801'
lonL ='4.8001016'
latT ='43.6008029'
lonT ='1.3628013'
# France:
#   * Lyon 472,317: 45.75801,4.8001016
#   * Toulouse 433,055: 43.6008029,1.3628013

dfD_G = ft.venues_explore(client, lat=latD, lng=lonD, limit=100, radius=20000, query='fitness')
dfD_G.to_csv('~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfD_G.csv', encoding='utf-8', index=False)

dfD_L = ft.venues_explore(client, lat=latD, lng=lonD, limit=100, radius=20000, query='laundry')
dfD_L.to_csv('~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfD_L.csv', encoding='utf-8', index=False)

dfD_B = ft.venues_explore(client, lat=latD, lng=lonD, limit=100, radius=20000, query='hair')
dfD_B.to_csv('~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfD_B.csv', encoding='utf-8', index=False)



dfL_G = ft.venues_explore(client, lat=latL, lng=lonL, limit=100, radius=20000, query='fitness')
dfL_G.to_csv('~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfL_G.csv', encoding='utf-8', index=False)

dfL_L = ft.venues_explore(client, lat=latL, lng=lonL, limit=100, radius=20000, query='laundry')
dfL_L.to_csv('~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfL_L.csv', encoding='utf-8', index=False)

dfL_B = ft.venues_explore(client, lat=latL, lng=lonL, limit=100, radius=20000, query='hair')
dfL_B.to_csv('~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfL_B.csv', encoding='utf-8', index=False)



dfB_G = ft.venues_explore(client, lat=latB, lng=lonB, limit=100, radius=20000, query='fitness')
dfB_G.to_csv('~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfB_G.csv', encoding='utf-8', index=False)

dfB_L = ft.venues_explore(client, lat=latB, lng=lonB, limit=100, radius=20000, query='laundry')
dfB_L.to_csv('~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfB_L.csv', encoding='utf-8', index=False)

dfB_B = ft.venues_explore(client, lat=latB, lng=lonB, limit=100, radius=20000, query='hair')
dfB_B.to_csv('~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfB_B.csv', encoding='utf-8', index=False)



dfT_G = ft.venues_explore(client, lat=latT, lng=lonT, limit=100, radius=20000, query='fitness')
dfT_G.to_csv('~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfT_G.csv', encoding='utf-8', index=False)

dfT_L = ft.venues_explore(client, lat=latT, lng=lonT, limit=100, radius=20000, query='laundry')
dfT_L.to_csv('~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfT_L.csv', encoding='utf-8', index=False)

dfT_B = ft.venues_explore(client, lat=latT, lng=lonT, limit=100, radius=20000, query='hair')
dfT_B.to_csv('~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfT_B.csv', encoding='utf-8', index=False)




