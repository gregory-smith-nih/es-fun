"""
Generic ElasticSearch Query runner
Input file is a query JSON
(std) output is the search results
"""

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import json
import argparse
import re
import glsutils as util

def remove_special_entries(source):
	new_source = {}
	for key in source:
		if key[0] == '_': continue
		new_source[key] = source[key]
	return new_source

def extract_hits(s):
	es_results = json.loads(s)
	results = []
	docs = util.get(es_results, "hits.hits", [])
	for doc in docs:
		source = remove_special_entries(doc["_source"])
		results.append(source)
	return results

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('-f', '--file', required=True, type = str, help='query file to use as input')
	args = vars(ap.parse_args())

	with open(args['file'], 'r') as f:
		results = f.read()

	hits = extract_hits(results)
	print(json.dumps(hits))


if __name__ == '__main__':
	main()
