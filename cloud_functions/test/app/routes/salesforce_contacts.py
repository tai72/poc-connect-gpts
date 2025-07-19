from flask import Blueprint, jsonify, Response
from app.services.salesforce.accounts import (
    get_account_info,
    get_account_metadatas,
    get_account_by_id
)

salesforce_bp = Blueprint('salesforce', __name__)


@salesforce_bp.route('/contacts', methods=['GET'])
def contacts():
    contacts = get_contacts()
    if isinstance(contacts, Response):
        return contacts
    return jsonify({'contacts': contacts})


@salesforce_bp.route('/leads', methods=['GET'])
def leads():
    leads = get_leads()
    if isinstance(leads, Response):
        return leads
    return jsonify({'leads': leads})


@salesforce_bp.route('/query', methods=['GET'])
def query():
    soql = request.args.get('q')
    if not soql:
        return jsonify({'error': 'q parameter is required'}), 400

    records = run_query(soql)
    if isinstance(records, Response):
        return records

    return jsonify({'records': records})
