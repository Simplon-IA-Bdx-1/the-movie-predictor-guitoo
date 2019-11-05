#!/usr/bin/env python3

import requests
from pprint import pprint

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('TMDB_API_KEY')

host='https://api.themoviedb.org/3'


print(api_key)

#'https://api.themoviedb.org/3/'

movie_id=100
result = requests.get(f'{host}/movie/{movie_id}?api_key={api_key}')
result_json=result.json()
#pprint(result.json())

title = result_json['title']
release_date = result_json['release_date']
popularity = result_json['popularity']
origin_country = result_json['production_countries'][0]['name']

print( ' '.join((title, release_date, str(popularity), origin_country)) )
