#

## Get FILEBEAT official image

`docker pull docker.elastic.co/beats/filebeat:6.6.0`

## Run FILEBEAT

* Load Templates for Elasticsearch

* Load Dashboards for Kibana

`$ docker run docker.elastic.co/beats/filebeat:6.6.0 setup -E setup.kibana.host=localhost:5601 -E output.elasticsearch.hosts="localhost:9200"`

`$ docker run -d 
   --name=filebeat \
   --user=root \
   --mount src=suricata,dst=/var/log/suricata \
   filebeat /usr/share/filebeat/bin/filebeat \
      -c /etc/filebeat/filebeat.yml \
      -path.home /usr/share/filebeat \
      -path.config /etc/filebeat \
      -path.data /var/lib/filebeat \
      -path.logs /var/log/filebeat \
      [-e -strict.perms=false ]\
      [-E output.elasticsearch.enable=false ] \
      [-E output.logstash.host=["localhost:5044"]] \
      [-E setup.kibana.host=localhost:5601] ]`
