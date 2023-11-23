import psycopg2
import pandas as pd

# defining the methods that deal with the database connection
class DataManager:
    def __init__(self, dbname, user, password, host, port):
        try:
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            print(f"Error: Could not connect to the database. {e}")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error executing query: {query}. {e}")
            return []

    def close_connection(self):
        try:
            self.cursor.close()
            self.conn.close()
        except psycopg2.Error as e:
            print(f"Error while closing connection. {e}")

    def get_movie(self):
        query = "SELECT movie.official_title, produced.country, movie.year, rating.votes, rating.score FROM imdb.produced LEFT JOIN imdb.movie ON produced.movie = movie.id LEFT JOIN imdb.rating ON produced.movie = rating.movie WHERE rating.votes >0 AND movie.year IS NOT NULL;"
        return pd.DataFrame(self.execute_query(query), columns=['official_title', 'country', 'year', 'votes','score'])
