import csv
from schema_transformer.transformer import CSVTransformer

class IpedsTransformer(CSVTransformer):
	def load(self, doc):
		return doc

schema = {
	'name': 'INSTNM',
	'location': {
		'street_address': 'ADDR',
		'city': 'CITY',
		'state': '',
		'country': String(),
		'ext_code': Integer()
	}
	'web_url': 'WEBADDR',
	'_id': ('UNITID', lambda x: int(x)),
	'public': ('CONTROL', lambda x: int(x) == 2),
	'for_profit': ('CONTROL', lambda x: int(x) ==3),
	'degree': 
}

f = open('hd2013.csv')
reader = csv.reader(f)

transformer = IpedsTransformer(schema, )