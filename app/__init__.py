import uuid
from flask import Flask, json, jsonify
from werkzeug.exceptions import HTTPException, Unauthorized
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import config

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    initialize_extensions(app)
    initialize_errorhandlers(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main_blueprint
    from .auth import auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # SQLAlchemy models
    from .models import User

    # Flask-JWT-Extended configuration
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        user_id = None
        if isinstance(user, User):
            user_id = user.get_id()
        if isinstance(user, str):
            user_id = user
        return user_id

    @jwt.expired_token_loader
    def expired_token_loader(token):
        return jsonify({
            "code": 401,
            "name": "Unauthorized",
            "description": "Token has expired"
        }), 401

    @jwt.unauthorized_loader
    def unauthorized_loader(msg):
        return jsonify({
            "code": 401,
            "name": "Unauthorized",
            "description": msg
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_loader(msg):
        return jsonify({
            "code": 422,
            "name": "Unprocessable Entity",
            "description": msg
        }), 422

    @jwt.user_loader_callback_loader
    def load_user_from_token(user_id):
        user = User.query.filter_by(id=uuid.UUID(user_id)).first()
        return user if user else None


def initialize_errorhandlers(app):

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

