import sys
import sqlite3 as lite
from imdb import IMDb
import omdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
Objectives: 
- look at trend in Nicolas Cage movie ratings - expect to be trending down
- generate rolling average chart for rotten tomatoes ratings
'''

personName = ''

def storeSearch(person_name):
con = lite.connect('lc.db')

with con:
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS person(person_id INT, person_name TEXT)")
cur.execute("DELETE FROM person WHERE person_id = 1")
cur.execute("INSERT INTO person VALUES(?,?)", (1, person_name))

def returnPriorSearch():
con = lite.connect('lc.db')

with con:
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS person(person_id INT, person_name TEXT)")
cur.execute("SELECT person_name FROM person WHERE person_id=1")
temp = cur.fetchone()

return temp

def createMovieTable():
con = lite.connect('lc.db')

with con:
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS movies")
cur.execute("CREATE TABLE movies(movie_id TEXT, movie_title TEXT, movie_year TEXT, imdb_rating TEXT, rt_critic TEXT, rt_user TEXT)")

def getPersonID(person_name):
ia = IMDb()
first_name = ia.search_person(person_name)[0]
return first_name.personID

def getMovieIDs(person_id):
movieIDList = []
ia = IMDb()
personInfo = ia.get_person(person_id)
for movie in personInfo['actor']:
movieIDList.append(movie.movieID)
return movieIDList

def getMovieInfo(movie_list):
omdb.set_default('tomatoes', True)
movieInfo = []
for movie in movie_list:
movieInfo.append(omdb.imdbid('tt' + str(movie)))
return movieInfo

def createDataArray(movie_info):
dataArray = []
for movie in movie_info:
if len(movie) > 0:
if movie['type']=='movie' and personName in movie['actors']:
tmpArray = []
tmpArray.extend([movie['imdb_id'],movie['title'],movie['year'],movie['imdb_rating'], movie['tomato_meter'],movie['tomato_user_meter']])
dataArray.append(tmpArray)

con = lite.connect('ncage.db')
with con:
cur = con.cursor()
cur.execute("DELETE FROM movies")
cur.executemany("INSERT INTO movies VALUES(?, ?, ?, ?, ?, ?)", dataArray)

def generateIMBDGraph():
con = lite.connect('ncage.db')
with con:
df = pd.read_sql("SELECT movie_id, movie_year, imdb_rating from movies", con, index_col='movie_id')
df = df.applymap(lambda x: np.nan if x == 'N/A' else x)
#df = df.ix[:,0:2]
df = df[df.imdb_rating.notnull()]
df.imdb_rating = df.imdb_rating.astype(float)
df = df.sort(['movie_year'], ascending=[0])
df = df.groupby('movie_year').mean()
return df.plot()

def generateRTCriticGraph():
con = lite.connect('ncage.db')
with con:
df = pd.read_sql("SELECT movie_year, rt_critic from movies", con, index_col='movie_year')
df = df.applymap(lambda x: np.nan if x == 'N/A' else x)
#df = df.ix[:,0:2]
df = df[df.rt_critic.notnull()]
df.rt_critic = df.rt_critic.astype(float)
#df.movie_year = df.movie_year.astype(float)
#df = df.sort(['movie_year'], ascending=[0])
df.sort_index(inplace=True)
df = pd.rolling_mean(df, 4)
#df = df.groupby('movie_year').mean()
return df.plot()

def generateRTUserGraph():
con = lite.connect('ncage.db')
#pd.options.display.mpl_style = 'default'
with con:
df = pd.read_sql("SELECT movie_year, rt_critic, rt_user from movies", con, index_col='movie_year')
df = df.applymap(lambda x: np.nan if x == 'N/A' else x)
#df = df.ix[:,0:2]
df = df[df.rt_user.notnull()]
df = df[df.rt_critic.notnull()]
df.rt_user = df.rt_user.astype(float)
df.rt_critic = df.rt_critic.astype(float)
#df.movie_year = df.movie_year.astype(float)
#df = df.sort(['movie_year'], ascending=[0])
df.sort_index(inplace=True)
df = pd.rolling_mean(df, 10)d
#df = df.groupby('movie_year').mean()
ax = df.plot()
ax.set_title(personName + ' Rolling Average Movie Ratings')
ax.set_ylabel('Rotten Tomatoes Rating')
ax.set_xlabel('Movie Year')
return ax

def getMovieTitles(movie_info):
movieTitles = []
for movie in movie_info:
if movie['type']=='movie':
if personName in movie['actors']:
movieTitles.append(movie['title'])
return movieTitles

if __name__ == "__main__":
personName = 'Nicolas Cage' #change to sys.argv[1]
forceUpdate = False #change to sys.argv[2]
if personName == returnPriorSearch()[0] and not forceUpdate:
#plt.show(generateIMBDGraph())
plt.show(generateRTUserGraph())
#plt.show(generateRTCriticGraph())
#pullDataArray()
else:
createMovieTable()
storeSearch(personName)
personID = getPersonID(personName)
movieIDs = getMovieIDs(personID)
movieInfo = getMovieInfo(movieIDs)
#printMovieInfo(movieInfo)
createDataArray(movieInfo)
plt.show(generateRTUserGraph())
#print analyzePandas()
#pullDataArray()
