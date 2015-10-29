import json
import logging

from schema_transformer.transformer import JSONTransformer
from main import Institution

logger = logging.getLogger(__name__)
logging.basicConfig()

GRID_FILE = 'raw_data/grid_2015_10_09.json'

class GridTransformer(JSONTransformer):
	def load(self, doc):
		return doc

schema = {
	'name': '/name',
	'location': {
		'street_address': ('/addresses', lambda x: x[0]['line_1']),
		'city': ('/addresses', lambda x: x[0]['city']),
		'state': ('/addresses', lambda x: x[0]['state']),
		'ext_code': ('/addresses', lambda x: x[0]['postcode']),
		'country': ('/addresses', lambda x: x[0]['country'])
	},
	'web_url': ('/links', lambda x: x[0]),
	'id': '/id',
	'other_names': ('/aliases', '/acronyms')
}

def debug(func):
    def inner(*args, **kwargs):
        import ipdb
        with ipdb.launch_ipdb_on_exception():
            return func(*args, **kwargs)
    return inner

@debug
def main():
	with open(GRID_FILE) as f:
		reader = csv.reader(f)

		transformer = GridTransformer(schema, next(reader))

		for row in reader:
			transformed = transformer.transform(row)
			logger.info('Adding {0}.'.format(transformed['name']))
			
			inst = Institution(**transformed)
			inst.save()

if __name__ == "__main__":
	main()