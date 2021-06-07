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

def search(es, query, index, limit=DEFAULT_SIZE):
	if limit == 0: limit = 1000000000 #infinite, please
	gls.error(gls.error("limit={:,.0f}".format(limit)))
	if not query:
		gls.error("Please specify a -f query.json")
		return

	limits = page_limits(query)
	curr = limits["from"] ### honor the original from
	size = limits["size"] or min(limit, MAX_PAGESIZE) ### honor the original size, or use the limit
	query = set_page(query, curr, size)
	cnt=0
	results=False
	while cnt < limit:
		response = es.search(body=query,index=index,request_timeout=TIMEOUT)
		cnt += len(gls.get(response, "hits.hits", []))
		total = gls.get(response, "hits.total", 0)
		if total < limit: limit = total
		newHits = gls.get(response, "hits.hits", [])
		if not results: results = response
		else: gls.get(results, "hits.hits", None).extend(newHits)
		gls.error("{:,.0f} of {:,.0f}".format(cnt, limit))
	gls.jprint(results)