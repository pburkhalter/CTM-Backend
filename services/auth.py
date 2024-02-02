import datetime
import jwt
from peewee import IntegrityError

from config import Config
from models.ctm_user import CTMUser

from exceptions.auth import (UserAlreadyExistsException, AuthenticationException,
                                 TokenRefreshException, UserNotFoundException, PasswordUpdateException)
from models.user import User


class AuthService:
    @staticmethod
    def register_user(email, password):
        try:
            user = CTMUser()
            user.email = email
            user.set_password(password)
            user.save()
        except IntegrityError:
            raise UserAlreadyExistsException('Username already taken')

    @staticmethod
    def login_user(email, password):
        try:
            ctm_user = CTMUser.get(CTMUser.email == email)
            if ctm_user.check_password(password):

                access_token = jwt.encode({
                    'sub': ctm_user.id,
                    'iat': datetime.datetime.utcnow(),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365)
                }, Config.SECRET_KEY, algorithm='HS256')

                refresh_token = jwt.encode({
                    'sub': ctm_user.id,
                    'iat': datetime.datetime.utcnow(),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3650)
                }, Config.REFRESH_SECRET_KEY, algorithm='HS256')

                user = User.get_or_none(User.email == email)

                user_id = ''
                user_full_name = ''

                if user:
                    user_id = user.id
                    user_full_name = user.fullName

                return {
                    'accessToken': access_token,
                    'refreshToken': refresh_token,
                    'email': ctm_user.email,
                    'id': user_id,
                    'fullName': user_full_name
                }
            else:
                raise AuthenticationException('Invalid email or password')
        except CTMUser.DoesNotExist:
            raise AuthenticationException('Invalid email or password')

    @staticmethod
    def logout_user(username, password):
        pass

    @staticmethod
    def refresh_access_token(refresh_token):
        try:
            payload = jwt.decode(refresh_token, Config.REFRESH_SECRET_KEY, algorithms=['HS256'])
            user_id = payload['sub']

            access_token = jwt.encode({
                'sub': user_id,
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, Config.SECRET_KEY, algorithm='HS256')

            refresh_token = jwt.encode({
                'sub': user_id,
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
            }, Config.SECRET_KEY, algorithm='HS256')

            return {
                'accessToken': access_token,
                'refreshToken': refresh_token,
            }
        except jwt.ExpiredSignatureError:
            raise TokenRefreshException("Refresh token expired")
        except (jwt.InvalidTokenError, CTMUser.DoesNotExist):
            raise TokenRefreshException("Invalid refresh token")

    @staticmethod
    def change_password(username, old_password, new_password):
        try:
            user = CTMUser.get(CTMUser.username == username)
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
            else:
                raise PasswordUpdateException('Invalid current password')
        except CTMUser.DoesNotExist:
            raise UserNotFoundException('User not found')
