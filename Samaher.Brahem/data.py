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

    def get_movie_release_years(self):
        query = "SELECT official_title, year FROM imdb.movie;"
        return pd.DataFrame(self.execute_query(query), columns=['official_title', 'year'])

    def get_movie_genres(self):
        query = "SELECT movie.official_title, genre.genre FROM imdb.genre LEFT JOIN imdb.movie ON movie.id = genre.movie;"
        return pd.DataFrame(self.execute_query(query), columns=['official_title', 'genre'])

    def get_producing_countries(self):
        query = "SELECT movie.official_title, produced.country FROM imdb.produced LEFT JOIN imdb.movie ON produced.movie = movie.id;"
        return pd.DataFrame(self.execute_query(query), columns=['official_title', 'country'])

    def get_rating_info(self):
        query = "SELECT movie.official_title, rating.votes, rating.score, rating.scale FROM imdb.movie LEFT JOIN imdb.rating ON movie.id = rating.movie;"
        return pd.DataFrame(self.execute_query(query), columns=['official_title', 'votes', 'score', 'scale'])

    def get_crew_contributions(self):
        query = "SELECT movie.official_title, person.given_name, crew.p_role FROM imdb.crew LEFT JOIN imdb.movie ON crew.movie = movie.id LEFT JOIN imdb.person ON crew.person = person.id;"
        return pd.DataFrame(self.execute_query(query), columns=['official_title', 'given_name', 'p_role'])
