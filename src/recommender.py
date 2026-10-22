import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("data/movies.csv")

movies["genres"] = movies["genres"].replace("(no genres listed)", "")

tfidf = TfidfVectorizer(token_pattern=r"[^|]+")
tfidf_matrix = tfidf.fit_transform(movies["genres"])


def recommend_movies(movie_title, number_of_recommendations=5):
    movie_title = movie_title.strip()

    if not movie_title:
        return "Please enter a movie name."

    # Check for an exact title match first
    exact_matches = movies[
        movies["title"].str.lower() == movie_title.lower()
    ]

    if not exact_matches.empty:
        movie_index = exact_matches.index[0]

    else:
        # Search without requiring the release year
        titles_without_year = movies["title"].str.replace(
            r"\s*\(\d{4}\)$", "", regex=True
        )

        partial_matches = movies[
            titles_without_year.str.contains(
                movie_title, case=False, regex=False, na=False
            )
        ]

        if partial_matches.empty:
            return "Movie not found. Please try another title."

        return {
            "message": "Select a matching movie title to get recommendations.",
            "matching_titles": partial_matches["title"].head(15).tolist()
        }

    similarity_scores = cosine_similarity(
        tfidf_matrix[movie_index],
        tfidf_matrix
    ).flatten()

    similarity_scores[movie_index] = -1

    top_indices = similarity_scores.argsort()[
        -number_of_recommendations:
    ][::-1]

    return movies.iloc[top_indices][["title", "genres"]]


if __name__ == "__main__":
    while True:
        movie_name = input(
            "\nEnter a movie name (or type 'exit' to quit): "
        )

        if movie_name.strip().lower() == "exit":
            break

        result = recommend_movies(movie_name)

        if isinstance(result, dict):
            print("\n" + result["message"])
            for title in result["matching_titles"]:
                print("-", title)

        elif isinstance(result, str):
            print(result)

        else:
            print(f"\nRecommendations for {movie_name}:")
            print(result.to_string(index=False))
