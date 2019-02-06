#

## Get the official KIBANA Docker Image

`$ docker pull ubuntu`
`$ docker pull docker.elastic.co/kibana/kibana:6.6.0`

## Run the KIBANA Docker image

`$ docker run --rm -d -e ELASTICSEARCH_URL="http://localhost:9200" --hostname=kibana --name=kibana --network=host -t docker.elastic.co/kibana/kibana:6.6.0`

More info here: [KIBANA deployemnt guide](https://www.elastic.co/guide/en/kibana/current/index.html)

