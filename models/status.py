from peewee import CharField, ForeignKeyField
from models.base import BaseModel
from models.project import Project


class Status(BaseModel):
    id = CharField(primary_key=True)
    name = CharField(null=True)

    project = ForeignKeyField(Project, backref='statuses')


