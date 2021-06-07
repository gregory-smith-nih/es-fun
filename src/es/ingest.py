import json
import glsutils as gls

def ingest(es, index_name, doc_type, filedata):
	if not doc_type or not index_name or not filedata: 
		print("you need to specify --file=infile.json, --index=index_name and --type=doc_type")
		return
	documents = json.loads(filedata)
	#gls.jprint(documents)
	cnt = 0
	if gls.isArray(documents):
		for document in documents:
			ingest_document(es, index_name, doc_type, document)
			cnt = cnt + 1
			if cnt % 100 == 0: gls.error("count: " + cnt)
	else:
		ingest_document(es, index_name, doc_type, documents)
	return

def ingest_document(es, index_name, doc_type, document):
	response = es.index(
		index = index_name,
		doc_type = doc_type,
		body = document)
	gls.jprint(response)
