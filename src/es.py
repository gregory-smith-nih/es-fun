#!/usr/bin/env python
"""
Elasticsearch CLI
"""

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import argparse
import re
import glsutils as gls
import sys
from es.info import info
from es.search import search
from es.create import create
from es.ingest import ingest
from es.ingest_directory import ingest_directory
from es.search_directory import search_directory
from es.alias import alias
from es.drop import drop
import urllib3


SERVICE='es'

global quiet
quiet=False

def main():
	args = getargs()
	filedata = readfile(args["file"])
	es = ElasticsearchOpen(args['host'], args['port'], args['aws']=="true")

	if args["cmd"] == "search": search(es, filedata, args["index"], args["limit"])
	elif args["cmd"] == "info": info(es, args["index"], args["type"])
	elif args["cmd"] == "create": create(es, args["index"], filedata)
	elif args["cmd"] == "ingest": ingest(es, args["index"], args["type"], filedata)
	elif args["cmd"] == "ingest_directory": ingest_directory(es, args["index"], args["type"], args["name"])
	elif args["cmd"] == "search_directory": search_directory(es, filedata, args["index"], args["name"], args["limit"])
	elif args["cmd"] == "drop": drop(es, args["index"])
	elif args["cmd"] == "alias": alias(es, args["index"], args["name"], args["action"])
	else: print("enter a command. one of [search, info, create, ingest, ingest_directory, drop, alias]")

def ElasticsearchOpen(host, port, aws=True):
	if quiet: urllib3.disable_warnings()
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
		es = Elasticsearch(
			hosts = [{'host':host, 'port':port}],
			use_ssl = False,
			ssl_show_warn = False)
	return es

def readfile(fname):
	filedata=""
	# gls.error(fname)
	if fname:
		with open(fname, 'r') as f:
			filedata = f.read()
	return filedata

def getargs():
	global quiet
	ap = argparse.ArgumentParser()
	ap.add_argument('-n', '--name', required=False, type = str, default="", help='name of an index or other object')
	ap.add_argument('-f', '--file', required=False, type = str, default="", help='optional input file')
	ap.add_argument('-H', '--host', required=False, type = str, default="localhost", help='hostname')
	ap.add_argument('-p', '--port', required=False, type = int, default=9200, help='port')
	ap.add_argument('-l', '--limit', required=False, type = int, default=10, help='limit')
	ap.add_argument('-t', '--type', required=False, type = str, default="", help='type')
	ap.add_argument('-i', '--index', required=False, type = str, default="", help='index')
	ap.add_argument('-q', '--quiet', required=False, type = str, default="", help='quiet the SSL warnings')
	ap.add_argument('--aws', required=False, type = str, default="true", help='use awsauth "true" or "false"')
	ap.add_argument('--cmd', required=False, type=str, default="help", help='one of [search, info]')
	ap.add_argument('-a', '--action', required=False, type = str, default="", help='an action on the command - sub command, if you will')
	
	args = vars(ap.parse_args())
	if args["quiet"]: quiet = True
	if args["cmd"] == "help":
		print("enter a --cmd. one of [search, info, create, ingest, ingest_directory, drop, alias]")
		exit()
	return args


if __name__ == '__main__':
	main()
