from flask import Flask
from .routes.customers import customers_bp
from .routes.salesforce_account import salesforce_bp
from .routes.oauth import oauth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # セッション用の秘密鍵（任意のランダム文字列）
    app.secret_key = 'your-random-secret-key-here'  # ここを追加

    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(salesforce_bp, url_prefix='/salesforce')
    app.register_blueprint(oauth_bp)

    return app
