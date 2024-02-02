from peewee import IntegrityError, prefetch

from playhouse.shortcuts import model_to_dict

from capmo.project import CapmoProjectClient
from models.project import Project
from exceptions.project import ProjectSyncException, ProjectCleanException, ProjectFetchException
from models.project_user import ProjectUser
from models.status import Status
from models.ticket import Ticket
from models.user import User


class ProjectService:
    def __init__(self):
        self.client = CapmoProjectClient()

    def sync(self):
        try:
            gql_data = self.client.get_projects()
            gql_projects = gql_data['items']
            gql_project_ids = {project['id'] for project in gql_projects}

            with Project._meta.database.atomic():
                for gql_project in gql_projects:
                    project, created = Project.get_or_create(id=gql_project['id'], defaults={
                        'name': gql_project['name'],
                        'isArchived': gql_project['isArchived']
                    })

                    if not created:
                        project.name = gql_project['name']
                        project.isArchived = gql_project['isArchived']
                        project.save()

                    self._sync_project_attributes(project)

                # Delete projects that are not in the GraphQL data
                Project.delete().where(Project.id.not_in(gql_project_ids)).execute()
        except IntegrityError as e:
            raise ProjectSyncException(f"Database error occurred: {e}")
        except Exception as e:
            raise ProjectSyncException(f"An error occurred: {e}")

    def _sync_project_attributes(self, project):
        attributes = self.client.get_project_attributes(project.id)

        # Sync ticket statuses
        for status in attributes.get('ticketStatuses', []):
            status_data, created = Status.get_or_create(id=status['id'], defaults={
                'name': status['name'],
                'project': project.id
            })

            if not created:
                if status_data.name != status['name']:
                    status_data.name = status['name']
                    status_data.save()

        # Sync project members
        for member in attributes.get('members', []):
            user_info = member['user']
            member_data, created = User.get_or_create(id=user_info['id'], defaults={
                'fullName': user_info['fullName'],
                'email': user_info['email']
            })

            if not created:
                update_fields = []
                if member_data.fullName != user_info['fullName']:
                    member_data.fullName = user_info['fullName']
                    update_fields.append(User.fullName)
                if member_data.email != user_info['email']:
                    member_data.email = user_info['email']
                    update_fields.append(User.email)
                if update_fields:
                    member_data.save(only=update_fields)

            # Create or update ProjectUser
            project_user, created = ProjectUser.get_or_create(project=project, user=member_data)
            if not created:
                pass
                # Update project_user if necessary
                # e.g., project_user.some_field = some_new_value
                # project_user.save()  # Only save if there are changes

    def _sync_project_settings(self):
        pass

    def clean(self):
        try:
            Project.delete().execute()
        except IntegrityError as e:
            raise ProjectCleanException(f"Database error occurred: {e}")
        except Exception as e:
            raise ProjectCleanException(f"An error occurred: {e}")

    def get_project_by_id(self, project_id):
        try:
            # Fetch the project
            project = Project.get(Project.id == project_id)

            # Convert project to dict
            project_dict = model_to_dict(project)

            # Fetch related tickets
            tickets = Ticket.select().where(Ticket.project == project)

            # Convert tickets to dict and add to project data
            project_dict['tickets'] = [model_to_dict(ticket) for ticket in tickets]

            return project_dict
        except Project.DoesNotExist:
            raise ProjectFetchException(f"No project found with ID: {project_id}")
        except IntegrityError as e:
            raise ProjectFetchException(f"Database error occurred: {e}")
        except Exception as e:
            raise ProjectFetchException(f"An error occurred: {e}")

    def get_projects(self, user_id=None):
        # Fetch projects
        if user_id is not None:
            projects_query = (Project
                              .select()
                              .join(ProjectUser)
                              .where(ProjectUser.user == user_id)
                              .distinct())
        else:
            projects_query = Project.select().distinct()

        # Fetch related tickets and statuses
        tickets_query = Ticket.select().join(Project)
        statuses_query = Status.select().join(Project)

        # Prefetch related data
        projects_with_related_data = prefetch(
            projects_query,
            tickets_query, statuses_query)

        projects = []
        for project in projects_with_related_data:

            # Fetch members
            members_query = (User
                             .select(User.id, User.fullName)
                             .join(ProjectUser)
                             .where(ProjectUser.project == project))
            members = [{
                'id': member.id,
                'fullName': member.fullName
            } for member in members_query]

            # Modify statuses to include ticket counts
            statuses = []
            for status in project.statuses:
                count = Ticket.select().where(
                    (Ticket.project == project) & (Ticket.status == status)
                ).count()
                statuses.append({
                    'id': status.id,
                    'name': status.name,
                    'ticket_count': count  # Include ticket count here
                })

            # Process tickets
            tickets = [{
                'id': ticket.id,
                'description': ticket.description,
                'cost': ticket.cost,
                'deadline': ticket.deadline,
                'ticketKey': ticket.ticketKey,
                'ticketNumber': ticket.ticketNumber,
                'name': ticket.name,
                'status': {
                    'id': ticket.status.id,
                    'name': ticket.status.name
                } if ticket.status else [],
                'responsible': {
                    'id': ticket.responsible.id,
                    'fullName': ticket.responsible.fullName
                } if ticket.responsible else {}
            } for ticket in project.tickets]

            # Construct project information
            project_info = {
                'id': project.id,
                'name': project.name,
                'tickets': tickets,
                'members': members,
                'statuses': statuses,
                'isArchived': project.isArchived
            }
            projects.append(project_info)

        return projects

    def count(self):
        return Project.select().count()
