import requests
from src.config import FT_CLIENT_ID, FT_CLIENT_SECRET, TOKEN_URL, API_URL

class FranceTravailClient:
    """Client for interacting with the France Travail API"""
    def __init__(self):
        self.client_id = FT_CLIENT_ID # Ft_CLIENT_ID is the client ID for authentication
        self.client_secret = FT_CLIENT_SECRET # FT_CLIENT_SECRET is the client secret for authentication
        self.token = None # temporary variable to store the access token

    def get_access_token(self):
        """Obtain or refresh access token from France Travail API,
        payload is the body of the POST request to get the token, headers specify content type.
        The function handles the response and extracts the token if successful, otherwise it logs the error."""
        
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'api_offresdemploiv2 o2dso' 
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'} # Headers for the POST request, specifying that the body is form-encoded
        
        try: 
            response = requests.post(TOKEN_URL, data=payload, headers=headers) # Send POST request to get the token
            response.raise_for_status() # Check if the request was successful (status code 200)
            self.token = response.json().get('access_token') # Extract the token from the response JSON
            print("Token récupéré avec succès.")
            return self.token
        except Exception as e:
            print(f"Erreur lors de la récupération du token: {e}")
            return None

    def fetch_offres(self, params=None):
        """Fetch job offers from the API, using the access token for authentication."""
        if not self.token: # if we don't have a token, we need to get one first
            self.get_access_token()
        headers = {'Authorization': f'Bearer {self.token}'} # Use the temporary token (Bearer token) in the Authorization header
        
        try:
            response = requests.get(API_URL, headers=headers, params=params)
            
            if response.status_code == 206: # Partial Content, meaning the response is truncated but we still get some data
                return response.json().get('resultats', [])
            elif response.status_code == 200: # OK, full response received
                return response.json().get('resultats', [])
            else:
                print(f"Erreur API: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Erreur lors du fetch: {e}")
            return []

# Testing
if __name__ == "__main__":
    client = FranceTravailClient()
    offres = client.fetch_offres(params={'motsCles': 'Data Engineer'})
    print(f"Nombre d'offres récupérées : {len(offres)}")