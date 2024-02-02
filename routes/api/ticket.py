from pprint import pprint

from flask import Blueprint, request, jsonify

from routes.decorator import protected
from services.ticket import TicketService
from exceptions.ticket import TicketSyncException, TicketCleanException, TicketFetchException

api_ticket_blueprint = Blueprint('ticket', __name__)


@api_ticket_blueprint.route('/<ticket_id>', methods=['GET'])
@protected
def post_ticket_by_id(current_user, ticket_id):
    preferences = request.json
    ticket_id = preferences.get('ticket_id')

    try:
        if ticket_id:
            return jsonify(TicketService().get_ticket_by_id(ticket_id)), 200
        else:
            return jsonify(TicketService().get_tickets()), 200
    except TicketSyncException as e:
        return jsonify({'error': str(e)}), 400


@api_ticket_blueprint.route('/', methods=['POST'])
@protected
def create_ticket(current_user):
    ticket_data = request.json
    pprint(ticket_data)

    project_id = ticket_data['projectId']
    name = ticket_data['name']
    description = ticket_data['description']
    responsible_id = ticket_data['responsibleId']
    status_id = ticket_data['statusId']
    deadline = ticket_data['deadline']

    try:
        ticket_service = TicketService()
        new_ticket = ticket_service.create_ticket(
            project_id=project_id,
            name=name,
            description=description,
            responsible_id=responsible_id,
            status_id=status_id,
            deadline=deadline
        )
        return jsonify(new_ticket), 201
    except TicketSyncException as e:
        return jsonify({'error': str(e)}), 400


@api_ticket_blueprint.route('/<ticket_id>', methods=['PUT'])
@protected
def update_ticket(current_user, ticket_id):
    update_data = request.json

    try:
        ticket_service = TicketService()
        updated_ticket = ticket_service.update_ticket(ticket_id, update_data)
        return jsonify(updated_ticket), 200
    except TicketFetchException as e:
        return jsonify({'error': str(e)}), 404
    except TicketSyncException as e:
        return jsonify({'error': str(e)}), 400


@api_ticket_blueprint.route('/clean', methods=['GET'])
@protected
def clean(current_user):
    try:
        TicketService().clean()
        return jsonify({'message': 'All tickets successfully cleaned'}), 200
    except TicketCleanException as e:
        return jsonify({'error': str(e)}), 400
