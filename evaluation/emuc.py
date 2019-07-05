#  Copyright (c) 2018 SONATA-NFV, 5GTANGO, Paderborn University
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
# This work has been performed in the framework of the SONATA project,
# funded by the European Commission under Grant number 671517 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.sonata-nfv.eu).
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).

# copied from https://github.com/sonata-nfv/tng-sdk-benchmark/blob/master/src/tngsdk/benchmark/pdriver/vimemu/emuc.py
import requests
import time
import json
import logging

LOG = logging.getLogger(__name__)


class EmuSrvClient(object):

    def __init__(self, endpoint):
        self.emu_endpoint = "{}/api/v1/emulation".format(endpoint)
        LOG.debug("Initialized EmuSrv client for {}".format(endpoint))

    def check_platform_ready(self):
        try:
            r = requests.get(self.emu_endpoint)
        except BaseException as ex:
            LOG.debug(ex)
            raise BaseException("con't connect to tng-bench-emusrv ")
        if r.status_code != 200:
            raise BaseException("tng-bench-emusrv not ready")
        if r.text.strip() != "false":
            raise BaseException("emulation server not empty")

    def start_emulation(self):
        try:
            r = requests.post(self.emu_endpoint)
        except BaseException as ex:
            LOG.debug(ex)
            raise BaseException("con't connect to tng-bench-emusrv ")
        if r.status_code != 201:
            raise BaseException(
                "tng-bench-emusrv couldn't start emulation")

    def stop_emulation(self):
        try:
            r = requests.delete(self.emu_endpoint)
        except BaseException as ex:
            LOG.debug(ex)
            raise BaseException("con't connect to tng-bench-emusrv ")
        if r.status_code != 200:
            raise BaseException(
                "tng-bench-emusrv couldn't stop emulation")

    def wait_emulation_ready(self, llcmc, timeout=60):
        for i in range(0, timeout):
            try:
                LOG.info("Waiting for emulator LLCM ... {}/{}"
                         .format(i, timeout))
                r = llcmc.list_packages()
                if r.status_code == 200:
                    LOG.info("Emulator LLCM ready")
                    return True
            except BaseException:
                pass  # ignore connection failures
            time.sleep(1)  # wait for retry
        raise BaseException("Timeout. Emulation LLCM was not ready in time")


class LLCMClient(object):

    def __init__(self, endpoint):
        self.pkg_endpoint = "{}/packages".format(endpoint)
        self.nsi_endpoint = "{}/instantiations".format(endpoint)
        LOG.debug("Initialized LLCM client for {}".format(endpoint))

    def list_packages(self):
        return requests.get(self.pkg_endpoint)

    def upload_package(self, pkg_path):
        LOG.info("On-boarding to LLCM: {}".format(pkg_path))
        with open(pkg_path, "rb") as f:
            data = {"package": f.read()}
            t_start = time.time()
            r = requests.post(
                self.pkg_endpoint, files=data)
            self._t_onboarding = time.time() - t_start
            if r.status_code == 201:
                return json.loads(r.text).get("service_uuid")
            raise BaseException("Error during on-boarding.")

    def instantiate_service(self, uuid):
        LOG.info("Instantiating NS: {}".format(uuid))
        data = {"service_uuid": uuid}
        t_start = time.time()
        r = requests.post(
            self.nsi_endpoint, json=data)
        self._t_instantiation = time.time() - t_start
        if r.status_code == 201:
            return json.loads(r.text).get("service_instance_uuid")
        raise BaseException("Error during NS instantiation.")

    def terminate_service(self, uuid):
        LOG.info("Terminating NS: {}".format(uuid))
        data = {"service_instance_uuid": uuid}
        r = requests.delete(
            self.nsi_endpoint, json=data)
        if r.status_code == 200:
            return r.text
        raise BaseException("Error during NS termination.")

    def store_stats(self, path):
        """
        Store collected statistics as JSON.
        """
        stats = {
            "t_onboarding": self._t_onboarding,
            "t_instantiation": self._t_instantiation
        }
        LOG.debug("Writing LLCM stats: {}".format(path))
        with open(path, 'w') as f:
            json.dump(stats, f)
