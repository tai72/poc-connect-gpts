import requests
from app.services.salesforce.base import ensure_salesforce_authenticated


@ensure_salesforce_authenticated
def get_opportunities(access_token, instance_url):
    url = f"{instance_url}/services/data/v64.0/sobjects/Opportunity"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response.json()


@ensure_salesforce_authenticated
def get_opportunity_by_id(access_token, instance_url, opportunity_id):
    url = f"{instance_url}/services/data/v64.0/sobjects/Opportunity/{opportunity_id}"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    account = response.json()
    return account
