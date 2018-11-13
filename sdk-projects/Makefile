gen_emu: sonata-psa-gen-emu/project.yml sonata-psa-gen-emu/sources/nsd/sonata-psa.yml sonata-psa-gen-emu/sources/vnf/vpn/vpn-vnfd.yml sonata-psa-gen-emu/sources/vnf/fw/fw-vnf-vnfd.yml sonata-psa-gen-emu/sources/vnf/cache/cache-vnfd.yml
	@echo '* Generated the NSD/VNFDs for the emulator'

sonata-psa-gen-emu/project.yml: sonata-psa/project.yml
	mkdir -p $$(dirname $@)
	sed -r 's~^( +name:).*~\1 "sonata-psa-gen-emu"~' $^ > $@

sonata-psa-gen-emu/sources/nsd/sonata-psa.yml: sonata-psa/sources/nsd/sonata-psa.yml
	mkdir -p $$(dirname $@)
	sed -r 's~^name:.*~name: "sonata-psa-gen-emu"~' $^ > $@

sonata-psa-gen-emu/sources/vnf/vpn/vpn-vnfd.yml: sonata-psa/sources/vnf/vpn/vpn-vnfd.yml
	mkdir -p $$(dirname $@)
	sed -r 's~^( +vm_image:).*~\1 "sonata-psa/vpn"~; s~^( +vm_image_format:).*~\1 "docker"~' $^ > $@

sonata-psa-gen-emu/sources/vnf/fw/fw-vnf-vnfd.yml: sonata-psa/sources/vnf/fw/fw-vnf-vnfd.yml
	mkdir -p $$(dirname $@)
	sed -r 's~^( +vm_image:).*~\1 "sonata-psa/fw"~; s~^( +vm_image_format:).*~\1 "docker"~' $^ > $@

sonata-psa-gen-emu/sources/vnf/cache/cache-vnfd.yml: sonata-psa/sources/vnf/cache/cache-vnfd.yml
	mkdir -p $$(dirname $@)
	sed -r 's~^( +vm_image:).*~\1 "sonata-psa/cache"~; s~^( +vm_image_format:).*~\1 "docker"~' $^ > $@
