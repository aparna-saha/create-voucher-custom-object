import requests
import json
import os
import argparse
from dotenv import load_dotenv
from client import fetch_token

load_dotenv()

project_key = os.getenv("PROJECT_KEY")
api_url_graphql = "https://api.europe-west1.gcp.commercetools.com"

def custom_object_exists(container, key, context):
    token = fetch_token()
    if not token:
        return False

    url = f"{api_url_graphql}/{project_key}/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    query = """
    query ($container: String!, $key: String!) {
        customObject(container: $container, key: $key) {
            id
            container
            key
            value
        }
    }
    """
    variables = {
        "container": container,
        "key": key
    }
    payload = {
        "query": query,
        "variables": variables,
        "context": context  # Add context to the payload
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("data", {}).get("customObject") is not None
    else:
        print(f"Error checking custom object: {response.status_code} - {response.text}")
        return False

def create_custom_object_graphql(container, key, value, context):
    if custom_object_exists(container, key, context):
        print(f"Custom object with key '{key}' in container '{container}' already exists.")
        return

    token = fetch_token()
    if not token:
        return

    url = f"{api_url_graphql}/{project_key}/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    query = """
    mutation ($container: String!, $key: String!, $value: String!) {
        createOrUpdateCustomObject(draft: {container: $container, key: $key, value: $value}) {
            id
            container
            key
            value
        }
    }
    """
    variables = {
        "container": container,
        "key": key,
        "value": json.dumps(value)  # Convert value to JSON string
    }
    payload = {
        "query": query,
        "variables": variables,
        "context": context  # Add context to the payload
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        custom_object = data.get("data", {}).get("createOrUpdateCustomObject")
        if custom_object:
            print(f"Custom object created successfully with ID: {custom_object['id']}")
        else:
            print("Custom object creation failed.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Parse command line arguments
parser = argparse.ArgumentParser(description='Create a custom object from a JSON file.')
parser.add_argument('filename', type=str, help='The JSON file to read data from')
args = parser.parse_args()

# Read data from the specified JSON file
with open(args.filename, 'r') as file:
    data = json.load(file)

voucher_code = data['formValues']['voucherCode']
form_values = data['formValues']

create_custom_object_graphql("voucher-app-form-values", voucher_code, data, "ctp")