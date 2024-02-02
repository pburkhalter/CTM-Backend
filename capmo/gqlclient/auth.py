import requests
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError

from config import Config


class AuthAgentException(Exception):
    pass


class AuthAgent:
    _instance = None  # Class attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AuthAgent, cls).__new__(cls)
        return cls._instance

    def __init__(self):

        if not hasattr(self, 'is_initialized'):
            self.headers = {'Content-Type': 'application/json; charset=utf-8'}
            self.is_initialized = True  # Flag to indicate that the instance is initialized

            self.url = Config.CAPMO_AUTH
            self.email = Config.CAPMO_USER
            self.password = Config.CAPMO_PASSWORD

            self.id_token = None
            self.access_token = None
            self.refresh_token = None

            self.auth(
                self.url,
                self.email,
                self.password
            )

    def auth(self, url, email, password):
        if self.access_token:
            return True

        self.url = url

        payload = {
            "email": email,
            "password": password
        }

        response = self.request(self.url + "login", payload)
        if response is not None and 'AccessToken' in response['token']:
            self.id_token = response['token']['IdToken']
            self.access_token = response['token']['AccessToken']
            self.refresh_token = response['token']['RefreshToken']

            return True
        return False

    def refresh(self):
        payload = {
            "refreshToken": self.refresh_token
        }

        response = self.request(self.url + "refreshToken", payload)
        if response is not None:
            self.id_token = response['token']['IdToken']
            self.access_token = response['token']['AccessToken']

            return self.access_token
        return False

    def check(self):
        query = gql("""query AppcuesIdentifyQuery {me {id}}""")
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Authorization': 'Bearer ' + self.access_token
                   }

        transport = AIOHTTPTransport(url=self.url + "graphql", headers=headers)
        api_client = Client(transport=transport, fetch_schema_from_transport=False)

        try:
            api_client.execute(query, {})
        except TransportQueryError as err:
            if err.errors[0]['message'] == 'Only authenticated users can make graphql requests.':
                return False
            return True

    def request(self, url, payload):
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            raise AuthAgentException(e)
