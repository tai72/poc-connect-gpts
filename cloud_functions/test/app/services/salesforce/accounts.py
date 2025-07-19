from flask import redirect, url_for, request
import requests
from app.routes.oauth import access_token_store
from app.services.salesforce.base import ensure_salesforce_authenticated


@ensure_salesforce_authenticated
def get_account_metadatas(access_token, instance_url):
    url = f"{instance_url}/services/data/v64.0/sobjects/Account/describe"
    url = f"{instance_url}/services/data/v64.0/sobjects/Account/listviews"
    url = f"{instance_url}/services/data/v64.0/sobjects/Account"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response.json()


@ensure_salesforce_authenticated
def get_account_info(access_token, instance_url):
    # Id, Name, Phone を取得
    soql = "SELECT Id, Name, Phone FROM Account"
    url = f"{instance_url}/services/data/v64.0/query?q={soql}"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    response.raise_for_status()

    # 必要なフィールドを辞書で返す
    return [
        {
            'Id': record.get('Id'),
            'Name': record.get('Name'),
            'Phone': record.get('Phone')
        }
        for record in response.json().get('records', [])
    ]


@ensure_salesforce_authenticated
def get_account_by_id(access_token, instance_url, account_id):
    access_token = access_token_store.get('access_token')
    instance_url = access_token_store.get('instance_url')

    if not access_token or not instance_url:
        return redirect(url_for('oauth.salesforce_login', next=request.full_path))

    url = f"{instance_url}/services/data/v64.0/sobjects/Account/{account_id}"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    account = response.json()
    return account
    # return {'id': account.get('Id'), 'name': account.get('Name')}


# def get_contacts():
#     access_token = access_token_store.get('access_token')
#     instance_url = access_token_store.get('instance_url')

#     if not access_token or not instance_url:
#         print('未認証なので、`oauth.salesforce_login`にリダイレクト')
#         return redirect(url_for('oauth.salesforce_login', next=request.path))

#     url = f"{instance_url}/services/data/v64.0/query?q=SELECT+Name+FROM+Contact"
#     headers = {'Authorization': f'Bearer {access_token}'}
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()

#     return [record['Name'] for record in response.json().get('records', [])]


# def get_leads():
#     access_token = access_token_store.get('access_token')
#     instance_url = access_token_store.get('instance_url')

#     if not access_token or not instance_url:
#         print('未認証なので、`oauth.salesforce_login`にリダイレクト')
#         return redirect(url_for('oauth.salesforce_login', next=request.path))

#     url = f"{instance_url}/services/data/v64.0/query?q=SELECT+Name+FROM+Lead"
#     headers = {'Authorization': f'Bearer {access_token}'}
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()

#     return [record['Name'] for record in response.json().get('records', [])]


# def run_query(soql_query):
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
