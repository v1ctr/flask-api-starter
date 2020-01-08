from . import auth_blueprint
from app import db
from app.models import User

from flask import request, jsonify
from werkzeug.exceptions import BadRequest, Unauthorized
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_current_user,
                                create_access_token, create_refresh_token)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        raise BadRequest('must include email and password fields')

    user = User.query.filter_by(email=data['email']).first()
    if user and user.verify_password(data['password']):
        response_data = {
            'access_token': create_access_token(identity=user),
            'refresh_token': create_refresh_token(identity=user)
        }
        return jsonify(response_data), 200

    raise Unauthorized('Bad username or password')


@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user_id = get_jwt_identity()
    response_data = {
        'access_token': create_access_token(identity=current_user_id, fresh=False)
    }
    return jsonify(response_data), 200


@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    if 'email' not in data or 'password' not in data:
        raise BadRequest('must include email and password fields')
    if User.query.filter_by(email=data['email']).first():
        raise BadRequest('please use a different email address')

    new_user = User(data['email'], data['password'])
    db.session.add(new_user)
    db.session.commit()
    response_data = {
        'access_token': create_access_token(identity=new_user),
        'refresh_token': create_refresh_token(identity=new_user)
    }
    return jsonify(response_data), 201
