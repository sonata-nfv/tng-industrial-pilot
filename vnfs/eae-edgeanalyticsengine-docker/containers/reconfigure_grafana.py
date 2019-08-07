#!/usr/bin/env python3

#  Copyright (c) 2018 5GTANGO, Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the SONATA-NFV, 5GTANGO, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).


# use the values passed via env vars to dynamically replace/reconfigure the Grafana data source or dashboard


import os
import logging
import oyaml as yaml        # ordered yaml to avoid reordering of config files


log = logging.getLogger(__name__)


# get the IP and port of the CC's Prometheus DB from env var
# var name format: vendor_name_version_cp-id_ip/port
# see https://github.com/sonata-nfv/tng-industrial-pilot/wiki/Integration-with-SP
cc_db_var_name_vimemu = "eu.5gtango_smpilot-cc_0.1_prometheus"
cc_db_var_name_k8s = "smpilot_cc_eu_5gtango_0_1_prometheus"
log.info("Reading IP and port of {} or {} from env vars".format(cc_db_var_name_vimemu, cc_db_var_name_k8s))
cc_db_ip = os.getenv(cc_db_var_name_k8s + "_ip", os.getenv(cc_db_var_name_vimemu + "_ip", "localhost"))
cc_db_port = os.getenv(cc_db_var_name_k8s + "_port", os.getenv(cc_db_var_name_vimemu + "_port", "9090"))
cc_db_url = "http://{}:{}".format(cc_db_ip, cc_db_port)

# use that to replace the URL in the configuration
datasource_path = "/etc/grafana/provisioning/datasources/datasource.yml"
log.info("Updating configuration in {} accordingly".format(datasource_path))
f_r = open(datasource_path, "r")
ds = yaml.full_load(f_r)
ds['datasources'][0]['url'] = cc_db_url
f_r.close()
f_w = open(datasource_path, "w")
log.debug("Replacing datasource URL")
f_w.write(yaml.safe_dump(ds))
f_w.close()

log.info("Done updating Grafana configurations")
