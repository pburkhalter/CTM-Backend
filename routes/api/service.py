import logging
from pprint import pprint

from flask import Blueprint, jsonify, request
import os

from config import Config
from models.project import Project
from routes.decorator import protected
from services.project import ProjectService
from services.ticket import TicketService

from exceptions.project import ProjectSyncException
from exceptions.ticket import TicketSyncException


api_service_blueprint = Blueprint('service', __name__)


@api_service_blueprint.route('/init', methods=['GET'])
@protected
def init(current_user):
    # Check if the lock file exists
    if os.path.exists(Config.LOCK_FILE_PATH):
        return jsonify({'error': 'Service is busy'}), 503  # 503 Service Unavailable

    try:
        # Create a lock file
        with open(Config.LOCK_FILE_PATH, 'w') as lock_file:
            lock_file.write('locked')

        ps = ProjectService()
        ps.sync()
        for project in Project.select():
            logging.debug("Fetching Tickets for Project: " + project.name + "(ID: +" + project.id + ")")
            TicketService(project.id).sync()

        return jsonify({'projects': ps.count(), 'tickets': 0}), 200

    except (ProjectSyncException, TicketSyncException) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    finally:
        if os.path.exists(Config.LOCK_FILE_PATH):
            os.remove(Config.LOCK_FILE_PATH)


@api_service_blueprint.route('/stats', methods=['GET'])
@protected
def info(current_user):
    try:
        ps = ProjectService()
        ts = TicketService()

        data = {
            'info': {
                'version': {
                    'major': Config.VERSION_MAJOR,
                    'minor': Config.VERSION_MINOR,
                    'patch': Config.VERSION_PATCH,
                    'status': Config.VERSION_RELEASE
                },
                'project_count': ps.count(),
                'ticket_count': ts.count()
            }
        }

        return jsonify(data), 200
    except ProjectSyncException as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

