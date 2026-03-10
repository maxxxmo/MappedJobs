# MappedJobs
## Presentation
The goal is to display job offers around Paris in a force directed-graph in a 2D space.
Example :
![Force directed map example](images/force-directed.png)

The data will be from OpenData:
[OpenData reference](https://www.data.gouv.fr/datasets/offres-demploi-de-la-region-ile-de-france)


## Workflow

 1. ***Docker*** to create a ***PostgresQL*** database
 2. Creation of the ingestion script in python to get data from ***API***
 3. Data transforation with ***DBT***
 4. Orchestration of 2. and 3. with ***Airflow***
 5. Interface with streamlit

## 1. Docker-compose for database

First we select last updates of docker-compose and postgresql:

- [Docker compose version](#https://github.com/docker/compose/releases
)
- [Postgresql Version](https://www.postgresql.org/docs/14/app-initdb.html)

Security: I want to create a secured env so i dont want password in plain text. Password will be stored in .env and .env is added to .gitignore

## 2. Postgresql Database
First we install these in our .venv:
- requests -> send HTTP requests (SEND, POST) to the website
- pandas -> transform data
- sqlalchemy --> Object translate df transformation to sql
- psycopg2-binary --> PostgreSQL database adapter for the Python 

Then i add it to requirements:
````pip freeze > requirements.txt```` in terminal

- [sql alchemy](https://docs.sqlalchemy.org/en/20/core/engines.html) : Engine will do the translation between python to postgresql SQL database

With this code we can insert an abritary dataset in the database:
````import requests
import pandas as pd
from sqlalchemy import create_engine

DB_URL = "postgresql://user_admin:password_123@localhost:5432/jobs_database"

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



def test_pipeline():
    # data transformation
    df = pd.DataFrame(data)
    
    try:
        engine = create_engine(DB_URL)
        df.to_sql('raw_jobs', engine, if_exists='replace', index=False)
        print("Sucess!!!!")
    except Exception as e:
        print(f"Error : {e}")

if __name__ == "__main__":
    test_pipeline()
````

## Change of API --> using france travail
[rules](https://francetravail.io/produits-partages/documentation/conditions-dutilisation-api/licence-offres-emploi)
[portal](https://authentification-partenaire.francetravail.io/connexion/XUI/?realm=/partenaire&goto=https://authentification-partenaire.francetravail.io/connexion/oauth2/realms/root/realms/partenaire/authorize?realm%3D/partenaire%26response_type%3Dcode%26client_id%3DPAR_PN109-PEIO_7F2253D7E228B22A08BDA1F09C516F6FEAD81DF6536EB02FA991A34BB38D9BE8%26scope%3Dapplication_PAR_PN109-PEIO%2520email%2520openid%2520peiofront%2520sldng%2520profile%26redirect_uri%3Dhttps://francetravail.io/auth/auth.html%26state%3DnQ3GvTYDaSGZ2J_nYWdahA%26nonce%3D0U4bD9wir7elLGN3jUS2Lg#login/)
[Utilisation](https://francetravail.io/produits-partages/documentation/utilisation-api-france-travail)

Royaume : "https://api.francetravail.io/partenaire/offresdemploi"

## Directories