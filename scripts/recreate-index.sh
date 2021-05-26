infile=$1;shift

HOST=localhost
PORT=9210
INDEX=strap

ES=$HOST:$PORT/$INDEX

function es {
    method="$1"; shift
    cmd="$1"; shift
    index="$1"; shift
    data="$1"; shift
    echo '>>>' $method $cmd $data
    if [[ "$index" ]]; then index="/"$index; fi
    if [[ "$cmd" ]]; then cmd="/"$cmd; fi
    if [[ "$data" ]]; then data="-d @$data"; fi
    curl -X $method -H 'Content-Type: application/json' "$ES$index$cmd?pretty" $data
}

jq < trial.settings-resourcing.json > trial._settings.json '.settings'
jq < trial.settings-resourcing.json > trial._mappings.json '.mappings'

es DELETE
es PUT
es POST _close
es PUT _settings "" trial._settings.json
es PUT _mappings "trial" trial._mappings.json
es POST _open

#items=`jq < extracts.json '.[]|.xxx?' | wc -l` ; items=10
#items=`jq < 10.json '.[]|.xxx?' | wc -l`
items=`jq < $infile '.[]|.xxx?' | wc -l`
echo $items
i=0
while true; do
    echo $i
    jq < $infile '.['$i']' > documents/$i.json
    es POST "" trial documents/$i.json
    i=$((i+1))
    if [[ $i -eq $items ]]; then break; fi
done
exit

curl -X POST 'localhost:9210/trial/my_app' -H 'Content-Type: application/json' -d'
{
	"timestamp": "2018-01-24 12:34:56",
	"message": "User logged in",
	"user_id": 4,
	"admin": false
}
'

curl -X POST "localhost:9200/_bulk?pretty" -H 'Content-Type: application/json' -d'
{ "index" : { "_index" : "test", "_id" : "1" } }
{ "field1" : "value1" }
{ "delete" : { "_index" : "test", "_id" : "2" } }
{ "create" : { "_index" : "test", "_id" : "3" } }
{ "field1" : "value3" }
{ "update" : {"_id" : "1", "_index" : "test"} }
{ "doc" : {"field2" : "value2"} }
'
