import elasticsearch
from elasticsearch import ElasticSearch
import elasticsearch_dsl
from elasticsearch_dsl import Search
import psycopg2


es = ElasticSearch(
    "http://elastic:changeme@localhost:9200/"
)

conn = psycopg2.connect(
    host="localhost",
    database="spinneys",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

s = Search(index="es_spinneys") \
            .using(es) \
            .query("match", status="Product")
es_result = s.execute()

product_list = []

for _ in es_result:
    product_list.append(_.name)