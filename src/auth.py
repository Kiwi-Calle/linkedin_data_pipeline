import requests
import os

TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

def get_access_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET")
    }
    response = requests.post(TOKEN_URL, data=data)
    return response.json().get("access_token")
