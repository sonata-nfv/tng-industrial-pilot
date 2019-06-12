#!/bin/bash
echo "Instantiating NS1.2 ..."
tng-cli -u http://127.0.0.1 service -i tng-smpilot-ns1-emulator
echo "DONE"
echo ""

echo "Instantiating NS2.3 and NS2.4 ..."
tng-cli -u http://127.0.0.1 service -i tng-smpilot-ns2-emulator
tng-cli -u http://127.0.0.1 service -i tng-smpilot-ns2-emulator
echo "DONE"
echo ""
