#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
from movie import Movie
from person import Person





class MovieManager:

    movies_table = 'movies'
    people_table = 'people'

    movies_fields = ['original_title', 'title', 'duration',
                     'rating', 'release_date']
    people_fields = ['firstname', 'lastname']

    cnx = None
    cursor = None

    def __init__(self,
                 host=None,
                 user=None,
                 password=None,
                 database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connectToDatabase(self):
        self.cnx = mysql.connector.connect(user=self.user,
                                           password=self.password,
                                           host=self.host,
                                           database=self.database)

    def disconnectDatabase(self):
        self.cnx.close()
        self.cnx = None

    def createCursor(self):
        self.cursor = self.cnx.cursor(dictionary=True)

    def closeCursor(self):
        self.cursor.close()
        self.cursor = None

    def findQuery(self, table, id):
        return (f"SELECT * FROM {table} WHERE id = {id} LIMIT 1")

    def findAllQuery(self, table):
        return ("SELECT * FROM {}".format(table))

    def insertPersonQuery(self):
        return insert_query_generator(self.people_table, self.people_fields)
        
    def insertMovieQuery(self):
        return insert_query_generator(self.movies_table, self.movies_fields)

    def sendSelectQuery(self, query):
        self.connectToDatabase()
        self.createCursor()
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if (self.cursor.rowcount == 0):
            results = None
        self.closeCursor()
        self.disconnectDatabase()
        return results

    def sendInsertQuery(self, query, data):
        self.connectToDatabase()
        self.createCursor()
        self.cursor.execute(query, data)
        self.cnx.commit()
        last_id = self.cursor.lastrowid
        self.closeCursor()
        self.disconnectDatabase()
        return last_id

    def find(self, table, id):
        query = self.findQuery(table, id)
        results = self.sendSelectQuery(query)
        if results:
            return results[0]
        return None

    def find_movie(self, id):
        result = self.find(self.movies_table, id)
        if result:
            movie = Movie(result['title'],
                          result['original_title'],
                          result['duration'],
                          result['rating'],
                          result['release_date'])
            movie = Movie(**result)
            movie.id = result['id']
            return movie
        return None

    def find_person(self, id):
        result = self.find(self.movies_table, id)
        if result:
            person = Person(result['firstname'],
                            result['lastname'])
            person = Person(**result)
            person.id = result['id']
            return person
        return None 


def insert_query_generator(table, fields):
    sep = ', '
    columns = ['`'+field+'`' for field in fields]
    placeholders = sep.join(['%s'] * len(fields))
    query = f"INSERT INTO `{table}`"
    query += f"({sep.join(columns)})"
    query += "VALUES({});".format(placeholders)
    return query


if __name__ == '__main__':
    mm = MovieManager('127.0.0.1', 'predictor', 'predictor', 'predictor')
    print(mm.insertPersonQuery())
    print(mm.insertMovieQuery())
    print(mm.find_movie(1))
