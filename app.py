#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TheMoviePredictor script
Author: Arnaud de Mouhy <arnaud@admds.net>
Author: Guillaume Meurisse <g.meurisse.ia@gmail.com>
"""

import mysql.connector
import sys
import argparse
import csv
import requests
from bs4 import BeautifulSoup
import re

def connectToDatabase():
    return mysql.connector.connect(user='predictor', password='predictor',
                              host='127.0.0.1',
                              database='predictor')

def disconnectDatabase(cnx):
    cnx.close()

def createCursor(cnx):
    return cnx.cursor(dictionary=True)

def closeCursor(cursor):    
    cursor.close()

def findQuery(table, id):
    return ("SELECT * FROM {} WHERE id = {}".format(table, id))

def findAllQuery(table):
    return ("SELECT * FROM {}".format(table))

def insertPersonQuery(table,firstname,lastname):
    return ("INSERT INTO {} (`firstname`, `lastname`) VALUES (\"{}\", \"{}\");".format(table,firstname,lastname))

def insertMovieQuery(table, title, duration, original_title, rating, release_date):
    return ("""INSERT INTO {} (`title`, `duration`, `original_title`, `rating`, `release_date`)
               VALUES (\"{}\", {}, \"{}\", \"{}\", \"{}\");""".format(table, title, duration, original_title, rating, release_date))

def insertMovieDictQuery(table, movie):
    fields=[]
    values=[]
    for key in movie:
        fields.append('`'+ key+ '`')
        values.append('\"' + movie[key]+ '\"')
    sep=', '
    return ("""INSERT INTO {} ({})
               VALUES ({});""".format(table, sep.join(fields), sep.join(values)))


def sendSelectQuery(query):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(query)
    results = cursor.fetchall()
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return results

def sendInsertQuery(query):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(query)
    cnx.commit()
    closeCursor(cursor)
    disconnectDatabase(cnx)

def find(table, id):
    query = findQuery(table, id)
    return sendSelectQuery(query)

def findAll(table):
    return sendSelectQuery(findAllQuery(table))

def insertPerson(table,firstname, lastname):
    query = insertPersonQuery(table, firstname, lastname)
    sendInsertQuery(query)

def insertMovie(table, title, duration, original_title, rating, release_date):
    query = insertMovieQuery(table, title, duration, original_title, rating, release_date)
    sendInsertQuery(query)

def insertMovieDict(table, movie):
    query = insertMovieDictQuery(table, movie)
    print(query)
    sendInsertQuery(query)


def printPerson(person):
    print("#{}: {} {}".format(person['id'], person['firstname'], person['lastname']))

def printMovie(movie):
    print("#{}: {} released on {}".format(movie['id'], movie['title'], movie['release_date']))

def find_text_in_tag(tag_name,string):
    return lambda tag: tag.name==tag_name and string in tag.get_text()

