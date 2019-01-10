# SELK

This page guides you through the process to deploy a combination of Suricata-IDS with ELK 


# Suricata-IDS

## Build the image

`$ docker build -t suricata .`


# Get the ELK official images

`$ docker pull docker.elastic.co/logstash/logstash:6.5.4` or
`$ docker pull logstash:6.5.4`

`$ docker pull docker.elastic.co/elasticsearch/elasticsearch:6.5.4` or
`$ docker pull elasticsearch:6.5.4`

`$ docker pull docker.elastic.co/kibana/kibana:6.5.4` or
`$ docker pull kibana:6.5.4`

# Run the containers

// Run Kibana Docker image: https://hub.docker.com/_/kibana

`$ docker run --rm -e ELASTICSEARCH_URL="http://localhost:9200" --hostname=kibana --name=kibana --network=host -p 5601:5601 -t docker.elastic.co/kibana/kibana:6.5.4`

// Run Elasticsearch Docker image: https://www.elastic.co/guide/en/elasticsearch/reference/6.4/docker.html

`$ docker run --rm -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --hostname=elasticsearch --name=elasticsearch --network=host --mount source=elastic,destination=/usr/share/elasticsearch/data -t docker.elastic.co/elasticsearch/elasticsearch:6.5.4`


// Run Logstash Docker image: https://www.elastic.co/guide/en/logstash/current/docker-config.html

`$ docker run --rm -d -e xpack.monitoring.elasticsearch.url="http://localhost:9200" --hostname=logstash --name=logstash --network=host -v ~/tng-industrial-pilot/vnfs/ids-suricata/logstash.conf:/usr/share/logstash/config/logstash.conf -t docker.elastic.co/logstash/logstash:6.5.4`

`$ docker run --network=host --hostname=suricata --name=suricata -it suricata`

