"""
Does a Depth-first-search looking for a field that matches the name passed in the args
Returns a path to the first field found.
"""

import json
import argparse

def flatten(A):
    rt = []
    for i in A:
        if isinstance(i,list): rt.extend(flatten(i))
        else: rt.append(i)
    return rt

def _find_fields_in_list(l, field):
    result = []
    for i in range(len(l)):
        x = _find_field(l[i], field)
        if x: return ["["+str(i)+"]", x]
    return result
    
def _find_field(d, field):
    if type(d) is list: return _find_fields_in_list(d, field)
    if type(d) is not dict: return ""
    result = []
    for key in d:
        if (key == field):
            return key
        else:
            found = _find_field(d[key], field)
            if found:
                result.append(key)
                result.append(found)
                return result
    return result

def find_field(d, field):
    result = _find_field(d, field)
    return ".".join(flatten(result)) if result else ""

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('field', type=str, help='field to search for')
    ap.add_argument('-f', '--file', required=True, type = str, help='query file to use as input')
    args = vars(ap.parse_args())
    print()

    with open(args['file'], 'r') as f:
        query = f.read()
        d = json.loads(query)

    print(d['hits']['hits'])
    print(">>> " + find_field(d, args['field']))
