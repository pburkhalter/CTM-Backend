import peewee

from database import db


class BaseModel(peewee.Model):
    class Meta:
        database = db
