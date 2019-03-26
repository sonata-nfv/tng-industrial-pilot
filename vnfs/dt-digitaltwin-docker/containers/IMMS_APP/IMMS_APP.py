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
    File name: IMMS_APP.py
    Description: Injection Moulding Machine Simulator (IMMS)
    Version: 2018-12-28
    Python Version: 3.6.7
    Editor: Spyder (indentation characters: 4 spaces)
    Maintainer: Marcel Müller <Marcel.Mueller@weidmueller.com>
    Copyright: 2018, Marcel Müller, Weidmüller Group, Detmold, Germany
"""

import math
import re
import os
import sys
import time
import datetime
import threading
import argparse
from statemachine import StateMachine, State
from flask import Flask, render_template, request
from em63 import rmFile
import plotly
import plotly.graph_objs as go
import numpy as np

app = Flask(__name__)

# User inputs
# User inputs: variable values
varSetCntMld = 0  # Number of moulds per tool, e.g., 12
varSetCntPrt = 0  # Number of parts to be produced, e.g. 50000 parts
varSetTimCyc = 0  # Cycle time set
# User inputs: variable names
txtSetCntMld = 'SetCntMld'
txtSetCntPrt = 'SetCntPrt'
txtSetTimCyc = 'SetTimCyc'
# User inputs: variable description
desSetCntMld = ',N,5,0,1,"-","Number of Cavities Run";'
desSetCntPrt = ',N,10,0,1,"-","Piece Counter Setpoint";'
desSetTimCyc = ',N,3,2,1,"s","Overall Cycle Time Setpoint.";'

# Only Outputs
# Only Outputs: variable values
varDATE = 0  # HH:MM:SS
varTIME = 0  # YYYYMMDD
varATActSimPara1 = 0  # Constant value from formATActSimPara1
varATActSimPara2 = 0
varActStsMach = '0U000'  # Machine state
varActCntCyc = 0  # Actual number of cycles already done
varActCntPrt = 0  # Actual number of parts already produced
varActTimCyc = 0  # Actual cycle time
# Only Outputs: variable names
txtDATE = 'DATE'
txtTIME = 'TIME'
txtATActSimPara1 = '@ActSimPara1'
txtATActSimPara2 = '@ActSimPara2'
txtActCntCyc = 'ActCntCyc'
txtActCntPrt = 'ActCntPrt'
txtActStsMach = 'ActStsMach'
txtActTimCyc = 'ActTimCyc'
# Only Outputs: variable desc
desDATE = 'xxx'
desTIME = 'xxx'
desATActSimPara1 = ',N,5,0,0,"-","Actual Simulated Parameter 1";'
desATActSimPara2 = ',N,8,4,0,"-","Actual Simulated Parameter 2";'
desActCntCyc = ',N,10,0,0,"Cycles","Actual Cycle Count";'
desActCntPrt = ',N,10,0,0,"Part","Piece Counter";'
desActStsMach = ',A,5,0,0,"-","Actual Machine Status";'
desActTimCyc = ',N,8,4,0,"s","Actual Cycle Time";'

# Parameters used for creating varATActSimPara2
varATActSimPara2period = 0  # Sine periodic time from formATActSimPara2period
varATActSimPara2amplitude = 0  # Sine amplitude from formATActSimPara2amplitude
varATActSimPara2phase = 0  # Sine phase shift from formATActSimPara2phase
varATActSimPara2offset = 0  # Sine offset from formATActSimPara2offset

varPlotATActSimPara = 0
varFormState = 'none'

varFormEM63path = ''
varFormEM63user = ''
varFormEM63pass = ''

session = 0  # Increment session for further em63 sessions

# Get configuration from environment varialbe (or use the old default)
filepathEM63 = os.environ.get("DT_EM63_SHARE", "/home/marcel/em63/")

valEM63 = [
        [txtDATE, varDATE, desDATE],
        [txtTIME, varTIME, desTIME],
        [txtATActSimPara1, varATActSimPara1, desATActSimPara1],
        [txtATActSimPara2, varATActSimPara2, desATActSimPara2],
        [txtActCntCyc, varActCntCyc, desActCntCyc],
        [txtActCntPrt, varActCntPrt, desActCntPrt],
        [txtActStsMach, varActStsMach, desActStsMach],
        [txtActTimCyc, varActTimCyc, desActTimCyc],
        [txtSetCntMld, varSetCntMld, desSetCntMld],
        [txtSetCntPrt, varSetCntPrt, desSetCntPrt],
        [txtSetTimCyc, varSetTimCyc, desSetTimCyc]
        ]

# Create static content for GETID
txtGETID = ''
for index in range(2, len(valEM63)):
    txtGETID = txtGETID + valEM63[index][0] + valEM63[index][2] + '\n'

# Static Content for GETINFO if no text file available
txtGETINFO = """MachVendor,	"xxx";
MachNbr,	"xxx";
MachDesc,	"xxx";
ContrType,	"xxx";
ContrVersion,	"xxx";
Version,	"xxx";
MaxJobs,	x;
MaxEvents,
    CURRENT_ALARMS	x
    ALARMS	x
    CHANGES	x;
