import requests
import time
from dotenv import load_dotenv
import os

load_dotenv("/Users/mahdi/Desktop/cinetrack/.env")

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def get_popular_movies():
    url = f"{BASE_URL}/movie/popular"
    params = {"api_key": API_KEY, "language": "en-US", "page": 1}
    response = requests.get(url, params=params)
    return response.json()

def parse_movies(raw_movies):
    parsed = []
    for movie in raw_movies:
        parsed.append({
            "id": movie["id"],
            "title": movie["title"],
            "release_year": int(movie["release_date"][:4]),
            "rating": movie["vote_average"]
        })
    return parsed

data = get_popular_movies()
raw_movies = data["results"]
parsed_movies = parse_movies(raw_movies)

def get_movie_credits(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {"api_key": API_KEY, "language": "en-US", "page": 1}
    response = requests.get(url, params=params)
    time.sleep(0.3)
    return response.json()

def get_directors(movie_id):
    credits = get_movie_credits(movie_id)
    crew = credits["crew"]
    directors = [person for person in crew if person["job"] == "Director"]
    return directors

def get_genres():
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY, "language": "en-US", "page": 1}
    response = requests.get(url , params=params)
    time.sleep(0.3)
    genres_data = response.json()
    return genres_data["genres"]

for i in data["results"]:
    print(i["id"])
    print(i["genre_ids"])