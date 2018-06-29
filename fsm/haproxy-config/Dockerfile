FROM debian:stretch-slim
MAINTAINER SONATA

# configrurations
ENV mongo_host mongo
ENV mongo_port 27017
ENV broker_host amqp://guest:guest@broker:5672/%2F
ENV broker_exchange son-kernel
#

RUN apt-get update \
	&& apt-get install -y --no-install-recommends  python3-setuptools\
                python3-pip ssh \
		liblua5.3-0 \
		libpcre3 \
		libssl1.1 \
                && apt-get update && pip3 install paramiko \
                && apt-get install -y python3-amqp python3-amqplib \
                && pip3 install IPy setuptools wheel\
	&& rm -rf /var/lib/apt/lists/*

ENV HAPROXY_MAJOR 1.8
ENV HAPROXY_VERSION 1.8.9
ENV HAPROXY_MD5 1466cf8c1c036e376265b86df43efc89

RUN set -x \
	\
	&& buildDeps=' \
		ca-certificates \
		gcc \
		libc6-dev \
		liblua5.3-dev \
		libpcre3-dev \
		libssl-dev \
		make \
		wget \
		zlib1g-dev \
	' \
	&& apt-get update && apt-get install -y $buildDeps --no-install-recommends && rm -rf /var/lib/apt/lists/* \
	\
	&& wget -O haproxy.tar.gz "https://www.haproxy.org/download/${HAPROXY_MAJOR}/src/haproxy-${HAPROXY_VERSION}.tar.gz" \
	&& echo "$HAPROXY_MD5 *haproxy.tar.gz" | md5sum -c \
	&& mkdir -p /usr/src/haproxy \
	&& tar -xzf haproxy.tar.gz -C /usr/src/haproxy --strip-components=1 \
	&& rm haproxy.tar.gz \
	\
	&& makeOpts=' \
		TARGET=linux2628 \
		USE_LUA=1 LUA_INC=/usr/include/lua5.3 \
		USE_OPENSSL=1 \
		USE_PCRE=1 PCREDIR= \
		USE_ZLIB=1 \
	' \
	&& make -C /usr/src/haproxy -j "$(nproc)" all $makeOpts \
	&& make -C /usr/src/haproxy install-bin $makeOpts \
	\
	&& mkdir -p /usr/local/etc/haproxy \
	&& cp -R /usr/src/haproxy/examples/errorfiles /usr/local/etc/haproxy/errors \
	&& rm -rf /usr/src/haproxy \
	\
	&& apt-get purge -y --auto-remove $buildDeps

#RUN git clone --recursive https://github.com/sonata-nfv/son-sm.git
#RUN git clone --recursive https://github.com/miguelmesquita/son-security-pilot.git

ADD son-sm/son-mano-framework/son-mano-base /son-mano-base
ADD son-sm/son-sm-template /son-sm-template


#WORKDIR /son-sm/son-mano-framework/son-mano-base
#RUN python setup.py install

#WORKDIR /son-sm/son-sm-template
#RUN python setup.py install

WORKDIR /son-mano-base
Run python setup.py install

WORKDIR /son-sm-template
RUN python setup.py install

#WORKDIR /son-security-pilot/install/roles/docker-quagga/files
#COPY ansible/roles/quagga/files /etc/squid3

WORKDIR /
ADD fsm/haproxy-config /haproxy-config

WORKDIR /haproxy-config
RUN python setup.py develop

CMD ["fsm-haproxy"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
