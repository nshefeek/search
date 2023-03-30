from pydantic import BaseSettings, Field, SecretStr


class ESAuth(BaseSettings):
    """
    Settings for ElasticSearch
    """

    host: str = Field(env="ELASTICSEARCH_HOST", default="http://localhost:9200")
    user: str = Field(env="ELASTICSEARCH_USER", default="elastic")
    password: str = Field(env="ELASTICSEARCH_PASSWORD", default="changeme")


es_auth = ESAuth()