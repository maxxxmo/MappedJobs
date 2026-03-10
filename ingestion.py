import requests
import pandas as pd
import os
from sqlalchemy import create_engine

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
API_URL = "https://api.francetravail.io/partenaire/offresdemploi"

data = [
        {
            "id": 1,
            "titre": "Data Engineer",
            "entreprise": "Tech Solutions",
            "ville": "Paris",
            "salaire": 55000
        },
        {
            "id": 2,
            "titre": "Analyste de données",
            "entreprise": "Eco Data",
            "ville": "Lyon",
            "salaire": 42000
        }
    ]

def fetch_function():
    """Fetch data from the API"""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            raw_data = response.json()
            return raw_data
        else:
            print(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Fetch Error: {e}")
        return None


def transform_function(raw_data):
    """Transform raw data into a DataFrame"""
    try:
        if raw_data is None:
            df = pd.DataFrame(data)  # Fallback to sample data
        else:
            df = pd.DataFrame(raw_data)
        return df
    except Exception as e:
        print(f"Load Error: {e}")
        return None
    
def load_function(df):
    """Load Df into database"""
    if df is not None:
        try:
            engine = create_engine(DB_URL)
            df.to_sql('raw_jobs', engine, if_exists='replace', index=False)
            print("Success!!!!")
        except Exception as e:
            print(f"Database Error: {e}")

def ingestion():
    """Main ingestion pipeline: fetch -> load -> database"""
    raw_data = fetch_function()
    df = transform_function(raw_data)
    load_function(df)

if __name__ == "__main__":
    ingestion()
