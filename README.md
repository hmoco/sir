# SIR (SHARE Institutions Repository)

## Primary Goals And Rationale
This is inteded to be a quick implementation of a collection of institutions, with unique identifiers and convenient API, 
to be used (at first) for COS projects, namely SHARE and OSF. This is not intended to eclipse efforts (some of which are 
being used as scaffolding for this project) done by other groups, nor to claim a complete catalog of all (wanted) 
institutions. With that in mind, advantages for internal use are:

1. Use of unique IDs for data from multiple sources. This allows disambiguation and deduplication efforts to be carried
out to the extent necessary for its use cases, and not any more. Use cases are:
	
	1. OSF users being able to attach institutions to their profiles.
	
	2. SHARE documents being able to point to an unique ID used here, instead of carrying institutions' metadata.

2. Api endpoints with return values tailored for OSF and SHARE. An example of that is the autocomplete endpoint, which
will allow for a simple add institution interface in the OSF. Also, as mainly a wrapper around elastic search queries, this
allows the project to be used outside of COS, so that requests cannot alter the data, but the data itself is openly available.

## Current API Endpoints
1.  ` /institutions', methods=['GET', 'POST'] `
2.  ` /institutions/names', methods=['GET', 'POST'] `
3.  ` '/institutions/autocomplete', methods=['GET'] `

TODO: I/O format

## Current Data Addition Strategy
1. Locally stored raw data, parsed using the schema-transformer library into the Institutions model, which defines 
the schema:
		
		``` 
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
		_id = String()
		public = Boolean()
		for_profit = Boolean()
		degree = Boolean()
		other_names = String()
		```

2. An strategy for finding existing entries, and a strategy to update rather than replace.
