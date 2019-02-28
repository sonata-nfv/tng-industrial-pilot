#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2018 5GTANGO, Weidmüller, Paderborn University
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
# Neither the name of the SONATA-NFV, 5GTANGO, Weidmüller, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).
"""
    File name: em63.py
    Description: Contains features for using Euromap 63 communication protocol.
    Version: 2019-02-28
    Python Version 3.6.7
    Editor: Spyder (indentation characters: 4 spaces)
    Maintainer: Marcel Müller <Marcel.Mueller@weidmueller.com>
    Copyright: 2018, Marcel Müller, Weidmüller Group, Detmold, Germany
"""
import os


# Check if file exists and remove it
def rmFile(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError:
            print("Exception detected while deleting a file: ", filename)
            pass
