from flask import request, jsonify
from functools import wraps
import jwt
from config import Config
from models.ctm_user import CTMUser
from models.user import User


def protected(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'A valid token is missing'}), 403

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = CTMUser.get(CTMUser.id == payload['sub'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401  # Token is expired
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return jsonify({'message': 'Invalid token'}), 401  # Invalid token

        return f(current_user, *args, **kwargs)

    return decorated_function
