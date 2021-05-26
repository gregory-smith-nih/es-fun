# es-fun - elastic search fun

## Set up ElasticSearch 6.8.1
* Directions: https://www.elastic.co/blog/getting-started-with-elasticsearch-security
* Install Java 8 Runtime: https://www.oracle.com/java/technologies/javase/javase8u211-later-archive-downloads.html
* Download and install Elasticsearch 6.8.5: `curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.8.5.tar.gz`
  * NOTE: this link https://www.elastic.co/downloads/past-releases/elasticsearch-6-3-1
will get 6.3.1 but it has a catastrophic error that makes it unusable with Java 8. Recommend you get 6.8.5 as noted above
* edit elasticsearch.yml
    - set port=9210
* edit .bashrc
    - #export ES_HOME=~/elasticsearch-7.13.0
    - #export ES_HOME=~/elasticsearch-6.3.1
    - export ES_HOME=~/elasticsearch-6.8.5
    - export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_281.jdk/Contents/Home
    - export PATH=$JAVA_HOME/bin:${ES_HOME}/bin:$PATH
* run `elasticsearch`

## search.py - perform json query from input file
* Generic ElasticSearch Query runner
* Input file is a query JSON
* (std) output is the search results

1. connect to VPN using CISCO ANYCONNECT
2. run updateAWSKeys.sh # to freshen your aws credentials
    1. OR `okta-awscli  --force --profile DEVINT`
    1. Fresh install okta-awscli: pip3 install okta-awscli3
    2. Upgrade okta-awscli : pip3 install okta-awscli3 --upgrade
    3. (YOU SHOULD GET AN OKTA 2FA REQUEST)
3. run es-tunnel # so that you can access ES on https://localhost:9200
4. export AWS_PROFILE=DEVINT # so that you can import your credentials easily

`python src/search.py -f queries/query.json`
`usage: search.py [-h] -f FILE [-H HOST] [-p PORT]`

## find_field.py - find a field in result json
* Does a Depth-first-search looking for a field that matches the name passed in the args
* Returns a path to the first field found.

`usage: find_field.py [-h] -f FILE field`

## updateAWSKeys.sh

```bash
#!/bin/bash

#Update keys for all tiers you use. Comment those you don't use
echo "Updating DEVINT keys"
okta-awscli  --force --profile DEVINT

echo;echo "Updating UAT keys"
okta-awscli  --force --profile UAT

echo;echo "Updating PERF keys"
okta-awscli  --force --profile PERF

echo;echo "Updating PROD keys"
okta-awscli  --force --profile PROD

#Show new keys
echo;echo "Current Keys (Good for 12 hours):"
cat ~/.aws/credentials
```

## recreate-index.sh
`recreate-index.sh` will read a mappings file, split it into mappings and settings
and delete the entire index and type and ingest new data from the specified file

## search.sh
`search.sh` will read a query file and generate the results

