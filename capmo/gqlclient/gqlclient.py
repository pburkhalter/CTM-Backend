from pprint import pprint

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError, TransportServerError

from config import Config
from .auth import AuthAgent


class GraphQLClient:
    def __init__(self):
        self.auth_agent = AuthAgent()
        self.token = self.auth_agent.access_token

        self.endpoint = Config.CAPMO_API

        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {self.token}'
        }

    def _create_client(self) -> Client:
        transport = AIOHTTPTransport(url=self.endpoint, headers=self.headers)
        return Client(transport=transport, fetch_schema_from_transport=False)

    @staticmethod
    def _execute_query(client, statement, variables):
        query = gql(statement)
        response = client.execute(query, variables)
        return response['result']

    def exec(self, statement, variables):
        client = self._create_client()
        try:
            return self._execute_query(client, statement, variables)
        except (TransportServerError, TransportQueryError) as err:
            if 'Only authenticated users can make graphql requests.' in str(err):
                if self.auth_agent.refresh():
                    client = self._create_client()  # Refresh the client with new token
                    return self._execute_query(client, statement, variables)
                else:
                    raise RuntimeError("Failed to refresh token")
            else:
                raise
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}")
