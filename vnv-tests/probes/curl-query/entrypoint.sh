#!/bin/sh

echo "******* curlqueryprobe: starting entrypoint.sh ******"

source /${INSTALL_PATH}/config.cfg

echo "******* curlqueryprobe: creating folder /output/${PROBE}/${HOSTNAME} *******"

mkdir -p /output/${PROBE}/${HOSTNAME}

echo "ip = $IP"
echo "port = $PORT"
echo "query = $QUERY"

echo "******* curlqueryprobe: executing query : ${IP}:${PORT}${APIPATH}${QUERY}*******"

echo $(curl ${IP}:${PORT}${APIPATH}${QUERY}) > $RESULTS_FILE

cat $RESULTS_FILE

