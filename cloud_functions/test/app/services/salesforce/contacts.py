from flask import redirect, url_for, request
import requests
from app.routes.oauth import access_token_store
from app.services.salesforce.base import ensure_salesforce_authenticated


@ensure_salesforce_authenticated
def get_contacts(access_token, instance_url):
    url = f"{instance_url}/services/data/v64.0/query?q=SELECT+Name+FROM+Contact"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return [record['Name'] for record in response.json().get('records', [])]


@ensure_salesforce_authenticated
def get_leads(access_token, instance_url):
    access_token = access_token_store.get('access_token')
    instance_url = access_token_store.get('instance_url')

    if not access_token or not instance_url:
        print('未認証なので、`oauth.salesforce_login`にリダイレクト')
        return redirect(url_for('oauth.salesforce_login', next=request.path))

    url = f"{instance_url}/services/data/v64.0/query?q=SELECT+Name+FROM+Lead"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return [record['Name'] for record in response.json().get('records', [])]


# @ensure_salesforce_authenticated
# def run_query(access_token, instance_url, soql_query):
#     access_token = access_token_store.get('access_token')
#     instance_url = access_token_store.get('instance_url')

#     if not access_token or not instance_url:
#         print('未認証なので、`oauth.salesforce_login`にリダイレクト')
#         return redirect(url_for('oauth.salesforce_login', next=request.full_path))

#     url = f"{instance_url}/services/data/v64.0/query?q={soql_query}"
#     headers = {'Authorization': f'Bearer {access_token}'}
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()

#     return response.json().get('records', [])
