METHOD=${1};shift
CMD=${1};shift
TYPE=${1};shift
HOST=${HOST:-localhost};shift
PORT=${PORT:-9200};shift
INDEX=${INDEX:strap};shift
DATA=${1};shift

echo $HOST $PORT $INDEX $METHOD $CMD $TYPE $DATA

if [[ "$METHOD" == "" ]]; then echo "es.sh METHOD CMD TYPE data host port index"; exit; fi

ES=$HOST:$PORT/$INDEX

function es {
    method="$1"; shift
    cmd="$1"; shift
    type="$1"; shift
    data="$1"; shift
    echo '>>>' $method $cmd $data
    if [[ "$index" ]]; then index="/"$index; fi
    if [[ "$cmd" ]]; then cmd="/"$cmd; fi
    if [[ "$data" ]]; then data="-d @$data"; fi
    curl -X $method -H 'Content-Type: application/json' "$ES$type$cmd?pretty" $data
}

es $METHOD $CMD $TYPE $DATA
