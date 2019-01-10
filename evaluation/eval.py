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


# script for packaging, onboarding, and instantiating NS1 and NS2 and measuring the time (over multiple runs)
from timeit import default_timer as timer
from subprocess import run
import argparse
from emuc import EmuSrvClient, LLCMClient

srv_client = EmuSrvClient('http://127.0.0.1:4999')
llcm_client = LLCMClient('http://127.0.0.1:5000')


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="Runtime evaluation")
    parser.add_argument('-n', '-r', help="Number of evaluation runs per network service", default=1, dest='runs')
    return parser.parse_args()


def measure_times(project_path, package_path):
    times = dict()

    # start emulation
    print("Starting vim-emu")
    srv_client.start_emulation()

    # wait for it to be ready
    print("Waiting for it to be ready")
    srv_client.wait_emulation_ready(llcm_client)
    print("ready")

    # packaging
    print("Packaging")
    packaging_start = timer()
    run(['tng-pkg', '-p', project_path])
    packaging_done = timer()
    packaging_time = packaging_done - packaging_start
    times['packaging'] = packaging_time
    print("Packaging time: {}s".format(packaging_time))

    # on-board
    print("Uploading package")
    uuid = llcm_client.upload_package(package_path)
    uploading_done = timer()
    uploading_time = uploading_done - packaging_done
    times['uploading'] = uploading_time
    print("Uploading done in: {} (UUID: {})".format(uploading_time, uuid))

    # instantiate service
    print("Instantiating service")
    llcm_client.instantiate_service(uuid)
    instantiation_done = timer()
    instantiation_time = instantiation_done - uploading_done
    times['instantiation'] = instantiation_time
    times['total'] = instantiation_done - packaging_start
    print("Instantiation done in: {}".format(instantiation_time))

    # TODO: may also have to stop service in future (to stop Samba file share)
    # llcm_client.terminate_service(uuid)

    # stop emulation
    print("Stopping emulation")
    srv_client.stop_emulation()
    print("Emulation stopped")

    return times


if __name__ == '__main__':
    ns1_project = '../sdk-projects/tng-smpilot-ns1-emulator'
    ns1_package = '../sdk-projects/eu.5gtango.tng-smpilot-ns1-emulator.0.1.tgo'

    args = parse_args()

    for i in range(args.runs):
        times = measure_times(ns1_project, ns1_package)
        print(times)
