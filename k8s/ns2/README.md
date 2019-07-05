# Smart-Manufacturing pilot - Network Service 2 - Machine Data Collector

NS2 is build of one CNF: a customized Machine Data Collector (MDC) 

## MDC
This CNF exposes a SAMBA share for the factory machinery to send EM63 formated messages. You can use the 'smbclient' to test the CIFS share - ex:

`$ smbclient -L "SAMBA-SRV"`


## How to start

`$ kubectl apply -f ./`


## Check the deployed resources

`$ kubectl get deploy`

`$ kubectl get pod`

`$ kubectl get svc`


