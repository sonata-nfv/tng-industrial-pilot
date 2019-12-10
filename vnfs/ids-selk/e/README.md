# Elasticsearch

## Build a customized ES image

```
$ docker build -t vnf-ids-elasticsearch .
$ docker run --rm --name elasticsearch -d vnf-ids-elasticsearch
$ docker exec -it elasticsearch bash
```

## Manual instantiation of Elasticsearch CNF used in SMPilot

```
$ docker pull sonatanfv/vnf-ids-elasticsearch

$ docker run --rm --name my-es \
  -d sonatanfv/vnf-ids-elasticsearch

$ docker exec -it my-es bash

$ docker inspect my-es | grep -i ipaddress

172.17.0.2
```

## Manual instantiation of a standalone Elasticsearch

Get the official ELASTICSEARCH Docker Image

```$ docker pull elastic/elasticsearch:7.4.2```

Run the ELASTICSEARCH Docker image

```$ docker run --rm -d [-p 9200:9200 -p 9300:9300] -e "discovery.type=single-node" --hostname=elastic --name=elastic --network=host --mount source=elastic,destination=/usr/share/elasticsearch/data -t docker.elastic.co/elasticsearch/elasticsearch:7.4.2```


* `path.home=/usr/share/elasticsearch`
* `path.conf=/usr/share/elasticsearch/config`
* `published ports: -p 9200:9200 -p 9300:9300`

More info here: [ES deployemnt guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

