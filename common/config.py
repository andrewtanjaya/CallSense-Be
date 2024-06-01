import logging
from datetime import timedelta
from enum import Enum
from os import getenv as os_getenv
from sys import argv as sys_argv

import dotenv

logging.basicConfig(level=logging.INFO)


def load_env():
    env_file = ".env"

    for arg in sys_argv:
        if "pytest" in arg:
            if dotenv.find_dotenv(".env.test"):
                env_file = ".env.test"
                break

    dotenv.load_dotenv(dotenv_path=env_file, verbose=True)


load_env()


def get_bool_env(key: str, default: bool = False) -> bool:
    value = os_getenv(key)
    if value is None or value == "":
        return default

    map = {
        "true": True,
        "y": True,
        "yes": True,
        "on": True,
        "false": False,
        "n": False,
        "no": False,
        "off": False,
    }

    result = map.get(value.lower())
    if result is None:
        exc = ValueError("%s is not valid boolean representation" % value)
        logging.exception(exc)
        return default
    return result


def get_int_env(key: str, default: int) -> int:
    value = os_getenv(key)
    if value is None or value == "":
        return default

    try:
        return int(value)
    except Exception as e:
        logging.exception(e)
        return default


def get_timedelta_env(key: str, default: timedelta) -> timedelta:
    value = os_getenv(key)
    if value is None or value == "":
        return default

    try:
        return timedelta(int(value))
    except Exception as e:
        logging.exception(e)
        return default


class Environment(Enum):
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"
    SCRAPPER = "SCRAPPER"


CONFIG_ENV = Environment.DEVELOPMENT
if os_getenv("CONFIG_ENV") == Environment.PRODUCTION:
    CONFIG_ENV = Environment.PRODUCTION

CONFIG_DEBUG = get_bool_env("CONFIG_DEBUG", False)
CONFIG_HOST_URL = os_getenv("CONFIG_HOST_URL")

"""
DB Config
"""
DB_USER = os_getenv("DB_USER")
DB_PASS = os_getenv("DB_PASS")
DB_NAME = os_getenv("DB_NAME")
DB_HOST = os_getenv("DB_HOST")
DB_PORT = os_getenv("DB_PORT")
DB_SSL_CA = os_getenv("DB_SSL_CA")
DB_SSL_CERT = os_getenv("DB_SSL_CERT")
DB_SSL_KEY = os_getenv("DB_SSL_KEY")


def _set_database_url():
    if DB_SSL_CA and DB_SSL_CERT and DB_SSL_KEY:
        return (
            "postgresql+psycopg2://%s:%s@%s:%s/%s?"
            "sslrootcert=%s&sslcert=%s&sslkey=%s"
            % (
                DB_USER,
                DB_PASS,
                DB_HOST,
                DB_PORT,
                DB_NAME,
                DB_SSL_CA,
                DB_SSL_CERT,
                DB_SSL_KEY,
            )
        )
    return "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
        DB_USER,
        DB_PASS,
        DB_HOST,
        DB_PORT,
        DB_NAME,
    )


DATABASE_URL = _set_database_url()

"""
SQLAlchemy Engine Config
"""
ENGINE_POOL_PRE_PING = get_bool_env("ENGINE_POOL_PRE_PING", True)
ENGINE_POOL_USE_LIFO = get_bool_env("ENGINE_POOL_USE_LIFO", True)
ENGINE_IMPLICIT_RETURNING = get_bool_env("ENGINE_IMPLICIT_RETURNING", False)
ENGINE_POOL_SIZE = get_int_env("ENGINE_POOL_SIZE", 20)
ENGINE_POOL_RECYCLE = get_int_env("ENGINE_POOL_RECYCLE", 3600)

GOOGLE_APPLICATION_CREDENTIALS = os_getenv("GOOGLE_APPLICATION_CREDENTIALS")
FIREBASE_STORAGE_BUCKET = os_getenv("FIREBASE_STORAGE_BUCKET")
