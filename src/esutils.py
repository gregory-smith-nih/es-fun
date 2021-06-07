import glsutils as gls

def info(es):
    results = es.info()
    results["indexes"] = get_aliases(es)

    statuses = get_statuses(es)
    for index in results["indexes"].keys():
        if not index: continue
        results["indexes"][index]["status"] = statuses[index]
        results["indexes"][index]["types"] = get_types(es, index)
        search_results = _search_one(es, index)
        results["indexes"][index]["total"] = gls.get(search_results, "hits.total", 0)
    return results

def get_indexes(es):
    aliases = get_aliases(es)
    indexes = [x for x in aliases.keys()]
    return indexes

def get_aliases(es):
    aliases = es.indices.get_alias("*")
    return aliases

def get_mappings(es):
    mappings = es.indices.get_mapping("*")
    return mappings

def get_mapping(es, index):
    mapping = es.indices.get_mapping(index)
    return mapping

def get_types(es, index):
    mapping = get_mapping(es, index)
    typedict = {}
    type_keys = mapping[index]["mappings"].keys()
    types = [x for x in type_keys]
    for type in types:
        search_results = _search_one_type(es, index, type)
        typedict[type] = gls.get(search_results, "hits.total", 0)
    return typedict

def get_statuses(es):
    dict = {}
    statuses = es.cat.indices("*").split("\n")
    for line in statuses:
        if not line: continue
        status = _expload_info(line)
        dict[status["index"]] = status
    return dict

def _expload_info(line):
    if not line: return {}
    fields = line.split()
    dict = {}
    i=0
    dict["status"] = fields[i]; i += 1
    dict["open"] = fields[i]; i += 1
    dict["index"] = fields[i]; i += 1
    dict["id"] = fields[i]; i += 1
    dict["shards"] = fields[i]; i += 1
    dict["n"] = fields[i]; i += 1
    dict["used"] = fields[i]; i += 1
    dict["documents"] = fields[i]; i += 1
    dict["available"] = fields[i]; i += 1
    dict["used"] = fields[i]; i += 1
    return dict

def _search_one(es, index):
	query = '{"from" : 0, "size" : 1}'
	results = es.search(body=query,index=index,request_timeout=30)
	return results

def _search_one_type(es, index, type):
    query = '{"from" : 0, "size" : 1,"query": {"match": {"_type": "'+type+'"} } }'
    results = es.search(body=query,index=index,request_timeout=30)
    return results