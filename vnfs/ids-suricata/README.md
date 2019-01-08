# SELK

This page guides you through the process to deploy a combination of Suricata-IDS with ELK 


# Suricata-IDS

## Build the image

`
$ docker build -t suricata .
`

## Run the Container

`
$ docker run --network=host --hostname=suricata --name=suricata -it suricata
`

# ELK

## Get the ELK official images

`
$ docker pull logstash:6.5.4
`

`
$ docker pull elasticsearch:6.5.4
`

`
$ docker pull kibana:6.5.4
`

## Run the containers

`
$ docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --hostname=elastic --name=elastic --network=host -t --mount source=elastic,destination=/usr/share/elasticsearch/data docker.elastic.co/elasticsearch/elasticsearch:6.5.4
`

`
$ docker run -e ELASTICSEARCH_URL="http://localhost:9200" --hostname=kibana --name=kibana --network=host -p 5601:5601 -t docker.elastic.co/kibana/kibana:6.5.4
`

`
$ docker run --hostname=logstash --name=logstash --network="host" -e "xpack.monitoring.elasticsearch.url=http://localhost:9200" -t logstash
`
