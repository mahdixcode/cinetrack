from dotenv import load_dotenv
import os
import psycopg2
import time
from extract import get_popular_movies, parse_movies, get_movie_credits, get_directors, get_genres

load_dotenv("/Users/mahdi/Desktop/cinetrack/.env")
print(os.getenv("DB_USER"))
conn = psycopg2.connect(
    host= os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()
print("YES DATABASE IS CONNECTED!")

# --- Insert Movies ---
def insert_movies(movies):
    for movie in movies:
        cursor.execute("""
            INSERT INTO movies (id, title, release_year, rating)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (movie["id"], movie["title"], movie["release_year"], movie["rating"]))
    
    conn.commit()
    print(f"{len(movies)} MOIVE HAS BEEN INSERTED!")
    

data = get_popular_movies()
movies = parse_movies(data["results"])
insert_movies(movies)

# --- Insert Directors ---

def insert_directors():
    cursor.execute("SELECT id FROM movies")
    movie_ids = cursor.fetchall()
    
    for row in movie_ids:
        movie_id = row[0]
        directors = get_directors(movie_id)
        
        directors_data = []
        movie_directors_data = []
        
        for director in directors:
            directors_data.append((director["id"], director["name"]))
            movie_directors_data.append((movie_id, director['id']))
        
        cursor.executemany(
              """
                INSERT INTO directors (id, name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING
              """
                ,directors_data
            )
            
        cursor.executemany(
                """
                INSERT INTO movie_directors (movie_id, director_id)
                VALUES (%s,%s)
                ON CONFLICT (movie_id, director_id) DO NOTHING
                """
                ,movie_directors_data
            )
        
        time.sleep(0.3)
        
    print("DIRECTORS HAS BEEN INSERTED!")
    
    conn.commit()
    
# insert_directors()

# --- Insert Genres ---
def insert_genres():
    
    genres = get_genres()
    
    for genre in genres:
        genres_query = """ INSERT INTO genres (id, name) 
        VALUES (%s, %s) ON CONFLICT (id) DO NOTHING """
        genres_values = (genre["id"], genre["name"])
        cursor.execute(genres_query, genres_values)
        
    print("GENERES HAS BEEN INSERTED!")
    
    conn.commit()

insert_genres()


# --- Insert Movie_ID & Genres_IDS ---

def insert_movie_genres():
    data = get_popular_movies()
    movies = data["results"]
    
    for movie in movies:
        movie_id = movie["id"]
        genre_ids = movie["genre_ids"]
        
        for genre_id in genre_ids:
            genre_id_query = """ INSERT INTO movie_genres(movie_id, genre_id)
            VALUES (%s, %s) 
            ON CONFLICT (movie_id, genre_id) DO NOTHING """
            genre_values = (movie_id, genre_id)
        
            cursor.execute(genre_id_query, genre_values)
        
    print("Movie_ID & Genres_IDS HAVE BEEN INSERTED!")
    conn.commit()    

insert_movie_genres()