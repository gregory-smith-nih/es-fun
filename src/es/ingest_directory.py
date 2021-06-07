import json
import glsutils as gls
from os import listdir
from os.path import isfile, join
import time

TIMEOUT=30
SLEEP=1
def ingest_directory(es, index_name, doc_type, dirname):
	if not doc_type or not index_name or not dirname: 
		print("you need to specify --type=doc_type, --index=index_name and --name=dirname")
		return
	
	documents = [f for f in listdir(dirname) if isfile(join(dirname, f))]
	cnt = 0
	for docname in documents:
		docpath = dirname + "/" + docname
		with open(docpath, 'r') as f:
			text = f.read()
			document = json.loads(text)
		document = document['_source']
		if gls.get(document, "_aggregates", None): del document["_aggregates"]
		ingest_document(es, index_name, doc_type, document)
		cnt = cnt + 1
		if cnt % 100 == 0: gls.error("count: " + str(cnt))

def ingest_document(es, index_name, doc_type, document):
	response = es.index(
		index = index_name,
		doc_type = doc_type,
		body = document,
		request_timeout=TIMEOUT)
	#time.sleep(SLEEP)
