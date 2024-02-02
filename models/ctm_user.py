from peewee import CharField
from flask_bcrypt import generate_password_hash, check_password_hash

from models.base import BaseModel


class CTMUser(BaseModel):
    email = CharField(unique=True)
    password_hash = CharField()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
