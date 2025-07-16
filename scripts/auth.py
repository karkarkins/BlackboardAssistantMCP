import requests
import os
from dotenv import load_dotenv

load_dotenv()

BB_BASE_URL = os.getenv("BB_BASE_URL")
BB_CLIENT_ID = os.getenv("BB_CLIENT_ID")
BB_CLIENT_SECRET = os.getenv("BB_CLIENT_SECRET")

def get_access_token():
    url = f"{BB_BASE_URL}/learn/api/public/v1/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
    }
    response = requests.post(url, headers=headers, auth=(BB_CLIENT_ID, BB_CLIENT_SECRET), data=data)
    response.raise_for_status()
    return response.json()["access_token"]