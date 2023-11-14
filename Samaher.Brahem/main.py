from data import DataManager

# Opening the connection
imdb_data = DataManager(
    dbname='imdb',
    user='samaher',
    password="CodingIsFun++",
    host='localhost',
    port='5432'
)

# Get data from the movie table
movie_data = imdb_data.get_movie()

# Get data from the genre table
genre_data = imdb_data.get_genre()

# Get data from the produced table
prod_data = imdb_data.get_prod()

# Get data from the rating table
rating_data = imdb_data.get_rating()

# Get data from the crew table
crew_data = imdb_data.get_crew()




# Closing the connection
imdb_data.close_connection()
