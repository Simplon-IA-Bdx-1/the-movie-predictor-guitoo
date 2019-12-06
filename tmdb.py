#!/usr/bin/env python3

from movie import Movie
from person import Person
from restclient import RestClient
from pprint import pprint
from time import sleep

class Tmdb(RestClient):

    # host = 'https://api.themoviedb.org/3'
    language = 'fr'
    region = 'FR'

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

    def query_string(self, command='', args={}):
        string = RestClient.query_string(self, command,
                                         {**args, **self.language_arg()})
        return string

    def search_titles(self, query, year=None,
                      primary_release_year=None, region=None):
        args = {'query': query, 'page': 1}
        keep_going = True
        page = 1
        if year:
            args['year'] = year
        if primary_release_year:
            args['primary_release_year'] = primary_release_year
        if region:
            args['region'] = region

        titles = []
        while keep_going:
            response = self.get('/search/movie/', args)
            results = response['results']
            last_page = int(response['total_pages'])
            for title in results:
                titles.append(title)
            if page < last_page:
                page += 1
                args.update({'page': page})
            else:
                keep_going = False
        for i in range(2, last_page+1):
            args.update({'page': i})
            response = self.get('/search/movie/', args)
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
            if movie is not None:
                movies.append(movie)
        return movies

    def get_imdb_movie(self, imdb_id):
        # args = {'external_source': 'imdb_id'}
        # results = self.get(f'/find/{imdb_id}', args)['movie_results']
        # if len(results) > 0:
        #    id = results[0]['id']
        #    return self.get_movie(id)
        # return None
        return self.get_movie(imdb_id)

    def get_person(self, id):
        args = {}
        result = self.get(f'/person/{id}', args)
        person = Person(name=result['name'], imdb_id=result['imdb_id'])
        return person

    def get_person_imdb_id(self, person_tmdb_id):
        args = {}
        result = self.get(f'/person/{person_tmdb_id}/external_ids', args)
        return result['imdb_id']

    def get_credits(self, imdb_id):
        actors = []
        
        result = self.get(f'/movie/{imdb_id}/credits')
        # return result
        for i, actor in enumerate(result['cast']):
            actor_tmdb_id = int(actor['id'])
            person_id = self.get_person_imdb_id(actor_tmdb_id)
            person = Person(name=actor['name'], imdb_id=person_id)
            if person_id is not None:
                actors.append(person)
                # print(person)
            if i % 10 == 9:
                sleep(2)

        writers = []
        directors = []
        producers = []
        editors = []
        for i, crew in enumerate(result['crew']):
            if crew['job'] in ['Screenplay', 'Director', 'Editor', 'Producer']:
                crew_tmdb_id = int(crew['id'])
                person_id = self.get_person_imdb_id(crew_tmdb_id)
                person = Person(name=crew['name'], imdb_id=person_id)
                if person_id is not None:
                    if crew['job'] == 'Screenplay':
                        writers.append(person)
                    elif crew['job'] == 'Director':
                        directors.append(person)
                    elif crew['job'] == 'Editor':
                        editors.append(person)
                    elif crew['job'] == 'Producer':
                        producers.append(person)
                    # print(person)
                if i % 10 == 9:
                    sleep(2)
        return {'actors': actors,
                'writers': writers,
                'editors': editors,
                'directors': directors,
                'producers': producers}
    
    def get_movie(self, id):
        args = {'region': self.region}
        result = self.get(f'/movie/{id}', args)
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
        movie.synopsis = result['overview']
        movie.production_budget = result['budget']
        movie.tmdb_id = result['id']
        movie.imdb_id = result['imdb_id']
        movie.score = result['vote_average']
        # print(movie)
        return movie

    def get_titles_by_dates(self, from_date, to_date):
        args = {'region': self.region,
                'release_date.gte': from_date,
                'release_date.lte': to_date}
        response = self.get(f'/discover/movie', args)
        results = response['results']
        last_page = int(response['total_pages'])

        titles = []
        for title in results:
            titles.append(title)
        for i in range(2, last_page+1):
            args.update({'page': i})
            response = self.get('/discover/movie/', args)
            results = response['results']
            for title in results:
                titles.append(title)
        return titles

    def get_movies_by_dates(self, from_date, to_date):
        titles = self.get_titles_by_dates(from_date, to_date)
        movies = []
        for item in titles:
            movie = self.get_movie(item['id'])
            movies.append(movie)
        return movies


if __name__ == '__main__':

    import os
    from dotenv import load_dotenv
    load_dotenv()

    movie_db = Tmdb(os.getenv('TMDB_API_KEY'))

    # titanic = movie_db.get_imdb_movie('tt0120338')
    titanic = movie_db.get_credits('tt0120338')
    pprint(titanic)
    #print(titanic)

    #movie = movie_db.get_movie(100)
    #print(movie)

    #movies = movie_db.search_movies('Joker', year=2019)
    #print(len(movies))
    #for movie in movies:
        #print(movie)
