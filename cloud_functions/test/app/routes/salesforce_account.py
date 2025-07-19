from flask import Blueprint, jsonify, Response
from app.services.salesforce.accounts import (
    get_account_info,
    get_account_metadatas,
    get_account_by_id
)

salesforce_bp = Blueprint('salesforce/account', __name__)


@salesforce_bp.route('/accounts', methods=['GET'])
def accounts():
    accounts = get_account_metadatas()

    # 「もしリダイレクトだったら、すぐそのまま返す」
    if isinstance(accounts, Response):
        return accounts

    # 普通にデータだったら、JSONで返す
    return jsonify({'accounts': accounts})


@salesforce_bp.route('/account_info', methods=['GET'])
def account_names():
    accounts = get_account_info()

    # 「もしリダイレクトだったら、すぐそのまま返す」
    if isinstance(accounts, Response):
        return accounts

    # 普通にデータだったら、JSONで返す
    return jsonify({'accounts': accounts})


@salesforce_bp.route('/account/<account_id>', methods=['GET'])
def account_detail(account_id):
    account = get_account_by_id(account_id)
    if isinstance(account, Response):
        return account

    return jsonify(account)


# @salesforce_bp.route('/contacts', methods=['GET'])
# def contacts():
#     contacts = get_contacts()
#     if isinstance(contacts, Response):
#         return contacts
#     return jsonify({'contacts': contacts})


# @salesforce_bp.route('/leads', methods=['GET'])
# def leads():
#     leads = get_leads()
#     if isinstance(leads, Response):
#         return leads
#     return jsonify({'leads': leads})


# @salesforce_bp.route('/query', methods=['GET'])
# def query():
#     soql = request.args.get('q')
#     if not soql:
#         return jsonify({'error': 'q parameter is required'}), 400

#     records = run_query(soql)
#     if isinstance(records, Response):
#         return records

#     return jsonify({'records': records})
