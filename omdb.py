#!/usr/bin/env python3

import requests
from movie import Movie
from dotenv import load_dotenv
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

    def search_movies(self, title, year=None, ):
        params = self.api_param()
        params += f'&s={title}'
        params += f'&type=movie'

        imdb_ids=[]
        
        if year:
            params += f'&y={year}'

        results = requests.get(f'{self.host}/?{params}').json()
        
        if results['Response'] != 'True':
            return None
        
        for movie in results['Search']:
            imdb_ids.append(movie['imdbID'])
        
        nb_results = int(results['totalResults'])
        last_page = ceil(nb_results/10)

        for i in range(2,last_page+1):
            page_param = f'&page={i}'
            results = requests.get(f'{self.host}/?{params}{page_param}').json()
            for movie in results['Search']:
                imdb_ids.append(movie['imdbID'])
        return(imdb_ids)
        movies=[]
        for id in imdb_ids:
            movie = self.get_movie(id)
            movies.append(movie)
        return movies

    def get_movie(self, id):
        self.get_imdb_movie(id)
    
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
   
    load_dotenv()

    movie_db = Omdb(os.getenv('OMDB_API_KEY'))

    titanic = movie_db.get_imdb_movie('tt0120338')
    print(titanic)

    #movies = movie_db.search_movies('Joker')
    #pprint(movies)
    #print(len(movies))
    #for movie in movies:
    #    print(movie)