MaxReports,	x;
MaxArchives,	x;
InjUnitNbr,	x;
MaterialNbr,	"x";
CharDef,	"x";
MaxSessions,	x;
ActiveJobs,
    "x";
ActiveReports,	;
ActiveEvents,	;
"""


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    return render_template('setup.html')


@app.route('/monitoring')
def monitoring():
    return render_template('monitoring.html')


@app.route('/plotActSimPara')
def plotActSimPara():
    return render_template('plotActSimPara.html')


@app.route('/plotActCntCyc')
def plotActCntCyc():
    return render_template('plotActCntCyc.html')


@app.route('/resultSimPara', methods=['GET', 'POST'])
def resultSimPara():
    global varATActSimPara1
    global varATActSimPara2period, varATActSimPara2amplitude
    global varATActSimPara2phase, varATActSimPara2offset, varPlotATActSimPara
    if request.form['formPlotATActSimPara'] == '1':
        varPlotATActSimPara = 1
    else:
        varPlotATActSimPara = 0
    varATActSimPara1 = int(request.form['formATActSimPara1'])
    varATActSimPara2period = float(request.form['formATActSimPara2period'])
    varATActSimPara2amplitude = \
        float(request.form['formATActSimPara2amplitude'])
    varATActSimPara2phaseStr = request.form['formATActSimPara2phase']
    if varATActSimPara2phaseStr == '-pi':
        varATActSimPara2phase = -1*math.pi
    elif varATActSimPara2phaseStr == '-pi/2':
        varATActSimPara2phase = -1*math.pi/2
    elif varATActSimPara2phaseStr == '-pi/4':
        varATActSimPara2phase = -1*math.pi/4
    elif varATActSimPara2phaseStr == '0':
        varATActSimPara2phase = 0.0
    elif varATActSimPara2phaseStr == 'pi/2':
        varATActSimPara2phase = math.pi/2
    elif varATActSimPara2phaseStr == 'pi/4':
        varATActSimPara2phase = math.pi/4
    elif varATActSimPara2phaseStr == 'pi':
        varATActSimPara2phase = math.pi
    else:
        varATActSimPara2phase = 0

    varATActSimPara2offset = float(request.form['formATActSimPara2offset'])
    print("@ActSimPara1 = ", varATActSimPara1)
    print("@ActSimPara2_period = ", varATActSimPara2period)
    print("@ActSimPara2_amplitude = ", varATActSimPara2amplitude)
    print("@ActSimPara2_phase = ", varATActSimPara2phaseStr)
    print("@ActSimPara2_phase (DEZ) = ", varATActSimPara2phase)
    print("@ActSimPara2_offset = ", varATActSimPara2offset)
    return render_template("result.html", result=result)


@app.route('/result', methods=['GET', 'POST'])
def result():
    global varActStsMach, varSetCntMld, varSetCntPrt, varSetTimCyc
    varSetCntMld = int(request.form['formSetCntMld'])
    varSetCntPrt = int(request.form['formSetCntPrt'])
    varSetTimCyc = float(request.form['formSetTimCyc'])
    print("SetCntMld = ", varSetCntMld)
    print("SetCntPrt = ", varSetCntPrt)
    print("SetTimCyc = ", varSetTimCyc)
    return render_template("result.html", result=result)


@app.route('/resultState', methods=['GET', 'POST'])
def resultState():
    global varFormState
    varFormState = request.form['formState']
    print("varFormState = ", varFormState)
    return render_template("result.html", result=result)


@app.route('/resultNetwork', methods=['GET', 'POST'])
def resultNetwork():
    print("Currently not supported. Please use /etc/network/interfaces")
    return render_template("result.html", result=result)


@app.route('/resultEM63', methods=['GET', 'POST'])
def resultEM63():
    global varFormEM63path, varFormEM63user, varFormEM63pass, filepathEM63
    varFormEM63path = request.form['formEM63path']
    varFormEM63user = request.form['formEM63user']
    varFormEM63pass = request.form['formEM63pass']
    print("EM63 Path = ", varFormEM63path)
    print("EM63 User = ", varFormEM63user)
    print("EM63 Pass = ", varFormEM63pass)
    return render_template("result.html", result=result)


def _start_flask():
    # Make the server configurable through environment variables
    # Default localhost: http://127.0.0.1:5000
    listen_host = os.environ.get("DT_WEB_LISTEN", "127.0.0.1")
    listen_port = os.environ.get("DT_WEB_PORT", 5000)
    app.run(host=listen_host, port=listen_port)
    return


def start_webapp():
    thread = threading.Thread(target=_start_flask)
    thread.daemon = True
    thread.start()
    return


def _start_EM63():
    while 0 < 1:
        run_EM63()


def start_EM63():
    thread2 = threading.Thread(target=_start_EM63)
    thread2.daemon = True
    thread2.start()
    return


def make_ATActSimPara2(t1):
    global varATActSimPara2period, varATActSimPara2amplitude
    global varATActSimPara2phase, varATActSimPara2offset
    if varATActSimPara2period != 0:
        varATActSimPara2 = varATActSimPara2amplitude * \
            math.sin(2 * math.pi / varATActSimPara2period * t1 +
                     varATActSimPara2phase) + varATActSimPara2offset
    else:
        varATActSimPara2 = 0
    varATActSimPara2 = format(varATActSimPara2, '8.4f')
    return varATActSimPara2


def production():
    global varActStsMach, varSetCntMld, varSetCntPrt, varSetTimCyc
    global varActCntPrt, varActCntCyc, varATActSimPara2, varActTimCyc
    global varFormState
    if 0 < 1:
        if varFormState == 'formStatepause':
            return IMM1.e_pause()
        if varFormState == 'formStateerror':
            return IMM1.e_error()
        if varPlotATActSimPara == 1:
            # List for graph plottig
            sinPlotX = []
            sinPlotY = []
            sinPlotY2 = []
            sinPlotY3 = []
        while varActCntPrt < varSetCntPrt:
            varActStsMach = '0A000'
            if varFormState == 'formStatepause':
                return IMM1.e_pause()
            if varFormState == 'formStateerror':
                return IMM1.e_error()
            # Start Timer for ActTimCyc
            # time.clock()works on win (is wall-clock),
            # but not linux because sleep time is not counted => time.monotonic
            t1 = time.monotonic()
            # Sine function for @ActSimPara2
            varATActSimPara2 = make_ATActSimPara2(t1)
            if varPlotATActSimPara == 1:
                # Append content to list for graph plotting
                # sinPlotX.append(float(t1))
                sinPlotX.append(datetime.datetime.now())
                sinPlotY.append(float(varATActSimPara2))
                sinPlotY2.append(float(varATActSimPara1))
                sinPlotY3.append(float(varActTimCyc))
            # Part/Cycle counter
            varActCntCyc = varActCntCyc + 1
            time.sleep(varSetTimCyc)
            varActCntPrt = int(varSetCntMld * varActCntCyc)
            # Stop Timer for ActTimCyc
            t2 = time.monotonic()
            dt = t2 - t1
            varActTimCyc = format(dt, '8.4f')
            valEM63print()
            if varPlotATActSimPara == 1:
                plotAllLocal(sinPlotX, sinPlotY, sinPlotY2, sinPlotY3)
            if varActCntPrt >= varSetCntPrt:
                print("Job finished...")
                return


def finished():
    global varFormState, varActStsMach, varSetCntMld, varSetCntPrt
    global varSetTimCyc, varActCntPrt, varActCntCyc, varActTimCyc
    while 0 < 1:
        if varFormState == 'formStateidle':
            varFormState = 'none'
            varSetCntMld = 0
            varSetCntPrt = 0
            varSetTimCyc = 0
            varActCntCyc = 0
            varActCntPrt = 0
            varActTimCyc = 0
            return
        else:
            time.sleep(1)  # waiting


# Check if necessary or not
# def errorState():
#    while 0<1:
#        if varFormState == 'formStateproduction':
#            #IMM1.e_confirm()
#            return;
#        else:
#            time.sleep(1)
#
# def pauseState():
#    while 0<1:
#        if varFormState == 'formStateproduction':
#            #IMM1.e_proceed()
#            return;
#        else:
#            time.sleep(1)
#
# def machineSetup():
#    while 0<1:
#        if varFormState == 'formStateproduction':
#            return;
#        else:
#            time.sleep(1)


def valEM63refresh():
    global varActStsMach, varSetCntMld, varSetCntPrt, varSetTimCyc
    global varActCntPrt, varActCntCyc, varActTimCyc, valEM63
    global varATActSimPara1, varATActSimPara2
    valEM63[0][1] = varDATE
    valEM63[1][1] = varTIME
    valEM63[2][1] = varATActSimPara1
    valEM63[3][1] = varATActSimPara2
    valEM63[4][1] = varActCntCyc
    valEM63[5][1] = varActCntPrt
    valEM63[6][1] = varActStsMach
    valEM63[7][1] = varActTimCyc
    valEM63[8][1] = varSetCntMld
    valEM63[9][1] = varSetCntPrt
    valEM63[10][1] = varSetTimCyc
    return


def valEM63print():
    global varActStsMach, varSetCntMld, varSetCntPrt, varSetTimCyc
    global varActCntPrt, varActCntCyc, varActTimCyc
    global valEM63, varATActSimPara1, varATActSimPara2
    print("---------------------------------------------")
    print("DATE = ", varDATE)
    print("TIME = ", varTIME)
    print("@ActSimPara1 = ", varATActSimPara1)
    print("@ActSimPara2 = ", varATActSimPara2)
    print("ActCntCyc = ", varActCntCyc)
    print("ActCntPrt = ", varActCntPrt)
    print("ActStsMach = ", varActStsMach)
    print("ActTimCyc = ", varActTimCyc)
    print("SetCntMld = ", varSetCntMld)
    print("SetCntPrt = ", varSetCntPrt)
    print("SetTimCyc = ", varSetTimCyc)
    print("\n")
    sys.stdout.flush()
    return


def run_EM63():
    global varDATE, varTIME, filepathEM63, varFormEM63path, session, valEM63
    session = session + 1
    if session > 3:
        session = 1

    valEM63refresh()

    varDATE = datetime.datetime.now().strftime("%Y%m%d")
    varTIME = datetime.datetime.now().strftime("%H:%M:%S")

    if varFormEM63path != '':
        filepathEM63 = varFormEM63path
        varFormEM63path = ''
    if filepathEM63 == '':
        print("EM63 path is not defined.")
        time.sleep(2)
        return
    else:
        # print("EM63 path is defined: " + filepathEM63)
        if filepathEM63.startswith('/') and not filepathEM63.endswith('/'):
            print("EM63 path needs / ")
            filepathEM63 = filepathEM63 + "/"
        if not os.path.exists(filepathEM63):
            print("EM63 path " + filepathEM63 + " does not exist.")
            time.sleep(2)
            return
        # else:
            # print("EM63 path exists.")

    # Open SESSnnnn.REQ file if it exists
    reqFile = filepathEM63 + "SESS" + str(session).zfill(4) + '.REQ'
    # print(reqFile)
    if os.path.exists(reqFile):
        print("---------------------------------------------")
        print("Request file found: "+reqFile+". Processing ...")
        f_in = open(reqFile, 'r')
        reqFileContent = f_in.read()
        f_in.close()

        # Extract Job file name from REQ file
        try:
            jobFile = re.search('"(.+?)"', reqFileContent).group(1)
            print("Job file name found: "+jobFile+".")
        except AttributeError:
            # ", " not found in the original string
            jobFile = ''
            print("No job file name found. Error ...")
        rmFile(reqFile)
    else:
        return

    # Look for job file named
    jobFile = filepathEM63 + jobFile
    if os.path.exists(jobFile):
        print("Job file found: "+jobFile+". Processing ...")
        f_in = open(jobFile, 'r')
        jobFileLines = f_in.readlines()
        f_in.close()
        # print(jobFileLines)
        # rmFile(jobFile)

        # Extract instructions from job file
        txtLOG = ''
        for line in jobFileLines:
            # GETID
            if 'GETID ' in line:
                # Extract target file name from line
                datFile = re.search('"(.+?)"', line).group(1)
                datFile = filepathEM63 + datFile
                f_datFile = open(datFile, 'w+')
                f_datFile.write(txtGETID)
                f_datFile.close()
                txtLOG = 'COMMAND 2 PROCESSED "GETID command" ' \
                    + str(varDATE) + ' ' + str(varTIME) + ';'
                # print(txtLOG)

            # GETINFO
            if 'GETINFO ' in line:
                # Extract target file name from line
                datFile = re.search('"(.+?)"', line).group(1)
                datFile = filepathEM63 + datFile
                # Check if local copy of GETINFO.DAT exists: GETINFO.conf
                if os.path.exists("GETINFO.conf"):
                    # use it
                    f_in = open('GETINFO.conf', 'r')
                    confFileBody = f_in.read()
                    f_datFile = open(datFile, 'w+')
                    f_datFile.write(confFileBody)
                    f_datFile.close()
                    f_in.close()
                else:
                    f_datFile = open(datFile, 'w+')
                    f_datFile.write(txtGETINFO)
                    f_datFile.close()
                txtLOG = 'COMMAND 2 PROCESSED "GETINFO command" ' \
                    + str(varDATE) + ' ' + str(varTIME) + ';'
                # print(txtLOG)

            # REPORT
            if 'REPORT ' in line:
                # Extract target file name from line
                datFile = re.search('"(.+?)"', line).group(1)
                datFile = filepathEM63 + datFile
                # Write only parameters requested
                txtREPORT = ''
                valREPORT = ''
                for line2 in jobFileLines:
                    for index in range(len(valEM63)):
                        if valEM63[index][0] in line2:
                            # print(valEM63[index][0], line2)
                            newline2 = line2
                            newline2 = newline2.replace(",", "")
                            newline2 = newline2.replace(" ", "")
                            newline2 = newline2.replace("\n", "")
                            # print(valEM63[index][0], newline2)
                            if newline2 in valEM63[index][0]:
                                # Use EM63 parameter names
                                txtREPORT = txtREPORT + valEM63[index][0]
                                if index < len(valEM63):
                                    txtREPORT = txtREPORT + ','
                                # Use EM63 parameter values
                                valREPORT = valREPORT + str(valEM63[index][1])
                                if index < len(valEM63):
                                    valREPORT = valREPORT + ','
                txtREPORT = txtREPORT + '\n' + valREPORT + ';'
                txtREPORT = txtREPORT.replace(",\n", "\n")
                txtREPORT = txtREPORT.replace(",;", "")
                f_datFile = open(datFile, 'w+')
                f_datFile.write(txtREPORT)
                f_datFile.close()
                txtLOG = 'COMMAND 2 PROCESSED "REPORT command" ' \
                    + str(varDATE) + ' ' + str(varTIME) + ';'
                # print(txtLOG)

            # Create LOG file
            if 'RESPONSE ' in line:
                # Write log file
                # Extract target file name from line for log file
                logFile = re.search('"(.+?)"', line).group(1)
                logFile = filepathEM63 + logFile
                if logFile != '':
                    txtLOG0 = 'COMMAND 1 PROCESSED "JOB command" ' \
                        + str(varDATE) + ' ' + str(varTIME) + ';\n'
                    if os.path.exists(logFile):
                        rmFile(logFile)
                    # if txtLOG != '' and txtLOG0 != '':
                    f_logFile = open(logFile, 'w+')
                    txtLOG0 = txtLOG0 + txtLOG
                    f_logFile.write(txtLOG0)
                    f_logFile.close()
                    # print("Log file was written: ", logFile)

        # Create RSP file
        rspFile = filepathEM63 + "SESS" + str(session).zfill(4) + '.RSP'
        if os.path.exists(rspFile):
            rmFile(rspFile)
        f_rspFile = open(rspFile, 'w+')
        txtRSP = '00000001 PROCESSED "EXECUTE ' + jobFile + '";'
        f_rspFile.write(txtRSP)
        f_rspFile.close()
        print("Response file was written: ", rspFile)
        sys.stdout.flush()


class vIMM(StateMachine):
    # Simplified IMM states
    s_idle = State('Idle', initial=True)
    s_setup = State('Set up')
    s_production = State('Production')
    s_error = State('Machine Error')
    s_pause = State('Pause')
    s_finished = State('Job Completed')

    # Simplified IMM transitions/events
    # e_EVENT = s_fromSTATE.to(s_toSTATE)
    e_setting = s_idle.to(s_setup)
    e_start = s_setup.to(s_production)
    e_proceed = s_pause.to(s_production)
    e_confirm = s_error.to(s_production)
    e_error = s_production.to(s_error)
    e_pause = s_production.to(s_pause)
    e_finished = s_production.to(s_finished)
    e_reset = s_finished.to(s_idle)

    def on_enter_s_idle(self):
        global varActStsMach, varActCntPrt, varActCntCyc, varSetCntMld
        global varSetCntPrt, varSetTimCyc, varActTimCyc
        varActStsMach = '1I000'
        varSetCntMld = 0
        varSetCntPrt = 0
        varSetTimCyc = 0
        varActCntCyc = 0
        varActCntPrt = 0
        varActTimCyc = 0
        return

    def on_enter_s_setup(self):
        # Initial parameters set by API
        global varActStsMach, varFormState
        varActStsMach = '1U001'
        return

    def on_enter_s_production(self):
        global varActStsMach
        varActStsMach = '0A000'
        return

    def on_enter_s_error(self):
        global varActStsMach
        varActStsMach = '0C001'
        print("State: error ...")
        return

    def on_enter_s_pause(self):
        global varActStsMach
        varActStsMach = '0H000'
        print("State: pause ...")
        return

    def on_s_error(self):
        while 0 < 1:
            if varFormState == 'formStateproduction':
                self.e_confirm()
            else:
                time.sleep(1)

    def on_s_pause(self):
        while 0 < 1:
            if varFormState == 'formStateproduction':
                self.e_proceed()
            else:
                time.sleep(1)

    def on_enter_s_finished(self):
        global varActStsMach
        varActStsMach = '1C000'
        print("Job finished... Restart?")
        finished()
        return


def waitForProduction():
    global varFormState
    while 0 < 1:
        if varFormState == 'formStateproduction':
            return
        else:
            time.sleep(1)


def autostart_production(args):
    """
    Autostart the production based on the
    given command line arguments.
    """
    global varATActSimPara1, varATActSimPara2period, varATActSimPara2amplitude
    global varATActSimPara2phase, varATActSimPara2phaseStr
    global varATActSimPara2offset
    global varSetCntMld, varSetCntPrt, varSetTimCyc, varFormState
    print("Autostarting the production ...")
    # Set variables based on args: simulation parameter
    varATActSimPara1 = int(args.varATActSimPara1)
    varATActSimPara2period = float(args.varATActSimPara2period)
    varATActSimPara2amplitude = float(args.varATActSimPara2amplitude)
    varATActSimPara2phase = float(args.varATActSimPara2phase)
    varATActSimPara2phaseStr = str(args.varATActSimPara2phase)
    varATActSimPara2offset = float(args.varATActSimPara2offset)
    # Set variables based on args: production params
    varSetCntMld = int(args.varSetTimCyc)
    varSetCntPrt = int(args.varSetCntPrt)
    varSetTimCyc = float(args.varSetTimCyc)
    # Set variables based on args: finally go to productions state
    varFormState = "formStateproduction"


#
# Command line argument parser
#
def parse_args(manual_args=None):
    """
    CLI interface definition.
    """
    parser = argparse.ArgumentParser(
        description="IMMS ('Injection Molding Machine Simulator' Application)")

    parser.add_argument(
        "-a",
        "--autostart",
        help="Automatically start production.",
        required=False,
        default=False,
        dest="autostart",
        action="store_true")

    parser.add_argument(
        "--varATActSimPara1",
        required=False,
        default=5)

    parser.add_argument(
        "--varATActSimPara2period",
        required=False,
        default=10.0)

    parser.add_argument(
        "--varATActSimPara2amplitude",
        required=False,
        default=1.0)

    parser.add_argument(
        "--varATActSimPara2phase",
        required=False,
        default=0)

    parser.add_argument(
        "--varATActSimPara2offset",
        required=False,
        default=1.0)

    parser.add_argument(
        "--varPlotATActSimPara",
        required=False,
        default=False)

    parser.add_argument(
        "--varSetCntMld",
        required=False,
        default=10)

    parser.add_argument(
        "--varSetCntPrt",
        required=False,
        default=10000)

    parser.add_argument(
        "--varSetTimCyc",
        required=False,
        default=1.0)

    if manual_args is not None:
        return parser.parse_args(manual_args)
    return parser.parse_args()


def main():
    # Parse CLI arguments
    args = parse_args()
    print("Starting IMMS with arguments: {}".format(args))
    # Instantiate
    # IMM1 = vIMM()
    start_webapp()
    start_EM63()

    if args.autostart:
        autostart_production(args)

    while 0 < 1:
        IMM1.e_setting()
        waitForProduction()
        IMM1.e_start()
        x = 1
        while x == 1:
            x = 0
            production()
            if IMM1.is_s_pause:
                waitForProduction()
                IMM1.e_proceed()
                x = 1
            if IMM1.is_s_error:
                waitForProduction()
                IMM1.e_confirm()
                x = 1
        IMM1.e_finished()
        IMM1.e_reset()


def plotAllLocal(sinPlotX, sinPlotY, sinPlotY2, sinPlotY3):
    plotActSimPara2(sinPlotX, sinPlotY, sinPlotY2)
    plotActCnt(sinPlotY3)


def plotActSimPara2(sinPlotX, sinPlotY, sinPlotY2):
    x = np.array(sinPlotX)
    y = np.array(sinPlotY)
    y2 = np.array(sinPlotY2)

    trace1 = go.Scatter(
                x=x,
                y=y2,
                mode='lines+markers',
                name='@ActSimPara1'
                )
    trace2 = go.Scatter(
                x=x,
                y=y,
                mode='lines+markers',
                name='@ActSimPara2'
                )

    plotly.offline.plot({
        "data": [trace1, trace2],
        "layout": go.Layout(title="Parameters")
    }, filename='templates/plotActSimPara.html', auto_open=False)


def plotActCnt(sinPlotY3):
    x = np.array(sinPlotY3)
    # data = [go.Histogram(x=x, histnorm='probability')]
    # plotly.offline.plot(data,  filename='ActCntCyc2.html', auto_open=False)
    plotly.offline.plot({
        "data": [go.Histogram(x=x, histnorm='probability')],
        "layout": go.Layout(title="ActCntCyc")
    }, filename='templates/plotActCntCyc.html', auto_open=False)


if __name__ == "__main__":
    # Instantiate
    IMM1 = vIMM()
    main()
