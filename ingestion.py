import requests
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# for postgres connection
load_dotenv()  # Load environment variables from .env file
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
# for API connection
FT_CLIENT_ID = os.getenv("FT_CLIENT_ID")
FT_CLIENT_SECRET = os.getenv("FT_CLIENT_SECRET")

TOKEN_URL = "https://francetravail.io/connexion/oauth2/access_token"
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
API_URL = "https://api.francetravail.io/partenaire/offresdemploi"

def get_access_token():
    """Obtain access token from France Travail API"""
    payload = {
        'grant_type': 'client_credentials',
        'client_id': FT_CLIENT_ID,
        'client_secret': FT_CLIENT_SECRET,
        'scope': 'api_offresdemploiv2 o2dso' 
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    try:
        response = requests.post(TOKEN_URL, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print(f"Auth Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Token Fetch Error: {e}")
        return None

def fetch_function(token=None):
    """Fetch data from the API"""
    if not token:
        return None
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            return response.json().get('resultats', [])
        else:
            print(f"Fetch Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"API Fetch Error: {e}")
        return None


def transform_function(raw_data):
    """Transform raw data into a DataFrame"""
    try:
        if raw_data is None:
            return None
        else:
            df = pd.json_normalize(raw_data)
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
    """Main ingestion pipeline: getting token->fetch -> load -> database"""
    token = get_access_token()
    raw_data = fetch_function(token)
    df = transform_function(raw_data)
    load_function(df)

if __name__ == "__main__":
    ingestion()
