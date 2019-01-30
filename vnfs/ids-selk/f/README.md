#

## Get FILEBEAT official image

`docker pull docker.elastic.co/beats/filebeat:6.6.0`

## Run FILEBEAT

* Load Templates for Elasticsearch

* Load Dashboards for Kibana

`$ docker run docker.elastic.co/beats/filebeat:6.6.0 setup -E setup.kibana.host=localhost:5601 -E output.elasticsearch.hosts="localhost:9200"`

