# Filebeat data shipper

## Filebeat CNF for SMP deployment via SP

```
$ docker pull sonatanfv/vnf-ids-filebeat

$ export lh_vnf2_eu_5gtango_0_4_logstash5044_ip=172.31.0.4

$ export k_vnf4_eu_5gtango_0_4_kibana5601_ip=172.17.0.3

$ docker run --rm --name my-fb \
  -e "LOGSTASH_HOSTS=http://${lh_vnf2_eu_5gtango_0_4_logstash5044_ip}:5044" \
  -e "KIBANA_HOSTS=http://${k_vnf4_eu_5gtango_0_4_kibana5601_ip}:5601" \
  -v /var/log/suricata:/usr/share/filebeat/logs \
  -d sonatanfv/vnf-ids-filebeat

$ docker exec -it my-fb bash

```

## Standalone Filebeat

Get FILEBEAT official image

```docker pull docker.elastic.co/beats/filebeat:7.3.1```

Run FILEBEAT

* Default configuration: Load Templates for Elasticsearch and Load Dashboards for Kibana

```$ docker run docker.elastic.co/beats/filebeat:7.3.1 setup -E setup.kibana.host=kibana:5601 -E output.elasticsearch.hosts="elasticsearch:9200"```

* Startup configuration for SELK NS

```$ docker run -d --rm \
   --hostname=filebeat \
   --name=filebeat \
   --user=root \
   --net=host \
   --mount src=suricata,dst=/var/log/suricata \
   -t u16filebeat \
      /usr/share/filebeat/bin/filebeat \
      -c /etc/filebeat/filebeat.yml \
      -path.home /usr/share/filebeat \
      -path.config /etc/filebeat \
      -path.data /var/lib/filebeat \
      -path.logs /var/log/filebeat \
      [-e -strict.perms=false ]\
      [-E output.elasticsearch.enable=false ] \
      [-E output.logstash.host=["localhost:5044"]] \
      [-E setup.kibana.host=localhost:5601] ]```


```
# filebeat test config

Config OK```

```
# filebeat test output

logstash: localhost:5044...
  connection...
    parse host... OK
    dns lookup... OK
    addresses: 127.0.0.1
    dial up... OK
  TLS... WARN secure connection disabled
  talk to server... OK```

