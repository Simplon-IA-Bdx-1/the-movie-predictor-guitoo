#!/usr/bin/env python3

import requests
from movie import Movie
from os import getenv
from math import ceil


class Omdb:
 
    host = 'http://www.omdbapi.com'
    def __init__(self, api_key=None):
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = getenv('OMDB_API_KEY')

    def api_param(self):
        return f'apikey={self.api_key}'

    def search_titles(self, title, year=None):
        params = self.api_param()
        params += f'&s={title}'
        params += f'&type=movie'

        titles = []
        
        if year:
            params += f'&y={year}'

        results = requests.get(f'{self.host}/?{params}').json()
        
        if results['Response'] != 'True':
            return None
        
        for movie in results['Search']:
            titles.append(movie)
        
        nb_results = int(results['totalResults'])
        last_page = ceil(nb_results/10)

        for i in range(2,last_page+1):
            page_param = f'&page={i}'
            results = requests.get(f'{self.host}/?{params}{page_param}').json()
            for movie in results['Search']:
                titles.append(movie)
        return titles
    
    def search_movies(self, title, year=None):
        titles = self.search_titles(title, year)
        
        movies=[]
        for title in titles:
            movie = self.get_imdb_movie(title['imdbID'])
            movies.append(movie)
        return movies

    def get_movie(self, id):
        return self.get_imdb_movie(id)
    
    def get_imdb_movie(self, id):
        params = self.api_param()
        params += f'&i={id}'
        params += f'&type=movie'
        result_json = requests.get(f'{self.host}/?{params}').json()

        # TODO convert date format
        movie = Movie(original_title=result_json['Title'],
                      duration=result_json['Runtime'],
                      release_date=result_json['Released'])

        movie.tmdb_id = id
                
        #print( ' '.join((title, original_title, str(duration), release_date, str(popularity), str(vote), str(revenue), origin_country)) )
        return movie


if __name__ == '__main__':
    from pprint import pprint
    import os
    from dotenv import load_dotenv
   
    load_dotenv()

    movie_db = Omdb(os.getenv('OMDB_API_KEY'))

    #titanic = movie_db.get_imdb_movie('tt0120338')
    #print(titanic)

    movies = movie_db.search_movies('Joker')
    print(len(movies))
    for movie in movies:
        print(movie)

