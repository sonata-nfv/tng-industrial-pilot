FROM ubuntu
MAINTAINER son-install@5gtango.eu

RUN apt-get update && apt-get install -y quagga quagga-doc
RUN apt-get install -y openssh-server

RUN mkdir /var/run/sshd
RUN useradd -ms /bin/bash tango
RUN echo 'tango:t4ng0' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

WORKDIR /
ADD config /quagga-config

WORKDIR /quagga-config

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
