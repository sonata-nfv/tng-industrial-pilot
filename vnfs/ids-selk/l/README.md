#

## Get the official LOGSTASH Docker Imag

`$ docker pull docker.elastic.co/logstash/logstash:6.6.0`


## Create a new image to include the new Logstash configuration file

`$ docker build --progress=plain --no-cache -t logstash .` 


## How to run

`$ docker run --network=host --hostname=logstash --name=logstash --mount src=suricata,dst=/var/log/suricata/ -d logstash`

