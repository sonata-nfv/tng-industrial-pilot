# SELK

This page guides you through the process to deploy a combination of Suricata-IDS with ELK using the following methods:
* Docker deployment - to run individual (yet integrated by configuration) Docker images 
* Docker Compose deployment - a tool for defining and running multi-container Docker applications
* Kompose deployment


## Build the Suricata-IDS image

`$ docker build --no-cache -t suricata .`


## Get the ELK official images

`$ docker pull docker.elastic.co/logstash/logstash:6.5.4` or simply 
`$ docker pull logstash:6.5.4`

`$ docker pull docker.elastic.co/elasticsearch/elasticsearch:6.5.4` or simply 
`$ docker pull elasticsearch:6.5.4`

`$ docker pull docker.elastic.co/kibana/kibana:6.5.4` or simply 
`$ docker pull kibana:6.5.4`


## Run SELK containers

// Run Elasticsearch Docker image: https://www.elastic.co/guide/en/elasticsearch/reference/6.4/docker.html

`$ docker run --rm -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --hostname=elastic --name=elastic --network=host --mount source=elastic,destination=/usr/share/elasticsearch/data -t docker.elastic.co/elasticsearch/elasticsearch:6.5.4`


// Run Kibana Docker image: https://hub.docker.com/_/kibana

`$ docker run --rm -e ELASTICSEARCH_URL="http://localhost:9200" --hostname=kibana --name=kibana --network=host -p 5601:5601 -t docker.elastic.co/kibana/kibana:6.5.4`


// Run Logstash Docker image: https://www.elastic.co/guide/en/logstash/current/docker-config.html

`$ docker run --rm -d -e xpack.monitoring.elasticsearch.url="http://localhost:9200" --hostname=logstash --name=logstash --network=host -v ~/tng-industrial-pilot/vnfs/ids-suricata/logstash.conf:/usr/share/logstash/config/logstash.conf -t docker.elastic.co/logstash/logstash:6.5.4`


// Run Suricata Docker image: created from local Dockerfile

`$ docker run -d --rm --network=host --hostname=suricata --name=suricata -t suricata:4.1.2`


Watch ASCIINEMA: https://asciinema.org/a/AyKiS96LTtR08hLps7o7fDqCD


## SELK Manual deployment via Docker Compose

`$ docker-compose up`
Watch ASCIINEMA: https://asciinema.org/a/sDZlFo3lIRaMvHCy1bJxLalwR


## Convert 'docker-compose.yml' file to a Kubernetes resources file using Kompose

`$ kompose convert -f docker-compose.yml -o k8s-selk.yml`


## SELK Manual deployment via Kubernetes

`$ kompose --file k8s-selk.yml up`

