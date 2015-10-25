from flask import Flask
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, String, Date, Boolean, Integer, Search
from elasticsearch_dsl.connections import connections

ELASTIC_URI = 'http://localhost:9200'
ELASTIC_INDEX = 'institution'

app = Flask(__name__)

connections.create_connection(hosts=[ELASTIC_URI])


class Institution(DocType):
	name = String()
	estabilished = String()
	location = {
		'street_address': String(),
		'city': String(),
		'state': String(),
		'country': String(),
		'ext_code': Integer()
	}
	web_url = String()
	_id = Integer()
	public = Boolean()
	for_profit = Boolean()
	degree = Boolean()
	class Meta:
		index = ELASTIC_INDEX

Institution.init()

s = Search()
res = s.execute()
print(res.hits.total)