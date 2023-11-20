
import pandas as pd

netflix_data = pd.read_csv('netflix_data.csv')

# Assuming df is your DataFrame and 'listed_in' is the column with genres
genres = netflix_data['listed_in']
# Create a set to store unique genres
unique_genres = set()

# Iterate through each row and split the genres
for genres in netflix_data['listed_in']:
    unique_genres.update(genres.split(", "))

# Create a new DataFrame to store the expanded data
expanded_df = pd.DataFrame(columns=['title'] + list(unique_genres))

# Iterate through each row again and set the genre columns
for index, row in netflix_data.iterrows():
    genres = row['listed_in'].split(", ")
    genre_row = {genre: 1 for genre in genres}
    genre_row['title'] = row['title']
    expanded_df = expanded_df._append(genre_row, ignore_index=True, sort=False)

# Fill NaN values with 0
expanded_df = expanded_df.fillna(0)
print(expanded_df.head())
# Now expanded_df contains a column for each genre

expanded_df.to_csv('genres_expanded.csv', index=False)



#Checking if my dataframe has duplicate titles
has_duplicates = netflix_data['title'].duplicated().sum()

if has_duplicates > 0:
    print(f"The DataFrame has {has_duplicates} duplicate titles.")
else:
    print("The DataFrame does not have any duplicate titles.")


