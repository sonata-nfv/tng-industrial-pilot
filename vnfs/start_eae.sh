#!/bin/bash
# starts vnf-eae and vnf-cc-database


docker run -d -p 9090:9090 --rm --name vnf-cc-database sonatanfv/vnf-cc-database:vimemu prometheus --config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/prometheus --web.console.libraries=/usr/share/prometheus/console_libraries --web.console.templates=/usr/share/prometheus/consoles
docker run -d -p 3000:3000 --rm --name vnf-eae sonatanfv/vnf-eae:vimemu
