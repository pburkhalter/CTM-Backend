import logging
import yaml


CONFIG_FILE = 'config.yml'

def get_config_prop(key):
    try:
        with open(CONFIG_FILE, 'r') as file:
            data = yaml.safe_load(file)
            # Assuming 'key' is a top-level key in the YAML structure
            return data.get(key, None)  # Returns None if key doesn't exist
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except FileNotFoundError:
        print(f"YAML file '{CONFIG_FILE}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


class Config(object):
    DEBUG = False

    VERSION_MAJOR = 0
    VERSION_MINOR = 3
    VERSION_PATCH = 6
    VERSION_RELEASE = 'BETA'

    LOG_TYPE = 'rotating'  # Example: 'rotating', 'file', 'console'
    LOG_FILE = 'app.log'
    LOG_LEVEL = logging.ERROR
    LOG_FORMAT = '%(asctime)s - %(module)s - %(levelname)s - %(message)s'
    LOG_MAX_BYTES = 1000000
    LOG_BACKUP_COUNT = 3

    HOST = '0.0.0.0'
    PORT = 8080

    SECRET_KEY = get_config_prop('secret_key')
    REFRESH_SECRET_KEY = get_config_prop('refresh_secret_key')

    CAPMO_AUTH = 'https://api.capmo.de/'
    CAPMO_API = 'https://api.capmo.de/graphql'

    CAPMO_USER = get_config_prop('capmo_user')
    CAPMO_PASSWORD = get_config_prop('capmo_password')

    DATABASE_TYPE = 'sqlite'
    DATABASE = 'ctm.db'
    DATABASE_OPTIONS = {}

    SCHEDULE_INTERVAL_HOURS = 1
    SCHEDULE_PROJECT_HOURS = 24
    SCHEDULE_TICKET_HOURS = 6

    LOCK_FILE_PATH = './lockfile.lock'

