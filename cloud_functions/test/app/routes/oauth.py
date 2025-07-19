from flask import Blueprint, redirect, request, current_app, jsonify
import requests
import secrets
import hashlib
import base64
from flask import session  # セッションで code_verifier 保管

oauth_bp = Blueprint('oauth', __name__)

# 一時保存（本来はDBやRedis）
access_token_store = {}


# PKCE用
def generate_code_verifier():
    return secrets.token_urlsafe(64)


def generate_code_challenge(code_verifier):
    digest = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')


@oauth_bp.route('/salesforce/login')
def salesforce_login():
    code_verifier = generate_code_verifier()
    session['code_verifier'] = code_verifier  # 後で使うため保存
    code_challenge = generate_code_challenge(code_verifier)

    # 元ページ覚える（nextパラメータを受け取る）
    next_url = request.args.get('next', '/')

    params = {
        'response_type': 'code',
        'client_id': current_app.config['SF_CLIENT_ID'],
        'redirect_uri': current_app.config['SF_REDIRECT_URI'],
        'scope': 'api',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
        'state': next_url
    }
    url = current_app.config['SF_AUTH_URL']
    full_url = requests.Request('POST', url, params=params).prepare().url

    print('リダイレクト', full_url)

    return redirect(full_url)


@oauth_bp.route('/oauth/callback')
def oauth_callback():
    code = request.args.get('code')
    code_verifier = session.get('code_verifier')

    print('code', code)

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': current_app.config['SF_CLIENT_ID'],
        'client_secret': current_app.config['SF_CLIENT_SECRET'],
        'redirect_uri': current_app.config['SF_REDIRECT_URI'],
        'code_verifier': code_verifier
    }

    response = requests.post(current_app.config['SF_TOKEN_URL'], data=data)

    print(response.text)

    response.raise_for_status()

    token_info = response.json()
    access_token_store['access_token'] = token_info['access_token']
    access_token_store['instance_url'] = token_info['instance_url']

    print('認証成功')
    print('リダイレクト先:', request.args)

    next_url = request.args.get('state', '/')
    return redirect(next_url)
