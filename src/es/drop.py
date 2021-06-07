import json
import glsutils as gls


def drop(es, index_name):
	if not index_name or not index_name: 
		print("you need to specify --index=index_name")
		return
	print("dropping index %s" % index_name)
	response = es.indices.delete(index=index_name, ignore=[400, 404])
	gls.jprint(response)