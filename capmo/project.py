from capmo.gqlclient.gqlclient import GraphQLClient
from capmo.queries.project import GET_PROJECTS_QUERY, GET_PROJECT_ATTRIBUTES_QUERY, GET_PROJECT_MEMBERS_QUERY, \
    GET_PROJECT_SETTINGS_QUERY


class CapmoProjectClient(GraphQLClient):

    def __init__(self):
        super().__init__()

    def get_projects(self):
        statement = GET_PROJECTS_QUERY

        variables = {"input": {"after": None, "limit": 100, "isArchived": False}}
        return self.exec(statement=statement, variables=variables)

    def get_project_attributes(self, project):
        statement = GET_PROJECT_ATTRIBUTES_QUERY

        variables = {"input": {"projectId": project}}
        return self.exec(statement=statement, variables=variables)

    def get_project_members(self, project_id):
        statement = GET_PROJECT_MEMBERS_QUERY

        variables = {
            "input": {
                "projectId": project_id
            }
        }

        return self.exec(statement=statement, variables=variables)

    def get_project_settings(self, project_id):
        statement = GET_PROJECT_SETTINGS_QUERY

        variables = {
            "projectInput": {
                "projectId": project_id
            }
        }

        return self.exec(statement=statement, variables=variables)