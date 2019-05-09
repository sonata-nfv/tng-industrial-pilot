# Smart-Manufacturing pilot - Network Service 2+ - MDC with IDS and ELK

NS2+ is build of five CNF's: 
1. a customized Machine Data Collector (MDC) 
2. a Suricata-based Intrusion Detection System (IDS) with Filebeat log shipper
3. the Logstash ETL (*)
4. the Elasticsearch TSDB (*)
5. the Kibana visualizer (*)
(*) based on official image from ES

## MDC
This CNF exposes a SAMBA share (CIFS protocol) for the factory machinery to send EM63 formated messages. You can use the 'smbclient' to test the CIFS share - ex:

`$ smbclient -L "SAMBA-SRV"`

## IDS
This CNF contains two VDU's: 
- a Suricata-based VDU running in promiscuos mode (`hostNetwork: true`)
- a Filebeat agent that ships formatted log messages generated by Suricata ('eve.json') to the Logstash CNF


## LOGSTASH
This CNF accepts input Beats (Lumberjack protocol) from the Filebeat agent instaled on the Suricata CNF, applies a convenient filter or enrich data received and outputs to Elasticsearch


## ELASTICSEARCH
This CNF is a Time Series Data Base 


## KIBANA
This CNF is a web application with dashboards for data visualization 


## Topology

`
                         +-------+    +-------+   +------+
                         |  LS   |____|  ES   |___|  KB  |
                         |  CNF  |    |  CNF  |   |  CNF |
                         +---+---+    +---+---+   +------+
                             |                        ^
                             |                        |
                             |                        | http://kibana-ip-addr:5601
            +-------+    +---+---+                    |
            |  MDC  |    |  IDS  |                    |
            |  CNF  |    |  CNF  |                    |
            +---+---+    +---+---+                    |
                |            |                        |
                +-----(+)----+                        |
                       ^                              |
                       |                              |     +----------+
  +--------+           |                              |     |          |
  | EXTERN |-----------+                              +-----+ OPERATOR |
  | ATTACK |                                                |          |
  +---+----+                                                +----------+
`
 

## How to start

`$ kubectl apply -f ./`


## Check the deployed resources

`$ kubectl get deploy`

`$ kubectl get pod`

`$ kubectl get svc`


## Access to Kibana dashboards
Get the external IP address of the running Kibana container

`$ kubectl get svc`

Go to a web browser and point to the Kibana web application: http://kibana-ip-addr:5601
