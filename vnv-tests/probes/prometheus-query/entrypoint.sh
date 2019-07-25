#!/bin/bash

echo "******* curlqueryprobe: starting entrypoint.sh ******"

source /${INSTALL_PATH}/config.cfg

echo "******* curlqueryprobe: creating folder /output/${PROBE}/${HOSTNAME} *******"

mkdir -p /output/${PROBE}/${HOSTNAME}

echo "ip = $IP"
echo "port = $PORT"
echo "query = $QUERY"

echo "******* curlqueryprobe: executing query : ${IP}:${PORT}/api/v1/query?query=${QUERY}*******"

echo $(curl ${IP}:${PORT}/api/v1/query?query=${QUERY}) > $RESULTS_FILE

cat $RESULTS_FILE

