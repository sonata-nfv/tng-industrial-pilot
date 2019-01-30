#

## Get the official ELASTICSEARCH Docker Image

$ docker pull ubuntu
$ docker pull docker.elastic.co/elasticsearch/elasticsearch:6.6.0

## Run the ELASTICSEARCH Docker image

`$ docker run -d [-p 9200:9200 -p 9300:9300] -e "discovery.type=single-node" --hostname=elastic --name=elastic --network=host -t --mount source=elastic,destination=/usr/share/elasticsearch/data docker.elastic.co/elasticsearch/elasticsearch:6.6.0`

[ES deployemnt guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

