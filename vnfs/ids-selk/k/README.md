# Kibana

## Kibana CNF for SMP deployment via the SP

```
$ docker pull sonatanfv/vnf-ids-kibana

$ export e_vnf3_eu_5gtango_0_4_elastic9200_ip=172.17.0.2

$ docker run --name my-kb \
  -e "e_vnf3_eu_5gtango_0_4_elastic9200=${e_vnf3_eu_5gtango_0_4_elastic9200_ip}" \
  -d sonatanfv/vnf-ids-kibana

$ docker exec -it my-kb bash
```

## Standalone Kibana

Get the official KIBANA Docker Image

```$ docker pull elastic/kibana:7.3.0```

Run the KIBANA Docker image

```$ docker run --rm -d -e ELASTICSEARCH_URL="http://elasticsearch:9200" --hostname=kibana --name=kibana --network=host -t elastic/kibana:7.3.0
```

More info here: [KIBANA deployemnt guide](https://www.elastic.co/guide/en/kibana/current/index.html)

