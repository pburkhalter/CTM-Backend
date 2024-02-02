from pprint import pprint

from flask import Blueprint, request, jsonify

from routes.decorator import protected
from services.project import ProjectService

from exceptions.project import ProjectSyncException, ProjectCleanException


api_project_blueprint = Blueprint('project', __name__)


@api_project_blueprint.route('/', methods=['GET'])
@protected
def get_projects(current_user):
    try:
        return jsonify(ProjectService().get_projects()), 200
    except ProjectSyncException as e:
        return jsonify({'error': str(e)}), 400


@api_project_blueprint.route('/', methods=['POST'])
@protected
def post_projects(current_user):
    preferences = request.json
    by_user = preferences.get('user_id')

    try:
        if by_user:
            return jsonify(ProjectService().get_projects(
                user_id=by_user
            )), 200
        else:
            return jsonify(ProjectService().get_projects()), 200
    except ProjectSyncException as e:
        return jsonify({'error': str(e)}), 400


@api_project_blueprint.route('/<project_id>', methods=['GET'])
@protected
def get_project_from_id(current_user, project_id):
    try:
        return jsonify(ProjectService().get_project_by_id(project_id)), 200
    except ProjectSyncException as e:
        return jsonify({'error': str(e)}), 400

@api_project_blueprint.route('/clean', methods=['GET'])
@protected
def clean(current_user):
    try:
        ProjectService().clean()
        return jsonify({'message': 'All projects successfully deleted'}), 200
    except ProjectCleanException as e:
        return jsonify({'error': str(e)}), 400
