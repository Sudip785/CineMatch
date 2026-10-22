
import pandas as pd

movies = pd.read_csv("data/movies.csv")

print("First 5 movies:")
print(movies.head())

print("\nDataset information:")
print("Total movies:", len(movies))
print("Columns:", movies.columns.tolist())


print("\nUnique genres:")

all_genres = set()

for genre_list in movies["genres"]:
    for genre in genre_list.split("|"):
        all_genres.add(genre)

print(sorted(all_genres))
print("Total unique genres:", len(all_genres))
