#!/usr/bin/env python3

from movie import Movie
from restclient import RestClient


class Tmdb(RestClient):

    # host = 'https://api.themoviedb.org/3'
    language = 'fr'

    def __init__(self, api_key=None):
        RestClient.__init__(self,
                            'https://api.themoviedb.org/3',
                            api_key,
                            'TMDB_API_KEY')
        self.api_key_argname = 'api_key'

    def language_query(self):
        return f'&language={self.language}'

    def language_arg(self):
        return {'language': self.language}

    def query_string(self, args={}, command=''):
        string = RestClient.query_string(self,
                                         {**args, **self.language_arg()},
                                         command)
        return string

    def search_titles(self, query, year=None,
                      primary_release_year=None, region=None):
        args = {'query': query}

        if year:
            args['year'] = year
        if primary_release_year:
            args['primary_release_year'] = primary_release_year
        if region:
            args['region'] = region

        response = self.get(args, '/search/movie/')
        results = response['results']
        last_page = int(response['total_pages'])

        titles = []
        for title in results:
            titles.append(title)
        for i in range(2, last_page+1):
            args.update({'page': i})
            response = self.get(args, '/search/movie/')
            results = response['results']
            for title in results:
                titles.append(title)
        return titles

    def search_movies(self, query, year=None,
                      primary_release_year=None, region=None):
        titles = self.search_titles(query, year, primary_release_year, region)
        movies = []
        for item in titles:
            movie = self.get_movie(item['id'])
            movies.append(movie)
        return movies

    def get_imdb_movie(self, imdb_id):
        args = {'external_source': 'imdb_id'}
        results = self.get(args, f'/find/{imdb_id}')['movie_results']
        if len(results) > 0:
            id = results[0]['id']
            return self.get_movie(id)
        return None

    def get_movie(self, id):
        result = self.get(command=f'/movie/{id}')
        title = result['title']
        release_date = result['release_date']
        duration = result['runtime']
        original_title = result['original_title']
        # origin_country = result_json['production_countries'][0]['name']
        movie = Movie(title, original_title, duration,
                      release_date=release_date)
        # popularity = result_json['popularity']
        # vote =  result_json['vote_average']
        # revenue = result_json['revenue']
        movie.tmdb_id = id
        return movie


if __name__ == '__main__':
    from pprint import pprint
    import os
    from dotenv import load_dotenv
    load_dotenv()

    movie_db = Tmdb(os.getenv('TMDB_API_KEY'))

#    titanic = movie_db.get_imdb_movie('tt0120338')
#    print(titanic)

#    movie = movie_db.get_movie(100)
#    print(movie)
   
    movies = movie_db.search_movies('Joker')
    print(len(movies))
    for movie in movies:
        pprint(movie)
