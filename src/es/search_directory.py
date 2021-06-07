import json
import glsutils as gls

MAX_PAGESIZE=100
DEFAULT_SIZE=10
TIMEOUT=30

global quiet

def page_limits(query):
	dict = json.loads(query)
	From = dict.get("from", 0)
	size = dict.get("size", 0)
	limits = {}
	limits["from"] = From
	limits["size"] = size
	return limits

def set_page(query, From, size):
	dict = json.loads(query)
	dict['from'] = From
	dict['size'] = size
	query = json.dumps(dict)
	return query

def search_directory(es, query, index, dirname, limit=DEFAULT_SIZE):
	if not query or not index or not dirname:
		print(query)
		print(index)
		print(dirname)
		print("you need to specify --file=query.json --index=index --name=dirname")
		return
	if limit == 0: limit = 1000000000 #infinite, please

	limits = page_limits(query)
	curr = limits["from"] ### honor the original from
	size = limits["size"] or min(limit, MAX_PAGESIZE) ### honor the original size, or use the limit
	query = set_page(query, curr, size)
	cnt=0
	i = 0
	while cnt < limit:
		response = es.search(body=query,index=index,request_timeout=TIMEOUT)
		cnt += len(gls.get(response, "hits.hits", []))
		total = gls.get(response, "hits.total", 0)
		if total < limit: limit = total
		newHits = gls.get(response, "hits.hits", [])
		for hit in newHits:
			outfname = dirname + "/" + ("%05d" % i) + ".json"
			i += 1
			with open(outfname, 'w') as f:
				text = json.dumps(hit)
				f.write(text)
			if i % 100 == 0: gls.error("{:,.0f} of {:,.0f}".format(i, limit))
