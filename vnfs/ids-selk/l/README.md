#

## Get the official LOGSTASH Docker Imag

`$ docker pull docker.elastic.co/logstash/logstash:7.3.0`


## Create a new image to include the new Logstash configuration file

`$ docker build --progress=plain --no-cache -t logstash .` 


## How to run

`$ docker run --rm -d --network=host --hostname=logstash --name=logstash -t logstash`


# More info

* [Directory layout of Docker Images](https://www.elastic.co/guide/en/logstash/6.x/dir-layout.html)

` home = /usr/share/logstash`
` -e path.settings = /usr/share/logstash/config`
` -e path.config = /usr/share/logstash/pipeline`
` -e path.plugins = /usr/share/logstash/plugins`
` -e path.data = /usr/share/logstash/data`

