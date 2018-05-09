EXTRA_SONVALIDATE_ARGS:=
EXTRA_SONPACKAGE_ARGS:=

#all: package package-emu
all: package

#docker-images: docker-image-squid docker-image-fw docker-image-vpn docker-image-cache

#docker-image-squid:
#	cd install/roles/docker-squid/files && \
#	  docker build -t sonata-psa/squid .

#docker-image-haproxy:
#	cd install/roles/docker-haproxy/files && \
#	  docker build -t sonata-psa/haproxy .

# docker-image-snort:
# 	docker pull glanf/snort

#docker-image-vpn:
#	cd install/roles/docker-openvpn/files && \
#		docker build -t sonata-psa/vpn .

#docker-image-fw:
#	cd install/roles/docker-firewall/files && \
#	  docker build -t sonata-psa/fw .
#
#docker-image-cache:
#	cd install/roles/docker-addblk/files && \
#          docker build -t sonata-psa/cache .

package:
	son-validate $(EXTRA_SONVALIDATE_ARGS) --debug -s -i -t --project projects/tango-etsi-plug-vrouter-fsm
	son-package $(EXTRA_SONPACKAGE_ARGS) --project projects/tango-etsi-plug-vrouter-fsm


#package-emu: docker-images gen_emu
#package-emu:
#	son-validate $(EXTRA_SONVALIDATE_ARGS) --debug -s -i -t --project projects/sonata-psa-gen-emu
#	son-package $(EXTRA_SONPACKAGE_ARGS) --project projects/sonata-psa-gen-emu

#gen_emu:
#	$(MAKE) -C projects gen_emu

#.PHONY: gen_emu docker-images
