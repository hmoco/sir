from . import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, String, Date
from elasticsearch_dsl.connections import connections

from . import settings
from main import Inst

connections.create_connection(hosts=['localhost'])

Institution.init()
