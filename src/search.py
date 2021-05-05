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

SERVICE='es'

def search(query, host, port):
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
		ssl_show_warn = False
	)

	response = es.search(body=query)

	return json.dumps(response, indent = 4, separators=(",", ": "), sort_keys=True)

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('-f', '--file', required=True, type = str, help='query file to use as input')
	ap.add_argument('-H', '--host', required=False, type = str, default="localhost", help='hostname')
	ap.add_argument('-p', '--port', required=False, type = int, default=9200, help='port')
	args = vars(ap.parse_args())

	with open(args['file'], 'r') as f:
		query = f.read()

	try:
		result = search(query, args['host'], args['port'])
		print(result)
	except Exception as ex:
		print(str(ex))

if __name__ == '__main__':
	main()
