SELK

This page guides you through the process to deploy a combination of Suricata-IDS with ELK using the following methods:
* Docker deployment - to run individual (yet integrated by configuration) Docker images 
* Docker Compose deployment - a tool for defining and running multi-container Docker applications
* Kompose deployment


# Build the Suricata-IDS image

`$ docker build --progress=plain --no-cache -t ce7suricata:4.1.2 .`

// Run SURICATA microservice: created from local Dockerfile

`$ docker run -d --rm --network=host --hostname=suricata --name=suricata -t ce7suricata:4.1.2`

// Directory structure

* BIN: /usr/sbin/suricata

* CONFIG: "-c /etc/suricata/suricata.yaml"

* RULES:  /usr/share/suricata/rules/ (instead of "/var/lib/suricata/rules/suricata.rules")

* LOGs: /var/log/suricata

* TEST: /usr/sbin/suricata -T -c /etc/suricata/suricata.yaml"


# Run ELK containers

## Run [ELASTICSEARCH](https://www.elastic.co/guide/en/elasticsearch/reference/6.6/docker.html) microservice

`$ docker pull docker.elastic.co/elasticsearch/elasticsearch:6.6.0` or simply 

`$ docker pull elasticsearch:6.6.0`

`$ docker run --rm -d [-p 9200:9200 -p 9300:9300] -e "discovery.type=single-node" --hostname=elastic --name=elastic --network=host --mount source=elastic,destination=/usr/share/elasticsearch/data -t docker.elastic.co/elasticsearch/elasticsearch:6.6.0`


## Run [KIBANA](https://hub.docker.com/_/kibana) microservice

`$ docker pull docker.elastic.co/kibana/kibana:6.6.0` or simply 

`$ docker pull kibana:6.6.0`

`$ docker run --rm -d -e ELASTICSEARCH_URL="http://localhost:9200" --hostname=kibana --name=kibana --network=host [-p 5601:5601] -t docker.elastic.co/kibana/kibana:6.6.0`


## Run [FILEBEAT](https://www.elastic.co/guide/en/beats/filebeat/current/index.html) microservice

`$ docker pull docker.elastic.co/beats/filebeat:6.6.0` or simply

`$ docker pull filebeat:6.6.0

`$ docker build --progress=plain -f ./Dockerfile -t filebeat .`

`$ docker run --rm -d \
  --name=filebeat  \
  --user=root \
  --net=host \
  --mount src=suricata,dst=/var/log/suricata/ \
  -t filebeat /usr/share/filebeat/filebeat \
    -e -strict.perms=false \
    -E output.elasticsearch.enabled=false \
    -E output.logstash.hosts=["localhost:5044"] \
    -E setup.kibana.host=localhost:5601` 


NOTE: The 'filebeat' executable file contains:

`exec /usr/share/filebeat/bin/filebeat \
  -path.home /usr/share/filebeat \
  -path.config /etc/filebeat \
  -path.data /var/lib/filebeat \
  -path.logs /var/log/filebeat \
  "$@"`


## Run [LOGSTASH](https://www.elastic.co/guide/en/logstash/current/docker-config.html) microservice

`$ docker pull docker.elastic.co/logstash/logstash:6.6.0` or simply 

`$ docker pull logstash:6.6.0`

`$ docker run --rm -d --hostname=logstash --name=logstash --network=host -t logstash`

Other parameters:

`-e xpack.monitoring.elasticsearch.url="http://localhost:9200"` - already included in 'logastash.yml' 

`-t docker.elastic.co/logstash/logstash:6.6.0`


# DEMO

Watch [ASCIINEMA](https://asciinema.org/a/AyKiS96LTtR08hLps7o7fDqCD)



# SELK Manual deployment via Docker Compose and Kubernetes


## SELK Manual deployment via Docker Compose

`$ docker-compose up`
Watch ASCIINEMA: https://asciinema.org/a/sDZlFo3lIRaMvHCy1bJxLalwR


## Convert 'docker-compose.yml' file to a Kubernetes resources file using Kompose

`$ kompose convert -f docker-compose.yml -o k8s-selk.yml`


## SELK Manual deployment via Kubernetes

`$ kompose --file k8s-selk.yml up`

