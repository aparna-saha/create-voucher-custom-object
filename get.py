import requests
import argparse
from client import fetch_token  # Import the fetch_token function

# Replace with your Commercetools credentials
project_key = "flaconi-dev"
api_url_graphql = "https://api.europe-west1.gcp.commercetools.com"

def get_custom_object_by_id(custom_object_id):
    token = fetch_token()
    if not token:
        return

    url = f"{api_url_graphql}/{project_key}/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    query = """
    query ($id: String!) {
        customObject(id: $id) {
            id
            container
            key
            value
        }
    }
    """
    variables = {
        "id": custom_object_id
    }
    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        custom_object = response.json().get("data", {}).get("customObject")
        if custom_object:
            print(f"Custom Object {custom_object['id']} retrieved successfully: {custom_object['value']}")
            return custom_object
        else:
            print("Custom object not found.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Parse command line arguments
parser = argparse.ArgumentParser(description='Retrieve a custom object by ID.')
parser.add_argument('custom_object_id', type=str, help='The ID of the custom object to retrieve')
args = parser.parse_args()

# Retrieve the custom object using the specified ID
get_custom_object_by_id(args.custom_object_id)