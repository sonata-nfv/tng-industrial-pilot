*** Settings ***
Documentation     Test suite template for deploy and undeploy of a NS composed of one cnf with elasticity policy enforcement
Library           tnglib
Library           Collections
Library           DateTime

*** Variables ***
${SP_HOST}                http://pre-int-sp-ath.5gtango.eu   #  the name of SP we want to use
${READY}       READY
${FILE_SOURCE_DIR}     ../../../sdk-projects   # to be modified and added accordingly if package is not on the same folder as test 
${NS_PACKAGE_NAME}           5gtango.tng-smp-ns2-k8s-mdc-eids.0.8.tgo    # The package to be uploaded and tested
${NS_PACKAGE_SHORT_NAME}  tng-smpilot-ns2-eids
${POLICIES_SOURCE_DIR}    ./   # to be modified and added accordingly if policy is not on the same folder as test ( ./policies from local pc)
${POLICY_NAME}           industrial-pilot-Security-Policy.json    # The policy to be uploaded and tested
${READY}       READY
${PASSED}      PASSED
${SERVICE_UUID}    89b9a0a7-db4e-45e8-9e31-1700bb869027

*** Test Cases ***
Setting the SP Path
    #From date to obtain GrayLogs
    ${from_date} =   Get Current Date
    Set Global Variable  ${from_date}
    Set SP Path     ${SP_HOST}
    ${result} =     Sp Health Check
    Should Be True   ${result} 
Create Runtime Policy
    ${result} =     Create Policy      ${POLICIES_SOURCE_DIR}/${POLICY_NAME}
    Should Be True     ${result[0]}
    Set Suite Variable     ${POLICY_UUID}  ${result[1]}
Define Runtime Policy as Default
    ${result} =     Define Policy As Default      ${POLICY_UUID}   service_uuid=${SERVICE_UUID}
    Should Be True     ${result[0]}
Deploying Service
    ${init} =   Service Instantiate     ${SERVICE_UUID}
    Log     ${init}
    Set Suite Variable     ${REQUEST}  ${init[1]}
    Log     ${REQUEST} 
Wait For Ready
    Wait until Keyword Succeeds     10 min   5 sec   Check Status
    Set SIU
Get Service Instance
    ${init} =   Get Request   ${REQUEST}
    Log     ${init}
    Set Suite Variable     ${SERVICE_INSTANCE_UUID}  ${init[1]['instance_uuid']}
    Log     ${SERVICE_INSTANCE_UUID} 
Wait for some minutes
    Sleep   10m
Deactivate Runtime Policy
    ${result} =     Deactivate Policy      ${SERVICE_INSTANCE_UUID}
    Should Be True     ${result[0]}
Terminate Service
    ${ter} =    Service Terminate   ${SERVICE_INSTANCE_UUID}
    Log     ${ter}
    Set Suite Variable     ${TERM_REQ}  ${ter[1]}
Wait For Terminate Ready    
    Wait until Keyword Succeeds     3 min   5 sec   Check Terminate 
Delete Runtime Policy
    ${result} =     Delete Policy      ${POLICY_UUID}
    Should Be True     ${result[0]}
Obtain GrayLogs
    ${to_date} =  Get Current Date
    Set Suite Variable  ${param_file}   True
    Get Logs  ${from_date}  ${to_date}  ${SP_HOST}  ${param_file}
    

*** Keywords ***
Check Status
    ${status} =     Get Request     ${REQUEST}
    Should Be Equal    ${READY}  ${status[1]['status']}
Set SIU
    ${status} =     Get Request     ${REQUEST}
    Set Suite Variable     ${TERMINATE}    ${status[1]['instance_uuid']}
Check Terminate
    ${status} =     Get Request     ${TERM_REQ}
    Should Be Equal    ${READY}  ${status[1]['status']}
