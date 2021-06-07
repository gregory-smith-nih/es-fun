import json

raw_json = '{"a": true, "b": false}'
print(raw_json)
dict_json = json.loads(raw_json)
print(dict_json)
str_json = json.dumps(dict_json)
print(str_json)