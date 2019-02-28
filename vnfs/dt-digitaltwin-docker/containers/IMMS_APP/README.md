# Default configuration of IMMS_APP

## General configuration
Local: configure IMMS via Website: http://127.0.0.1:5000
Local: default EM63 shared session folder: /home/marcel/em63/
Container: see Dockerfile for environment variables

# Application of IMMS_APP

## Get help
```sh
$~ python3 IMMS_APP.py --help
```

## Autostart
Start the application in autostart with default values for process parameters.
```sh
$~ python3 IMMS_APP.py --autostart
```

## Manual start
Start the application. Start the process.

### Manual start of IMMS_APP
```sh
$~ python3 IMMS_APP.py
```

### Manual start of the simulation
Select Setup
-> Parameter -> and define 2 configurable parameters
-> Job -> and define your job
-> Machine State -> and select Production
Request data using session and job files in EM63 shared session folder
When job is finished switch from machine state job completed back to idle
Select Setup -> Machine State -> Select Idle

# Modules needed
```sh
$~ pip3 install python-statemachine --user
$~ pip3 install Flask --user
$~ pip3 install numpy --user
$~ pip3 install plotly --user
```
# TODO

## EM63 communication
State: EM63 file exchange does not work fine.
Sometimes the process is running and IMMS_APP do not respond to REQ files. 
MDC is not able to work. After restart of IMMS_APP, it works fine again until next crash.
Issue: Maybe, the thread2 for EM63 communication was crashed. 

## EM63 log file
State: File with correct name is created.
Issue: COMMAND 1 is written to LOG file, COMMAND 2 can not be written.Log file is written before COMMAND2 is read.
Reason: RESPONSE is named in JOB file before REPORT, GETID, GETINFO.

## EM63 shared session folder
Make EM63 web configuration persistent.
Currently it is only temporary stored via web gui.

## Visualization in web GUI

### Parameter live visulization in monitoring tab
State: Live plot is not possible. html web site is static.
Issue: Refresh is used but html web sites already visited are not refreshed.
Reason: Maybe, website is already cached and cache refresh is not defined.

### Visualization of machine state
State: Current machine state is not visualized.
ToDo: Transfer machine state data from python script to web server.

## Misc
Reduce global variables and use call by reference instead of global variables.
