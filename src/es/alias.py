import json
import glsutils as gls


def alias(es, index_name, alias_name, action):
	if not index_name or not alias_name or not action: 
		print("you need to specify --index=index_name --name=alias_name --action=[add,remove]")
		return
	actions = {"actions": [{action: {"index": index_name, "alias": alias_name}}]}
	response = es.indices.update_aliases(actions)
	print(response)