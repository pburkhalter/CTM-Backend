from capmo.gqlclient.gqlclient import GraphQLClient
from capmo.queries.user import GET_USER_DETAILS_QUERY


class CapmoUserClient(GraphQLClient):

    def __init__(self):
        super().__init__()

    def get_user(self):
        statement = GET_USER_DETAILS_QUERY

        return self.exec(statement=statement, variables={})

