from flask import Blueprint, request, jsonify

from routes.decorator import protected
from services.user import UserService

from exceptions.user import UserSyncException, UserCleanException


api_user_blueprint = Blueprint('user', __name__)


@api_user_blueprint.route('/', methods=['GET'])
@protected
def get_all(current_user):
    try:
        return jsonify(UserService().get_all()), 200
    except UserSyncException as e:
        return jsonify({'error': str(e)}), 400


@api_user_blueprint.route('/company', methods=['GET'])
@protected
def get_teammates(current_user):
    try:
        return jsonify(UserService().get_users_by_email_domain('jhaefliger.ch')), 200
    except UserSyncException as e:
        return jsonify({'error': str(e)}), 400


@api_user_blueprint.route('/external', methods=['GET'])
@protected
def get_excluded(current_user):
    try:
        return jsonify(UserService().get_users_exclude_domain('jhaefliger.ch')), 200
    except UserSyncException as e:
        return jsonify({'error': str(e)}), 400


@api_user_blueprint.route('/<user_id>', methods=['GET'])
@protected
def get_user_by_id(current_user, user_id):
    try:
        return jsonify(UserService().get_by_id(user_id)), 200
    except UserSyncException as e:
        return jsonify({'error': str(e)}), 400




@api_user_blueprint.route('/clean', methods=['GET'])
@protected
def clean(current_user):
    try:
        UserService().clean()
        return jsonify({'message': 'All users successfully cleaned'}), 200
    except UserCleanException as e:
        return jsonify({'error': str(e)}), 400
