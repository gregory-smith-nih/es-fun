import json
from glsutils import jprint, set


def create(es, index_name, mappings, shards=2, replicas=0):
	if not mappings or not index_name: 
		print("you need to specify --file=mappings and --index=index_name")
		return
	request_body = {}
	# request_body["mappings"] = json.loads(mappings)
	# jprint(request_body)
	request_body = json.loads(mappings)
	set(request_body, "settings.number_of_shards", shards)
	set(request_body, "settings.number_of_replicas", replicas)

	print("creating mapping %s" % index_name)
	response = es.indices.create(index = index_name, body = request_body)
	jprint(response)