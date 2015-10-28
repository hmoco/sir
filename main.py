import json

from flask import Flask, request, Response
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, String, Date, Boolean, Integer, Search, Q
from elasticsearch_dsl.connections import connections

ELASTIC_URI = 'http://localhost:9200'
ELASTIC_INDEX = 'institution'
SIZE = 10

app = Flask(__name__)
app.debug = True

connections.create_connection(hosts=[ELASTIC_URI])

INSTITUTION_FIELDS = ['name', 'established', 'street_address', 'city', 'state', 'country', 'ext_code', 'web_url',
'_id', 'public', 'for_profit', 'degree']

class Institution(DocType):
	name = String()
	established = String()
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
	
	def save(self, **kwargs):
		self.meta.id = self.id
		return super(Institution, self).save(**kwargs)

	class Meta:
		index = ELASTIC_INDEX

def main():
	Institution.init()

def query_builder(queries, _and=True):
	assert validate_fields(queries.keys())
	queries = [ Q('match', **{k: v}) for k, v in queries.items() ]
	
	func = (lambda x, y: x & y) if _and else (lambda x, y: x | y)
	return reduce(func, queries)

def validate_fields(keys):
	for key in keys:
		if key not in INSTITUTION_FIELDS:
			return False
	return True

@app.route('/institutions', methods=['GET', 'POST'])
def all_institutions():
	page = int(request.args.get('page') or 1)
	start = (page - 1) * SIZE
	queries = {key: value for key, value in request.args.items() if key != 'page'}
	queries.update({key: value for key, value in (request.json or {}).items() if key != 'page'})

	try:
		query = query_builder(queries)
	except AssertionError:
		return Response({'Query Invalid'}, status=500)

	s = Search(index=ELASTIC_INDEX).query(query)[start:start + SIZE]
	res = s.execute()

	#Do some logic then return the results

	return Response(json.dumps(res.to_dict()), status=200)


@app.route('/')
def home():
    return 'poo'

if __name__ == '__main__':
	main()
	app.run()
