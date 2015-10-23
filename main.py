from flask import Flask
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, String, Date, Nested


app = Flask(__name__)
es = Elasticsearch()

class Institution(DocType):
	title = String()
	estabilished = Date()
	location = Nested(
		properties={
			'street_address': String(),
			'city': String(),
			'state': String(),
			'country': String(),
			'ext_code': Integer()
		}
	)
	web_url = String()
	_id = Integer()
	class Meta:
		index = 'institution'

