# routes/auth.py
from pprint import pprint

from flask import Blueprint, request, jsonify

from models.user import User
from services.auth import AuthService
from exceptions.auth import (UserAlreadyExistsException, AuthenticationException,
                            TokenRefreshException, UserNotFoundException, PasswordUpdateException)

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        AuthService.register_user(data['email'], data['password'])
        return jsonify({'message': 'User created successfully.'}), 201
    except UserAlreadyExistsException as e:
        return jsonify({'error': str(e)}), 400


@auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        response = AuthService.login_user(data['email'], data['password'])
        return jsonify(response), 200
    except AuthenticationException as e:
        return jsonify({'error': str(e)}), 401


@auth_blueprint.route('/refresh', methods=['POST'])
def refresh():
    try:
        data = request.json
        refresh_token = data.get('refreshToken')
        if not refresh_token:
            raise TokenRefreshException('Refresh token is required')
        response = AuthService.refresh_access_token(refresh_token)
        return jsonify(response), 200
    except TokenRefreshException as e:
        return jsonify({'error': str(e)}), 401


@auth_blueprint.route('/change-password', methods=['POST'])
def change_password():
    try:
        data = request.json
        AuthService.change_password(data['username'], data['old_password'], data['new_password'])
        return jsonify({'message': 'Password updated successfully'}), 200
    except UserNotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except PasswordUpdateException as e:
        return jsonify({'error': str(e)}), 400
