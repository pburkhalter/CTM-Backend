from peewee import ForeignKeyField, ManyToManyField, CompositeKey
from models.base import BaseModel
from models.project import Project
from models.user import User


class ProjectUser(BaseModel):
    project = ForeignKeyField(Project, backref='users')
    user = ForeignKeyField(User, backref='projects')

    class Meta:
        primary_key = CompositeKey('project', 'user')


Project.users = ManyToManyField(User, backref='projects', through_model=ProjectUser)
