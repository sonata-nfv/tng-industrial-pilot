#!/bin/bash
echo "On-boarding NS1 and NS2 ..."
tng-cli -u http://127.0.0.1 package -u eu.5gtango.tng-smpilot-ns1-emulator.0.1.tgo
tng-cli -u http://127.0.0.1 package -u eu.5gtango.tng-smpilot-ns2-emulator.0.1.tgo
echo "DONE"
echo ""

echo "Instantiating NS1.0 and NS1.1 ..."
tng-cli -u http://127.0.0.1 service -i tng-smpilot-ns1-emulator
tng-cli -u http://127.0.0.1 service -i tng-smpilot-ns1-emulator
echo "DONE"
echo ""

echo "Instantiating NS2.0 and NS2.1 and NS2.2 ..."
tng-cli -u http://127.0.0.1 service -i tng-smpilot-ns2-emulator
tng-cli -u http://127.0.0.1 service -i tng-smpilot-ns2-emulator
tng-cli -u http://127.0.0.1 service -i tng-smpilot-ns2-emulator
echo "DONE"
echo ""