def scrapWikiPage(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    infos={}
    infos['title'] = soup.find('div', class_='infobox_v3').find('div', class_='entete').find('cite').get_text()
    section = soup.find('span', class_='mw-headline', text='Fiche technique').parent.findNext('ul')
    item = section.find(find_text_in_tag('li','Titre original'))
    if item:
        infos['original_title']=item.find('i').get_text()
    item = section.find(find_text_in_tag('li','Pays d\'origine'))
    if item:
        infos['origin_country']=item.find('span').get_text().lstrip(' ')
    item = section.find(find_text_in_tag('li','Durée'))
    if item:
        infos['duration']=re.findall('(\d+)', item.get_text())[0]
    item = section.find(find_text_in_tag('li','Dates de sortie'))
    if item:
        infos['release_date']=re.findall('(\d+)\s(\w+)\s(\d+)', item.get_text())
        

    return infos
    

def scrapWikiPageb(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    infos = {}
    infos['title'] = soup.find('div', class_='infobox_v3').find('div', class_='entete').find('cite').get_text()
    keys = soup.find('div', class_='infobox_v3').find('tbody').find_all('th')
    values =soup.find('div', class_='infobox_v3').find('tbody').find_all('td')
    
    for row, raw_key in enumerate(keys):
        key = raw_key.get_text()
        if key=='Titre original':
            infos['original_title']=values[row].get_text().lstrip('\n')
        elif key=='Sortie':
            infos['release_date']=values[row].get_text().lstrip('\n')
        elif key=='Durée':
            infos['duration']=values[row].get_text().lstrip('\n').strip('\xa0minutes')
        elif key=='Acteurs principaux':
            actors=values[row].find_all('a')
            infos['cast']=[]
            for i,actor in enumerate(actors):
                infos['cast'].append(actor.get_text())
        else:
            if len(values[row].find_all('a')) >1:
                entries=values[row].find_all('a')
                infos[key]=[]
                for i,entry in enumerate(entries):
                    if entry.get_text() != '':
                        infos[key].append(entry.get_text())
            else:
                infos[key]=values[row].get_text().lstrip('\n')
    return infos



pre_parser = argparse.ArgumentParser(add_help=False)
pre_parser.add_argument('context', choices=['people', 'movies'], nargs='?')
args,remaining_args = pre_parser.parse_known_args()
context=args.context

parser = argparse.ArgumentParser(description='Process MoviePredictor data')
parser.add_argument('context', choices=['people', 'movies'], help='le contexte dans lequel nous allons travailler')

action_subparser = parser.add_subparsers(title='action', dest='action')

list_parser = action_subparser.add_parser('list', help='liste les entitées du contexte')
list_parser.add_argument('--export' , help='chemin du fichier exporté')

find_parser = action_subparser.add_parser('find', help='trouve une entité selon un paramètre')
find_parser.add_argument('id' , help='identifant à  rechercher')
insert_parser = action_subparser.add_parser('insert', help='insère une nouvelle entité')

if context == "people":
    insert_parser.add_argument('--firstname' , help='prénom de l\'entité à insérer', required=True)
    insert_parser.add_argument('--lastname' , help='nom de famille de l\'entité à insérer', required=True)
elif context == "movies":
    insert_parser.add_argument('--title', help='titre du film à insérer', required=True)
    insert_parser.add_argument('--duration', type=int, help='durée du film à insérer', required=True)
    insert_parser.add_argument('--original-title', help='titre original du film à insérer', required=True)
    insert_parser.add_argument('--rating', choices=["TP","-12", "-16", "-18"], help='catégorie d\'age du film à insérer', required=True)   
    insert_parser.add_argument('--release-date', metavar='YYYY-MM-DD',help='date de sortir du film à insérer', required=True)
    
    import_parser = action_subparser.add_parser('import', help='importe des entités à partir d\'un fichier')
    import_parser.add_argument('--file' , metavar='file.csv', help='fichier d\'où importer les entitées', required=True)

    movie_parser =  action_subparser.add_parser('scrap', help='importe des entités à partir d\'une page Wikipedia')
    movie_parser.add_argument('url' , help='page Wikipedia d\'un film')
     
args = parser.parse_args()

if args.context == "people":
    if args.action == "list":
        people = findAll("people")
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].keys())
                for person in people:
                    writer.writerow(person.values())
        else:
            for person in people:
                printPerson(person)
    if args.action == "find":
        peopleId = args.id
        people = find("people", peopleId)
        for person in people:
            printPerson(person)
    if args.action == "insert":
        insertPerson("people", args.firstname, args.lastname)

if args.context == "movies":
    if args.action == "list":  
        movies = findAll("movies")
        for movie in movies:
            printMovie(movie)
    if args.action == "find":  
        movieId = args.id
        movies = find("movies", movieId)
        for movie in movies:
            printMovie(movie)
    if args.action == "insert":
        insertMovie("movies", args.title, args.duration, args.original_title, args.rating, args.release_date)
    if args.action == "import":
        with open(args.file, 'r',newline='\n',encoding='utf-8') as csvfile:
            reader=csv.DictReader(csvfile)
            for row in reader:
#                insertMovie("movies", row['title'], row['duration'], row['original_title'], row['rating'], row['release_date'])
                insertMovieDict("movies", row)
    if args.action == 'scrap':
        print(scrapWikiPage(args.url))                     
