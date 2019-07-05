#!/bin/bash
sudo date
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

echo "Interconnecting services ..."
./netsoft_connect_stage1.sh
echo "DONE"
