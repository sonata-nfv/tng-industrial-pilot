# Smart-Manufacturing pilot - Security Barrier (NS3)

The NS3 at SMpilot implements a security barrier between data producers (ex, a Machine Park) and its data consumers (for instance, the Machine Data Collector).

It relies on [Suricata-IDS](https://suricata-ids.org/) with a ELK processing engine. 

The SELK NS rely on the official Elastic Stack Docker Images and is composed of two Pod:

* SF CNF: Suricata CDU + Filebeat CDU

NOTE: S+F runs in promiscuous mode due to Suricata requirement to inspect all teh network traffic at the host interface

* ELK CNF: Elasticsearch CDU + Logstasha CDU + Kibana CDU

NOTE: ELK exposes its Services as 'nodePort'

## Manual deployment of NS3

`// check the K8s configuration settings

 $ kubectl config view`

`// change K8s PoP, if necessary

 $ kubectl config use-context alb-sta`

`// create a K8s dedicated Namespace, if necessary

 $ kubectl create namespace smp-ns3`

`// clone the SM-pilot repo

 $ git clone https://github.com/sonata-nfv/tng-industrial-pilot.git

 $ cd vnfs/ids-selk`

`// run the deployment of NS3

 $ kubectl apply -f kube-sf-elk.git`

`// check the running resources

 $ kubectl -n smp-ns3 get svc

 $ kubectl -n smp-ns3 get configmap

 $ kubectl -n smp-ns3 get pod

 $ kubectl -n smp-ns3 describe pod ns3-sf | more

 $ kubectl -n smp-ns3 describe pod ns3-elk | more

 $ kubectl -n smp-ns3 logs ns3-sf suricata | more

 $ kubectl -n smp-ns3 logs ns3-sf filebeat | more

 $ kubectl -n smp-ns3 logs ns3-elk logstash | more

 $ kubectl -n smp-ns3 logs ns3-elk elasticsearch | more

 $ kubectl -n smp-ns3 logs ns3-elk kibana | more`


## SP deployment of NS3

[ToBeDone]
