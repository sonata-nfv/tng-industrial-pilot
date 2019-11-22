# Logstash

## Logstash CNF for SMP deployment via the SP

```
$ docker pull sonatanfv/vnf-ids-logstash

$ export e_vnf3_eu_5gtango_0_8_elastic9200_ip=172.17.0.2

$ docker run --rm --name my-ls \
  -e "ELASTICSEARCH_HOSTS=http://${e_vnf3_eu_5gtango_0_8_elastic9200_ip}:9200" \
  -d sonatanfv/vnf-ids-logstash

$ docker exec -it my-ls bash

```

## Standalone Logstash

Get the official LOGSTASH Docker Image

```$ docker pull elastic/logstash:7.4.2```


Create a new image to include the new Logstash configuration file

```$ docker build --progress=plain --no-cache -t logstash .```


Run the image

```$ docker run --rm -d --network=host --hostname=logstash --name=logstash -t logstash```


More info

* [Directory layout of Docker Images](https://www.elastic.co/guide/en/logstash/6.x/dir-layout.html)

` home = /usr/share/logstash`
` -e path.settings = /usr/share/logstash/config`
` -e path.config = /usr/share/logstash/pipeline`
` -e path.plugins = /usr/share/logstash/plugins`
` -e path.data = /usr/share/logstash/data`

