from capmo.gqlclient.gqlclient import GraphQLClient
from capmo.queries.ticket import GET_TICKETS_QUERY, CREATE_TICKET_QUERY, UPDATE_TICKET_QUERY, \
    UPDATE_TICKET_STATUS_QUERY, DELETE_TICKET_QUERY


class CapmoTicketClient(GraphQLClient):

    def __init__(self, project_id=None):
        super().__init__()

        self.project_id = project_id

    def get_tickets(self, project_id=None):
        project_id = project_id or self.project_id
        statement = GET_TICKETS_QUERY

        variables = {
            'input': {
                'after': None,
                'filters': {},
                'orderDirection': 'asc',
                'limit': 100,
                'orderBy': 'ticketNumber',
                'projectId': project_id
            }
        }

        return self.exec(statement=statement, variables=variables)

    def create_ticket(self, project_id, ticket_name, ticket_description, responsible_id, deadline, status_id=None, company_id=None, category_id=None, type_id=None):
        project_id = project_id or self.project_id
        statement = CREATE_TICKET_QUERY

        variables = {
            "input": {
                "projectId": project_id,
                "ticket": {
                    "attachments": [],
                    "name": ticket_name,
                    "description": ticket_description,
                    "categoryId": category_id,
                    "companyId": company_id,
                    "responsibleId": responsible_id,
                    "typeId": None,
                    "deadline": deadline,
                    "statusId": status_id
                }
            }
        }

        return self.exec(statement=statement, variables=variables)

    def update_ticket(self, ticket_id, name, description, status_id, company_id, responsible_id, deadline, category_id=None, type_id=None, location=None, cost=None):
        statement = UPDATE_TICKET_QUERY

        variables = {
            "input": {
                "ticketId": ticket_id,
                "ticket": {
                    "attachments": [],  # Assuming no attachments for now
                    "name": name,
                    "description": description,
                    "statusId": status_id,
                    "categoryId": category_id,
                    "companyId": company_id,
                    "responsibleId": responsible_id,
                    "typeId": type_id,
                    "deadline": deadline,
                    "location": location,
                    "cost": cost
                }
            }
        }

        return self.exec(statement=statement, variables=variables)

    def update_ticket_status(self, ticket, status_id):
        statement = UPDATE_TICKET_STATUS_QUERY

        variables = {"ticketId": ticket, "statusId": status_id}
        return self.exec(statement=statement, variables=variables)

    def delete_ticket(self, ticket_id):
        statement = DELETE_TICKET_QUERY

        variables = {
            "input": {
                "ticketId": ticket_id
            }
        }

        return self.exec(statement=statement, variables=variables)
