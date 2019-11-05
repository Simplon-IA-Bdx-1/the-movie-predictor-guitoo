#!/usr/bin/env python3

import requests
from movie import Movie
from dotenv import load_dotenv
from os import getenv

class Tmdb:

    host = 'https://api.themoviedb.org/3'
    language = 'fr'
    
    
    def __init__(self, api_key=None):
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = getenv('TMDB_API_KEY')
            

    def api_headers(self):
        return {"Authorization":f"Bearer {self.api_key}"}

    def language_query(self):
        return f'&language={self.language}'
    
    def search_movies(self, query=None, year=None, primary_release_year=None, region=None):
        if query == None and year == None and primary_release_year == None and region == None:
            #TODO error handling
            return None
        params = f'?api_key={self.api_key}{self.language_query()}'
        if query:
            params += f'&query={query}'
        if year:
            params += f'&year={year}'
        if primary_release_year:
            params += f'&primary_release_year={primary_release_year}'    
        if region:
            params += f'&region={region}'
        results = requests.get(f'{self.host}/search/movie/{params}').json()['results']
        movies=[]
        for item in results:
            id = item['id']
            movie = self.get_movie(id)
            movies.append(movie)
        return movies

    def get_imdb_movie(self, imdb_id):
        params = f'?api_key={self.api_key}{self.language_query()}'
        params += '&external_source=imdb_id'
        results = requests.get(f'{self.host}/find/{imdb_id}{params}').json()['movie_results']
        if len(results) > 0:
            id = results[0]['id']
            return self.get_movie(id)
        return None

    def get_movie(self, id):
        params = f'?api_key={self.api_key}{self.language_query()}'
        result_json = requests.get(f'{self.host}/movie/{id}{params}').json()
        title = result_json['title']
        release_date = result_json['release_date']
        duration = result_json['runtime']
        original_title = result_json['original_title']
        #origin_country = result_json['production_countries'][0]['name']
       
        movie = Movie(title, original_title, duration, release_date=release_date)
        #popularity = result_json['popularity']
        #vote =  result_json['vote_average']
        #revenue = result_json['revenue']
        
        movie.tmdb_id = id
                
        #print( ' '.join((title, original_title, str(duration), release_date, str(popularity), str(vote), str(revenue), origin_country)) )
        return movie


if __name__ == '__main__':
    from pprint import pprint
    import os
    
    
    load_dotenv()

    movie_db = Tmdb(os.getenv('TMDB_API_KEY'))

    titanic = movie_db.get_imdb_movie('tt0120338')
    print(titanic)

    movie = movie_db.get_movie(100)
    print(movie)
    
    movies = movie_db.search_movies('Joker', year=2019)
    for movie in movies:
        print(movie)
