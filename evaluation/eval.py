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
import requests
from time import sleep
from timeit import default_timer as timer
from subprocess import run

emuserv_url = 'http://127.0.0.1:4999/api/v1/emulation'


def measure_ns1():
    """"Measure the time for packaging, onboarding, and instantiating NS1"""

    # start vim-emu, sleep for 10s to wait until it's ready
    print("Starting vim-emu")
    response = requests.post(emuserv_url).text

    # wait until vim-emu is running (poll every 1s via http get)
    emu_running = requests.get(emuserv_url)
    while emu_running != 'true':
        sleep(1)
        emu_running = requests.get(emuserv_url).text
        print(emu_running)

    # packaging
    print("Packaging")
    start = timer()
    run(['tng-pkg', '-p', '../sdk-projects/tng-smpilot-ns1-emulator'])
    packaging_done = timer()
    packaging_time = packaging_done - start
    print(packaging_time)

    # stop emulator
    response = requests.delete(emuserv_url)


if __name__ == '__main__':
    measure_ns1()
