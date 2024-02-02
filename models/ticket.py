from peewee import CharField, ForeignKeyField, DateTimeField, TextField, IntegerField, BooleanField
from models.base import BaseModel
from models.project import Project
from models.user import User
from models.status import Status


class Ticket(BaseModel):
    id = CharField(primary_key=True)
    ticketNumber = IntegerField(null=True)
    ticketKey = CharField()
    name = CharField(null=True)
    deadline = DateTimeField(null=True)
    createdAt = DateTimeField(null=True)
    description = TextField(null=True)
    cost = IntegerField(null=True)
    hasComments = BooleanField(null=True)
    type = CharField(null=True)
    category = CharField(null=True)

    project = ForeignKeyField(Project, backref='tickets')
    responsible = ForeignKeyField(User, backref='assigned_tickets', null=True)
    status = ForeignKeyField(Status, backref='ticket_status', null=True)


