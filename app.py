import logging
from logging.handlers import RotatingFileHandler

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from config import Config
from logger import setup_logging
from routes.api.user import api_user_blueprint

from routes.auth import auth_blueprint
from routes.api.service import api_service_blueprint
from routes.api.ticket import api_ticket_blueprint
from routes.api.project import api_project_blueprint

from models.ctm_user import CTMUser
from models.user import User
from models.project import Project
from models.project_user import ProjectUser
from models.ticket import Ticket
from models.status import Status

from database import db
from scheduler import check_projects_last_updated, check_tickets_last_updated


db.connect()
db.create_tables([User, CTMUser, Project, ProjectUser, Ticket, Status], safe=True)

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)


# Call the logging setup function after the Flask app is created
setup_logging()

app.config.from_object('config.Config')

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(api_service_blueprint, url_prefix='/api/service')
app.register_blueprint(api_ticket_blueprint, url_prefix='/api/tickets')
app.register_blueprint(api_project_blueprint, url_prefix='/api/projects')
app.register_blueprint(api_user_blueprint, url_prefix='/api/users')

scheduler = BackgroundScheduler()
scheduler.add_job(check_projects_last_updated, 'interval', hours=Config.SCHEDULE_INTERVAL_HOURS)
scheduler.add_job(check_tickets_last_updated, 'interval', hours=Config.SCHEDULE_INTERVAL_HOURS)


if __name__ == "__main__":
    if not app.debug:
        file_handler = RotatingFileHandler('error.log', maxBytes=1024 * 1024 * 100, backupCount=20)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    scheduler.start()

    app.run(
        app.config['HOST'],
        app.config['PORT']
    )

