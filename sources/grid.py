import json
import logging
from schema_transformer.transformer import JSONTransformer

from models import Institution
from settings import GRID_FILE

logger = logging.getLogger(__name__)
logging.basicConfig()

class GridTransformer(JSONTransformer):
	pass

schema = {
	'name': '/name',
	'location': {
		'street_address': ('/addresses', lambda x: x[0]['line_1'] if x else None),
		'city': ('/addresses', lambda x: x[0]['city'] if x else None),
		'state': ('/addresses', lambda x: x[0]['state'] if x else None),
		'ext_code': ('/addresses', lambda x: x[0]['postcode'] if x else None),
		'country': ('/addresses', lambda x: x[0]['country'] if x else None)
	},
	'web_url': ('/links', lambda x: x[0] if x else None),
	'id_': '/id',
	'other_names': ('/aliases', '/acronyms', lambda x, y: x + y if x and y else x if x else y if y else None)
}

def debug(func):
    def inner(*args, **kwargs):
        import ipdb
        with ipdb.launch_ipdb_on_exception():
            return func(*args, **kwargs)
    return inner

def populate():
	with open(GRID_FILE) as f:
		clean = f.read().replace('\n', '')
		docs = json.loads(clean)
		transformer = GridTransformer(schema)

		for doc in docs['institutes']:
			try:
				transformed = transformer.transform(doc, load=False)
				#logger.info('Adding {0}.'.format(transformed['name']))
			
				inst = Institution(**transformed)
				inst.save()
				print transformed
			except UnicodeDecodeError:
				pass

if __name__ == "__main__":
	populate()
