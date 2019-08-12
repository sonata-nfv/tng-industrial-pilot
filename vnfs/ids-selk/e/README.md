#

## Get the official ELASTICSEARCH Docker Image

$ docker pull ubuntu
$ docker pull docker.elastic.co/elasticsearch/elasticsearch:7.3.0

## Run the ELASTICSEARCH Docker image

`$ docker run --rm -d [-p 9200:9200 -p 9300:9300] -e "discovery.type=single-node" --hostname=elastic --name=elastic --network=host --mount source=elastic,destination=/usr/share/elasticsearch/data -t docker.elastic.co/elasticsearch/elasticsearch:7.3.0`


* `path.home=/usr/share/elasticsearch`
* `path.conf=/usr/share/elasticsearch/config`
* `published ports: -p 9200:9200 -p 9300:9300`

More info here: [ES deployemnt guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

