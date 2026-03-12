from sqlalchemy import create_engine
from src.config import DB_URL  

# Create an SQLAlchemy engine that will do the translation from pandas to PostgreSQL
engine = create_engine(DB_URL) # use DB_URL from config.py for connection parameters

def load_function(df):
    """ Load Df into database"""
    if df is not None and not df.empty:
        try:
            df.to_sql('raw_jobs', engine, if_exists='replace', index=False)
            print("Success: Data loaded to PostgreSQL!!!!")
        except Exception as e:
            print(f"Database Error: {e}")
    else:
        print("Avertissement : Le DataFrame est vide, rien à charger.")
        
        
# Test
# if __name__ == "__main__":
#     import pandas as pd
    
#     print("Début du test de connexion...")
#     data_test = pd.DataFrame({
#         'job_title': ['Data Engineer', 'Data Scientist'],
#         'company': ['Test Corp', 'Python Lab']
#     })
    
#     load_function(data_test)