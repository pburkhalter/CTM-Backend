from peewee import SqliteDatabase, PostgresqlDatabase, MySQLDatabase

from config import Config


DATABASE_MAPPING = {
    'sqlite': SqliteDatabase,
    'postgresql': PostgresqlDatabase,
    'mysql': MySQLDatabase
}


def get_database_instance(config_name):
    database_class = DATABASE_MAPPING.get(config_name)
    if not database_class:
        raise ValueError(f"Unsupported database type: {config_name}")
    return database_class


dbi = get_database_instance(Config.DATABASE_TYPE)
db = dbi(Config.DATABASE, **Config.DATABASE_OPTIONS)
