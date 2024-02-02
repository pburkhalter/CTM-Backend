class UserAlreadyExistsException(Exception):
    pass


class AuthenticationException(Exception):
    pass


class TokenRefreshException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class PasswordUpdateException(Exception):
    pass
