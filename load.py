from dotenv import load_dotenv
import os
import psycopg2
import time
from extract import get_popular_movies, parse_movies, get_movie_credits, get_directors
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

def insert_directors():
    cursor.execute("SELECT id FROM movies")
    movie_ids = cursor.fetchall()
    
    for row in movie_ids:
        movie_id = row[0]
        directors = get_directors(movie_id)
        
        for director in directors:
            cursor.execute(
              """
                INSERT INTO directors (id, name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING
              """
                ,(director['id'], director['name'])
            )
            
            cursor.execute(
                """
                INSERT INTO movie_directors (movie_id, director_id)
                VALUES (%s,%s)
                ON CONFLICT (movie_id, director_id) DO NOTHING
                """
                ,(movie_id, director['id'])
            )
        
        time.sleep(0.3)
    
    conn.commit()
    
insert_directors()