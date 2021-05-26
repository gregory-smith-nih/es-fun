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
import sys

SERVICE='es'
MAX_PAGESIZE=10000
DEFAULT_SIZE=10

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

def search(query, host, port, aws=True, limit=DEFAULT_SIZE):
	limits = page_limits(query)
	curr = limits["from"] ### honor the original from
	size = limits["size"] or min(limit, MAX_PAGESIZE) ### honor the original size, or use the limit
	query = set_page(query, curr, size)

	if aws:
		session = boto3.Session() ### use AWS_PROFILE env to select profile
		credentials = session.get_credentials() 
		access_key = credentials.access_key
		secret_key = credentials.secret_key
		session_token = credentials.token
		region = session.region_name
		awsauth=AWS4Auth(access_key, secret_key, region, SERVICE, session_token=session_token)

		es = Elasticsearch(
			hosts = [{'host':host, 'port':port}],
			http_auth = awsauth,
			use_ssl = True,
			verify_certs = False,
			connection_class = RequestsHttpConnection,
			ssl_show_warn = False)
	else:
		es = Elasticsearch(hosts = [{'host':host, 'port':port}])

	cnt=0
	while cnt < limit:
		response = es.search(body=query)
		str = json.dumps(response, indent = 4, separators=(",", ": "), sort_keys=True)
		cnt += len(util.get(response, "hits.hits", []))
		total = util.get(response, "hits.total", 0)
		return response

def info(host, port, aws=True):
	if aws:
		session = boto3.Session() ### use AWS_PROFILE env to select profile
		credentials = session.get_credentials() 
		access_key = credentials.access_key
		secret_key = credentials.secret_key
		session_token = credentials.token
		region = session.region_name
		awsauth=AWS4Auth(access_key, secret_key, region, SERVICE, session_token=session_token)

		es = Elasticsearch(
			hosts = [{'host':host, 'port':port}],
			http_auth = awsauth,
			use_ssl = True,
			error_trace=True,
			verify_certs = False,
			connection_class = RequestsHttpConnection,
			ssl_show_warn = False)
	else:
		es = Elasticsearch(hosts = [{'host':host, 'port':port}])

	response = es.info()
	return response

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('-f', '--file', required=False, type = str, help='query file to use as input')
	ap.add_argument('-H', '--host', required=False, type = str, default="localhost", help='hostname')
	ap.add_argument('-p', '--port', required=False, type = int, default=9200, help='port')
	ap.add_argument('-l', '--limit', required=False, type = int, default=10, help='limit')
	ap.add_argument('-i', '--info', required=False, type = str, default="no", help='information? "yes" or "no"')
	ap.add_argument('--aws', required=False, type = str, default="true", help='use awsauth "true" or "false"')
	args = vars(ap.parse_args())

	if args['info'] == 'yes':
		result = info(args['host'], args['port'], args['aws']=="true")
		print(json.dumps(result))
		return

	if not args['file']:
		print("ERROR: -f FILE (required")
		ap.print_usage()
		return

	with open(args['file'], 'r') as f:
		query = f.read()

	# try:
		result = search(query, args['host'], args['port'], args['aws']=="true", args['limit'])
	# except:
	# 	print(sys.exc_info()[0])
	# 	print("ERROR: did you try --aws==false?")
	# 	return

	print(json.dumps(result))


if __name__ == '__main__':
	main()
