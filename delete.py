import requests
import argparse
from client import fetch_token
import os
from dotenv import load_dotenv

load_dotenv()

project_key = os.getenv("PROJECT_KEY")
api_url_graphql = "https://api.europe-west1.gcp.commercetools.com"

def delete_custom_object(container, key):
    token = fetch_token()
    if not token:
        return

    url = f"{api_url_graphql}/{project_key}/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    query = """
    mutation ($container: String!, $key: String!) {
        deleteCustomObject(container: $container, key: $key) {
            id
            container
            key
        }
    }
    """
    variables = {
        "container": container,
        "key": key
    }
    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Custom object deleted successfully")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Parse command line arguments
parser = argparse.ArgumentParser(description='Delete a custom object by key.')
parser.add_argument('key', type=str, help='The key of the custom object to delete')
args = parser.parse_args()

# Delete the custom object using the specified key
delete_custom_object("voucher-app-form-values", args.key)