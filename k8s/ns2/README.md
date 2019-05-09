# Smart-Manufacturing pilot - Network Service 2 - MDC with IDS add-on

NS2 is build of two CNF's: a customized Machine Data Collector (MDC) and an Intrusion Detection System (IDS) 

## MDC
This CNF exposes a SAMBA share for the factory machinery to send EM63 formated messages. You can use the 'smbclient' to test the CIFS share - ex:

`$ smbclient -L "SAMBA-SRV"`

## IDS
This CNF contains two VDU's: 
- a Suricata-based VDU running in promiscuos mode ('hostNetwork: true')
- a Filebeat agent that ships formatted log messages generated by Suricata (`/var/logs/suricata/eve.json`) to the Logstash CNF


## Topology

`
            +-------+    +-------+
            |  MDC  |    |  IDS  |
            |  CNF  |    |  CNF  |
            +---+---+    +---+---+
                |            |
                +------+-----+
                       ^
                       |
  +--------+           |
  | EXTERN |-----------+
  | ATTACK |
  +---+----+
` 
 

## How to start

`$ kubectl apply -f ./`


## Check the deployed resources

`$ kubectl get deploy`

`$ kubectl get pod`

`$ kubectl get svc`

