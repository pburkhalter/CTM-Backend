from peewee import CharField, TextField

from models.base import BaseModel


class User(BaseModel):
    id = CharField(primary_key=True)
    fullName = CharField(null=True)
    email = TextField(null=True)  # Making email optional
