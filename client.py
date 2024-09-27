import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
project_id = os.getenv("PROJECT_KEY")
auth_url = "https://auth.europe-west1.gcp.commercetools.com/oauth/token"

scopes = [
    f"manage_products:{project_id}",
    f"manage_categories:{project_id}",
    f"view_key_value_documents:{project_id}",
    f"view_project_settings:{project_id}",
    f"view_stores:{project_id}"
]

scope = " ".join(scopes)

class TokenSingleton:
    _instance = None
    _token = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenSingleton, cls).__new__(cls)
            cls._instance._fetch_token()
        return cls._instance

    def _fetch_token(self):
        data = {
            "grant_type": "client_credentials",
            "scope": scope
        }
        response = requests.post(auth_url, data=data, auth=HTTPBasicAuth(client_id, client_secret))
        if response.status_code == 200:
            self._token = response.json().get("access_token")
        else:
            print(f"Error fetching token: {response.status_code} - {response.text}")

    @property
    def token(self):
        return self._token

def fetch_token():
    singleton = TokenSingleton()
    return singleton.token