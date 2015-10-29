import csv
import logging

from schema_transformer.transformer import CSVTransformer
from elasticsearch.exceptions import SerializationError
from main import Institution

logger = logging.getLogger(__name__)
logging.basicConfig()

IPEDS_FILE = 'raw_data/hd2013.csv'

class IpedsTransformer(CSVTransformer):

	def _transform_string(self, val, doc):
		val = super(IpedsTransformer, self)._transform_string(val, doc)
		return val.decode('Windows-1252').encode('utf-8')

	def load(self, doc):
		return doc

schema = {
	'name': 'INSTNM',
	'location': {
		'street_address': 'ADDR',
		'city': 'CITY',
		'state': 'STABBR',
		'ext_code': 'ZIP'
	},
	'web_url': 'WEBADDR',
	'id': 'UNITID',
	'public': ('CONTROL', lambda x: int(x) ==  2),
	'for_profit': ('CONTROL', lambda x: int(x) == 3),
	'degree': ('UGOFFER', lambda x: int(x) == 1)
}

def debug(func):
    def inner(*args, **kwargs):
        import ipdb
        with ipdb.launch_ipdb_on_exception():
            return func(*args, **kwargs)
    return inner

@debug
def main():
	with open(IPEDS_FILE) as f:
		reader = csv.reader(f)

		transformer = IpedsTransformer(schema, next(reader))

		for row in reader:
			transformed = transformer.transform(row)
			logger.info('Adding {0}.'.format(transformed['name']))
			
			inst = Institution(country='United States', **transformed)
			inst.save()

if __name__ == "__main__":
	main()


