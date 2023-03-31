import os
import json
import logging

from typing import Optional, List, Dict
from elasticsearch import Elasticsearch
from pydantic import BaseSettings, Field, SecretStr
from sqlalchemy import select, MetaData, Table

from app.db import db
from app import config

db_engine = db.get_engine
meta = MetaData(bind=db_engine)

class EsManagement:
    def __init__(self):
        self.es_client = Elasticsearch(
            [config.ELASTICSEARCH_HOST],
            http_auth=(config.ELASTICSEARCH_USER, config.ELASTICSEARCH_PASSWORD)
        )
        logging.info(self.es_client.ping())

    def create_index(self, index_name: str, mapping: Dict) -> None:
        """
        Create an ES index.
        :param index_name: Name of the index.
        :param mapping: Mapping of the index
        """
        logging.info(f"Creating index {index_name} with the following schema: {json.dumps(mapping, indent=2)}")
        self.es_client.indices.create(index=index_name, ignore=400, body=mapping)

    def populate_index(self, table_name: str, index_name: str) -> None:
        """
        Populate an index from a PostgreSQL table.
        """
        table = Table(f"{table_name}", meta, auto_load=True, autoload_with=db_engine)
        query = select([table])
        transaction = db_engine.execute(query)
        result = transaction.fetchone()
        #
        #  https://stackoverflow.com/questions/56133020/indexing-sqlalchemy-models-on-elasticsearch
            
        self.es_client.index(index=index_name, body=json.dumps(result._asdict()))
