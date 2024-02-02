import datetime
from peewee import CharField, BooleanField, DateTimeField
from models.base import BaseModel


class Project(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    isArchived = BooleanField(null=True)
    lastUpdated = DateTimeField(default=datetime.datetime.utcnow)
