
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, str(Path(__file__).resolve().parent))

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from recommender import recommend_movies

app = FastAPI(title="CineMatch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"



def get_poster(title):
    if not TMDB_API_KEY:
        return None

    try:
        import re

        match = re.search(r"\((\d{4})\)$", title)
        year = match.group(1) if match else None

        clean_title = re.sub(r"\s*\(\d{4}\)$", "", title).strip()

        params = {
            "api_key": TMDB_API_KEY,
            "query": clean_title,
            "include_adult": "false",
        }

        if year:
            params["year"] = year

        response = requests.get(
            TMDB_SEARCH_URL,
            params=params,
            timeout=5,
        )
        response.raise_for_status()

        results = response.json().get("results", [])

        if not results:
            return None

        # Prefer a result matching the movie's release year.
        if year:
            year_matches = [
                item for item in results
                if item.get("release_date", "").startswith(year)
            ]

            if year_matches:
                results = year_matches

        # Choose the first result that actually has a poster.
        for item in results:
            poster_path = item.get("poster_path")

            if poster_path:
                return (
                    "https://image.tmdb.org/t/p/w500"
                    + poster_path
                )

    except requests.RequestException as error:
        print(f"TMDB poster lookup failed for {title}: {error}")

    return None



@app.get("/")
def home():
    return {"message": "Welcome to CineMatch API!"}


@app.get("/recommend")
def get_recommendations(movie: str, count: int = 5):
    results = recommend_movies(movie, count)

    if isinstance(results, str):
        return {
            "message": results,
            "recommendations": [],
        }

    if isinstance(results, dict):
        return results

    recommendation_list = results.to_dict(orient="records")

    for item in recommendation_list:
        item["poster_url"] = get_poster(item["title"])

    return {
        "searched_movie": movie,
        "recommendations": recommendation_list,
    }
