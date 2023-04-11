from pathlib import Path
from urllib import parse

from starlette.config import Config
from starlette.datastructures import Secret

BASE_DIR = Path(__file__).resolve().parent.parent

config = Config('.env')


# Database Config
SHOW_SQL = config('SHOW_SQL', cast=bool, default=False)
DATABASE_HOSTNAME = config("DATABASE_HOSTNAME", default="localhost")
DATABASE_CREDENTIALS = config("DATABASE_CREDENTIALS", cast=Secret, default="postgres:postgres")
_DATABASE_CREDENTIAL_USER, _DATABASE_CREDENTIAL_PASSWORD = str(DATABASE_CREDENTIALS).split(":")
_QUOTED_DATABASE_PASSWORD = parse.quote(str(_DATABASE_CREDENTIAL_PASSWORD))
DATABASE_NAME = config("DATABASE_NAME", cast=str, default="spinneys")
DATABASE_PORT = config("DATBASE_PORT", default="5432")
DATABASE_ENGINE_POOL_SIZE = config("DATABASE_ENGINE_POOL_SIZE", cast=int, default=20)
DATABASE_ENGINE_MAX_OVERFLOW = config("DATABASE_ENGINE_MAX_OVERFLOW", cast=int, default=0)
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{_DATABASE_CREDENTIAL_USER}:{_QUOTED_DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"


# Elasticsearch Config
ELASTICSEARCH_HOST = config("ELASTICSEARCH_HOST", default="http://elasticsearch:9200/")
ELASTICSEARCH_USER = config("ELASTICSEARCH_USER", default="elastic")
ELASTICSEARCH_PASSWORD = config("ELASTICSEARCH_PASSWORD", default="changeme")