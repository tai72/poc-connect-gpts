from flask import Blueprint, jsonify, Response
from app.services.salesforce.opportunities import (
    get_opportunities,
    get_opportunity_by_id
)

salesforce_opportunity_bp = Blueprint('salesforce/opportunity', __name__)


@salesforce_opportunity_bp.route('/list', methods=['GET'])
def opportunities():
    accounts = get_opportunities()

    # 「もしリダイレクトだったら、すぐそのまま返す」
    if isinstance(accounts, Response):
        return accounts

    return jsonify({'opportunities': accounts})


@salesforce_opportunity_bp.route('/detail/<opportunity_id>', methods=['GET'])
def detail(opportunity_id):
    opportunity = get_opportunity_by_id(opportunity_id)

    # 「もしリダイレクトだったら、すぐそのまま返す」
    if isinstance(opportunity, Response):
        return opportunity

    # 普通にデータだったら、JSONで返す
    return jsonify({'opportunity': opportunity})
