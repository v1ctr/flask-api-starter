from . import main_blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required


@main_blueprint.route('/public')
def public():
    response_data = {
        'success': True
    }
    return jsonify(response_data), 200


@main_blueprint.route('/private')
@jwt_required
def private():
    response_data = {
        'success': True
    }
    return jsonify(response_data), 200
