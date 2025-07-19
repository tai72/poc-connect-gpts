from flask import redirect, url_for, request
from functools import wraps
from app.routes.oauth import access_token_store


def ensure_salesforce_authenticated(func):
    """
    アクセストークンがあるか確認し、なければOAuth2.0認証によってアクセストークンを取得する
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = access_token_store.get('access_token')
        instance_url = access_token_store.get('instance_url')

        if not access_token or not instance_url:
            print('未認証なので、`oauth.salesforce_login`にリダイレクト')
            return redirect(url_for('oauth.salesforce_login', next=request.path))

        return func(access_token, instance_url, *args, **kwargs)
    return wrapper
