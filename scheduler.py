import logging
import datetime

from config import Config
from models.project import Project
from services.project import ProjectService
from services.ticket import TicketService


def check_projects_last_updated():
    threshold = datetime.datetime.utcnow() - datetime.timedelta(hours=Config.SCHEDULE_PROJECT_HOURS)
    logging.info(f"Projects last updated more than " + str(Config.SCHEDULE_PROJECT_HOURS) + " hours ago. Updating...")
    ProjectService().sync()


def check_tickets_last_updated():
    threshold = datetime.datetime.utcnow() - datetime.timedelta(hours=Config.SCHEDULE_PROJECT_HOURS)
    for project in Project.select().where(Project.lastUpdated < threshold):
        logging.info(f"Project {project.name} last updated more than " + str(Config.SCHEDULE_TICKET_HOURS) + " hours ago. Updating...")
        TicketService(project.id).sync()