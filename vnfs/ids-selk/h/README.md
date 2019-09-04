# Flask lightweight HTTP server

## Flask CNF for SMP deployment via the SP

```
$ docker pull sonatanfv/vnf-ids-http

$ docker run --rm --name my-fl \
  -v "/usr/share/logstash/logs:/var/log/logstash" \
  -d sonatanfv/vnf-ids-http

$ docker exec -it my-fl bash
```
