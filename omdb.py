#!/usr/bin/env python3

from movie import Movie
from math import ceil
import datetime
from restclient import RestClient
import re


class Omdb(RestClient):

    def __init__(self, api_key=None):
        RestClient.__init__(self,
                            'http://www.omdbapi.com',
                            api_key,
                            'OMDB_API_KEY')
        self.api_key_argname = 'apikey'

    def search_titles(self, title, year=None):
        args = {'type': 'movie', 's': title}
        if year:
            args['y'] = year
        titles = []
        results = self.get('/', args)
        if results['Response'] != 'True':
            return None
        for movie in results['Search']:
            titles.append(movie)
        nb_results = int(results['totalResults'])
        last_page = ceil(nb_results/10)

        for i in range(2, last_page+1):
            args.update({'page': i})
            results = self.get('/', args)
            for movie in results['Search']:
                titles.append(movie)
        return titles

    def search_movies(self, title, year=None):
        titles = self.search_titles(title, year)
        movies = []
        for title in titles:
            movie = self.get_imdb_movie(title['imdbID'])
            movies.append(movie)
        return movies

    def get_movie(self, id):
        return self.get_imdb_movie(id)

    def get_imdb_movie(self, id):
        args = {'type': 'movie', 'i': id}
        result = self.get('/', args)
        # TODO convert date format
        release_date = datetime.datetime.strptime(
            result['Released'], '%d %b %Y').date()
        duration = re.findall(r'(\d+)', result['Runtime'])[0]
        movie = Movie(original_title=result['Title'],
                      duration=duration,
                      release_date=release_date)
        movie.tmdb_id = id
        return movie


if __name__ == '__main__':

    import os
    from dotenv import load_dotenv

    load_dotenv()

    movie_db = Omdb(os.getenv('OMDB_API_KEY'))

    # titanic = movie_db.get_imdb_movie('tt0120338')
    # print(titanic)

    movies = movie_db.search_movies('Joker', year=2019)
    print(len(movies))
    for movie in movies:
        print(movie)
