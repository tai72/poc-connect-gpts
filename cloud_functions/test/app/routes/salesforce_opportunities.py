from flask import request, Blueprint, jsonify, Response
from app.services.salesforce.opportunities import (
    get_opportunities,
    get_opportunity_by_id,
    create_opportunity,
    delete_opportunity
)

salesforce_opportunity_bp = Blueprint('salesforce/opportunity', __name__)


@salesforce_opportunity_bp.route('/list', methods=['GET'])
def opportunities():
    accounts = get_opportunities()

    # 「もしリダイレクトだったら、すぐそのまま返す」
    if isinstance(accounts, Response):
        return accounts

    return jsonify({'opportunities': accounts})


@salesforce_opportunity_bp.route('/<opportunity_id>', methods=['GET'])
def detail(opportunity_id):
    opportunity = get_opportunity_by_id(opportunity_id)

    # 「もしリダイレクトだったら、すぐそのまま返す」
    if isinstance(opportunity, Response):
        return opportunity

    # 普通にデータだったら、JSONで返す
    return jsonify({'opportunity': opportunity})


@salesforce_opportunity_bp.route('/create', methods=['POST'])
def create():
    data = request.json  # POSTされたJSON
    name = data.get('name')
    stage_name = data.get('stage_name')
    close_date = data.get('close_date')
    amount = data.get('amount')

    result = create_opportunity(
        name=name,
        stage_name=stage_name,
        close_date=close_date,
        amount=amount
    )

    # Salesforceから正常に返ったものをJSONで返却
    return jsonify(result)


@salesforce_opportunity_bp.route('/delete/<opportunity_id>', methods=['DELETE'])
def delete_opportunity_route(opportunity_id):
    result = delete_opportunity(opportunity_id)
    if isinstance(result, Response):
        return result
    return jsonify(result)
