import json
import markdown
from flask import Flask, request, Response, render_template, Markup
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, String, Date, Boolean, Integer, Search, Q
from elasticsearch_dsl.connections import connections

from models import Institution
from settings import ELASTIC_URI, ELASTIC_INDEX, SIZE, INSTITUTION_FIELDS

app = Flask(__name__)
app.debug = True

connections.create_connection(hosts=[ELASTIC_URI])

def main():
	Institution.init()

def query_builder(queries, _and=True):
	assert validate_fields(queries.keys())
	queries = [Q('match', **{k: v}) for k, v in queries.items()]
	if not queries:
		return None
	
	func = (lambda x, y: x & y) if _and else (lambda x, y: x | y)
	return reduce(func, queries)

def validate_fields(keys):
	for key in keys:
		if key not in INSTITUTION_FIELDS:
			return False
	return True

def get_names(result):
	return [val['_source']['name'] for val in result.to_dict().get('hits').get('hits')]

def search_builder(request, size=SIZE):
	page = int(request.args.get('page') or 1)
	start = (page - 1) * size
	queries = {key: value for key, value in request.args.items() if key != 'page'}
	queries.update({key: value for key, value in (request.json or {}).items() if key != 'page'})

	try:
		query = query_builder(queries)
	except AssertionError as e:
		raise e

	if query:
		return Search(index=ELASTIC_INDEX).query(query)[start:start + size]

	return Search(index=ELASTIC_INDEX)[start:start + size]

@app.route('/institutions', methods=['GET', 'POST'])
def all_institutions():
	try:
		s = search_builder(request)
	except AssertionError:
		return Response({'Query Invalid'}, status=500)
		
	res = s.execute()

	return Response(json.dumps(res.to_dict()), status=200)

@app.route('/institutions/names', methods=['GET', 'POST'])
def all_institutions_titles():
	try:
		s = search_builder(request, size=20)
	except AssertionError:
		return Response({'Query Invalid'}, status=500)

	res = s.execute()

	return Response(json.dumps(get_names(res)), status=200)

@app.route('/institutions/autocomplete', methods=['GET'])
def autocomplete_institutions_titles():
	name = str(request.args.get('name'))
	if not name:
		return Response({'Autocomplete query requires a "?name={} parameter'}, status=500)
	page = int(request.args.get('page') or 1)
	size = int(request.args.get('size') or SIZE)
	start = (page - 1) * size
	s_title = Search(index=ELASTIC_INDEX).query('match_phrase_prefix', name={'query': name, 'slop': 5})[start:start + size]
	res_title = s_title.execute()
	s_alias =  Search(index=ELASTIC_INDEX).query('match_phrase_prefix', other_names={'query': name, 'slop': 5})[start:start + size]
	res_alias = s_alias.execute()
	comb = list(set(get_names(res_alias) + get_names(res_title)))
	return Response(json.dumps(comb), status=200)

@app.route('/')
def home():
	with open('README.md', 'r') as docs:
		content = Markup(markdown.markdown(docs.read()))
	return render_template('home.html', content=content)

if __name__ == '__main__':
	main()
	app.run()
