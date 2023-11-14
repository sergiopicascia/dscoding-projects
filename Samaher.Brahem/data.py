import psycopg2
import pandas as pd

class DataManager:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def get_movie(self):
        query = "SELECT movie.official_title, movie.year, rating.votes FROM imdb.movie LEFT JOIN imdb.rating ON movie.id = rating.movie WHERE rating.votes >0 AND movie.year IS NOT NULL;"
        return pd.DataFrame(self.execute_query(query), columns=['official_title', 'year','votes'])

    def get_genre(self):
        query = "SELECT movie.official_title, genre.genre FROM imdb.genre LEFT JOIN imdb.movie ON movie.id = genre.movie LEFT JOIN imdb.rating ON rating.movie = genre.movie WHERE rating.votes >0;"
        return pd.DataFrame(self.execute_query(query), columns=['official_title', 'genre'])

    def get_prod(self):
        query = "SELECT movie.official_title, produced.country FROM imdb.produced LEFT JOIN imdb.movie ON produced.movie = movie.id LEFT JOIN imdb.rating ON produced.movie = rating.movie WHERE rating.votes >0;"
        return pd.DataFrame(self.execute_query(query), columns=['official_title', 'country'])

    def get_rating(self):
        query = "SELECT movie.official_title, movie.year, rating.votes, rating.score, rating.scale FROM imdb.movie LEFT JOIN imdb.rating ON movie.id = rating.movie WHERE rating.votes >0;"
        return pd.DataFrame(self.execute_query(query), columns=['official_title', 'year', 'votes', 'score', 'scale'])

    def get_crew(self):
        query = "SELECT movie.official_title, person.given_name, crew.p_role FROM imdb.crew LEFT JOIN imdb.movie ON crew.movie = movie.id LEFT JOIN imdb.person ON crew.person = person.id LEFT JOIN imdb.rating ON crew.movie = rating.movie WHERE rating.votes > 0;"
        return pd.DataFrame(self.execute_query(query), columns=['official_title', 'given_name', 'p_role'])
