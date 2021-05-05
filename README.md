# es-fun - elastic search fun
## search.py - perform json query from input file
* Generic ElasticSearch Query runner
* Input file is a query JSON
* (std) output is the search results

`usage: search.py [-h] -f FILE [-H HOST] [-p PORT]`

## find_field.py - find a field in result json
* Does a Depth-first-search looking for a field that matches the name passed in the args
* Returns a path to the first field found.

`usage: find_field.py [-h] -f FILE field`