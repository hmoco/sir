from elasticsearch_dsl import DocType, String, Date, Boolean, Integer

from settings import ELASTIC_INDEX

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
	id_ = String()
	public = Boolean()
	for_profit = Boolean()
	degree = Boolean()
	other_names = String()
	
	def save(self, **kwargs):
		self.meta.id = self.id_
		return super(Institution, self).save(**kwargs)

	class Meta:
		index = ELASTIC_INDEX
