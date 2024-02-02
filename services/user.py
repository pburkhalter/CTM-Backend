from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict

from capmo.user import CapmoUserClient
from models.project import Project
from models.project_user import ProjectUser
from models.user import User

from exceptions.user import UserCleanException, UserFetchException


class UserService:
    def __init__(self):
        self.client = CapmoUserClient()

    def get_by_id(self, user_id):
        try:
            user = User.select().where(User.id == user_id).execute()
            return user
        except IntegrityError as e:
            raise UserFetchException(f"Database error occurred: {e}")
        except Exception as e:
            raise UserFetchException(f"An error occurred: {e}")

    def get_all(self):
        try:
            users = User.select()
            results = [model_to_dict(user) for user in users]
            return results
        except IntegrityError as e:
            raise UserFetchException(f"Database error occurred: {e}")
        except Exception as e:
            raise UserFetchException(f"An error occurred: {e}")

    from peewee import fn

    def get_users_by_email_domain(self, domain):
        try:
            # Query to find users with the specified email domain
            users_query = User.select().where(User.email.contains(f"@{domain}"))

            # Convert user models to dictionaries
            users_data = [model_to_dict(user, recurse=False) for user in users_query]

            return users_data

        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def get_users_exclude_domain(self, excluded_domain):
        try:
            # Query to find users whose email does not contain the specified domain
            users_query = User.select().where(~User.email.contains(f"@{excluded_domain}"))

            # Convert user models to dictionaries
            users_data = [model_to_dict(user, recurse=False) for user in users_query]

            return users_data

        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def get_users_in_projects_of_user(self, user_id):
        try:
            # Step 1: Find all projects associated with the given user
            projects_query = (Project
                              .select()
                              .join(ProjectUser)
                              .where(ProjectUser.user_id == user_id))

            projects_data = []
            for project in projects_query:
                # Convert project model to dictionary
                project_dict = model_to_dict(project, recurse=False)

                # Step 2: For each project, find all users (teammates) associated with this project
                teammates_query = (User
                                   .select()
                                   .join(ProjectUser)
                                   .where(ProjectUser.project_id == project.id)
                                   .distinct())

                # Convert user models to dictionaries
                project_dict['teammates'] = [model_to_dict(user, recurse=False) for user in teammates_query]

                projects_data.append(project_dict)

            return projects_data

        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def count(self):
        return User.select().count()

    def clean(self):
        try:
            User.delete().execute()
        except IntegrityError as e:
            raise UserCleanException(f"Database error occurred: {e}")
        except Exception as e:
            raise UserCleanException(f"An error occurred: {e}")
