# CineTrack 🎬

A data pipeline that extracts movie data from TMDB API 
and loads it into PostgreSQL for analysis.

## Tech Stack
- Python
- PostgreSQL
- TMDB API

## Setup
1. Clone the repo
2. Install dependencies: `pip3 install requests psycopg2-binary python-dotenv`
3. Create `.env` file based on `.env.example`
4. Run `python3 load.py`

## Data Pipeline
TMDB API → extract.py → load.py → PostgreSQL