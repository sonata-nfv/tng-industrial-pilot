FROM centos:7.6.1810

RUN yum -y install epel-release yum-plugin-copr && \ 
    yum -y copr enable jasonish/suricata-stable && \ 
    yum -y install suricata 

# Open up the permissions on /var/log/suricata so linked containers can see it. 
RUN chmod 755 /var/log/suricata 

VOLUME /var/log/suricata

COPY suricata.yaml /usr/share/suricata

ENTRYPOINT ["/usr/sbin/suricata"] 

# YOU MUST CHANGE THE NETWORK INTERFACE NAME TO YOUR's
CMD ["-c","/usr/share/suricata/suricata.yaml","-i","eth0"]

## USAGE
## $ docker build -t sonatanfv/vnf-ids-suricata .
## $ docker run --rm --name suricata -v /var/log/suricata:/var/log/suricata -d sonatanfv/vnf-ids-suricata
## $ docker exec -it suricata bash
