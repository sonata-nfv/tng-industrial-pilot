FROM centos:7.6.1810

RUN yum -y install epel-release yum-plugin-copr && \ 
    yum -y copr enable jasonish/suricata-stable && \ 
    yum -y install suricata && \
    yum -y install rustc cargo

# Open up the permissions on /var/log/suricata so linked containers can see it. 
RUN chmod 755 /var/log/suricata && \
    usermod -aG suricata root

VOLUME /var/log/suricata

WORKDIR /usr/share/suricata

COPY suricata.yaml .

#ENTRYPOINT /usr/sbin/suricata -c suricata.yaml -S rules/*.rules -i eth0
ENTRYPOINT ["/usr/sbin/suricata"] 
CMD ["-c","suricata.yaml","-S","/usr/share/suricata/rules/*.rules","-i","eth0"]

## USAGE
## $ docker build -t sonatanfv/vnf-ids-suricata .
## $ docker run --rm --name suricata -v /var/log/suricata:/var/log/suricata -d sonatanfv/vnf-ids-suricata
## $ docker exec -it suricata bash
