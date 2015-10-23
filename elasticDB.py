from . import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, String, Date
from elasticsearch_dsl.connections import connections

from . import settings
from main import Inst

connections.create_connection(hosts=['localhost'])


class Institution(DocType):

	class Meta:
        index = 'institutions'

	name = String()



Institution.init()


class DbManager():
	def __init__(self, uri=None):
		self.uri = uri or settings.ELASTIC_URI
		self.index = settings.ELASTIC_INDEX
		self.doc_type = settings.SCHEMA_NAME

	def connect(self):
		self.es = Elasticsearch(self.uri)

	def input(self, doc, _id, index=None, doc_type=None):
		self.es.index(
			index=index or self.index,
			doc_type=doc_type or self.doc_type,
			body=doc,
			id=_id
		)
