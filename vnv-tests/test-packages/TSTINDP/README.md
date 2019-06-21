<p align="center"><img src="https://github.com/sonata-nfv/tng-api-gtw/wiki/images/sonata-5gtango-logo-500px.png" /></p>

# Test Package


## Manual test steps on pre-int-vnv-bcn environment

ASSUMPTION: assume the NS (`eu.sonata-nfv.service-descriptor:sonata-vtc-only:0.1`) under test is already in SP catalog.

1. zip the folder as `5gtango-test-package-example.zip`
2. rename `5gtango-test-package-example.zip` as `5gtango-test-package-example.tgo`
3. upload the package via VnV Gatekeeper, it will return `package_process_uuid` for query later:
    ```
    curl -v -X POST -F "package=@/d/workspace/src/mrduguo/tng-schema/package-specification/examples/5gtango-test-package-example/5gtango-test-package-example.tgo" \
      http://pre-int-vnv-bcn.5gtango.eu:32002/api/v3/packages
    ```
4. find the package id via stats endpoint:
    ```
    curl -v http://pre-int-vnv-bcn.5gtango.eu:32002/api/v3/packages/status/dc26d20c-1c00-4bfd-88fc-b9c2606dab27
    ```
5. trigger the test with the package id:
    ```
    curl -v -X POST "http://pre-int-vnv-bcn.5gtango.eu:6100/tng-vnv-lcm/api/v1/packages/on-change"  \
     -H "Content-Type: application/json" -d '{ "event_name": "UPDATED", "package_id": "a1030acb-d392-4192-91d0-0c7724d8264e"}'
    ```
6. while test is running, user can view the progress from [graylog](http://logs.sonata-nfv.eu/search?rangetype=relative&fields=message&width=1536&highlightMessage=&relative=7200&q=pre-int-vnv-bcn+AND+container_name%3Atng%5C-vnv%5C-tee)
7. query the test suite result via Test Result Repository:
    ```
    curl -v http://pre-int-vnv-bcn.5gtango.eu:4012/trr/test-plans
    ```
8. a success test would have status:  `SUCCESS`:
    ```
    [
      {
        "created_at": "2018-05-30T08:44:57.575+00:00",
        "network_service_instances": [
          {
            "service_instance_uuid": "ed036e6a-faeb-4ae0-838f-b8618901ae17",
            "service_uuid": "58b47eb9-a603-4232-a090-cb3a01456344",
            "status": "READY",
            "runtime": null
          }
        ],
        "package_id": "45e20b48-84ff-4b29-8de1-e2e78ffcd6af",
        "status": "SUCCESS",
        "test_suite_results": [
          {
            "package_id": "45e20b48-84ff-4b29-8de1-e2e78ffcd6af",
            "uuid": "5b0e6489b371bf0001000003",
            "test_plan_id": "5b0e6434b371bf0001000001",
            "network_service_instance_id": "ed036e6a-faeb-4ae0-838f-b8618901ae17",
            "test_suite_id": "ca9a833a-59e1-4fbb-965d-4ae120291488",
            "status": "SUCCESS"
          }
        ],
        "updated_at": "2018-05-30T08:44:57.575+00:00",
        "uuid": "5b0e6489b371bf0001000004"
      }
    ]
    ```
9. query the test suite result via Test Result Repository:
    ```
    curl -v http://pre-int-vnv-bcn.5gtango.eu:4012/trr/test-suite-results
    ```
10. a success test would have status:  `SUCCESS`:
    ```
    [
      {
        "created_at": "2018-05-29T15:21:45.957+00:00",
        "details": {
          "none": 1,
          "pass": 0,
          "inconc": 0,
          "fail": 0,
          "error": 0
        },
        "network_service_instance_id": "ed036e6a-faeb-4ae0-838f-b8618901ae17",
        "package_id": "25adbc52-3488-443e-bdb2-2c641b113dac",
        "status": "SUCCESS",
        "sterr": "",
        "stout": "ttcn3_start: Starting the test suite\nspawn /home/node/titan/bin/mctr_cli ...................ted from MC. Terminating HC.\nMC@c838258ada7f: Shutdown complete.\n",
        "test_plan_id": "5b0d6fb53ac8300001000001",
        "test_suite_id": "abb83bbc-69de-41f3-9606-fdd1f88f6256",
        "tester_result_text": "15:20:54.044121 - TTCN-3 Main Test Component started on c838258ada7f. Version: CRL 113 2......................ase.\n15:21:44.825975 HTTP_Test.ttcn:251 Local verdict of MTC: none\n15:21:44.826047 HTTP_Test.ttcn:251 No PTCs were created.\n15:21:44.826118 HTTP_Test.ttcn:251 Test case tc_http_getResult finished. Verdict: none\n15:21:44.826470 - Verdict statistics: 1 none (100.00 %), 0 pass (0.00 %), 0 inconc (0.00 %), 0 fail (0.00 %), 0 error (0.00 %).\n15:21:44.826588 - Test execution summary: 1 test case was executed. Overall verdict: none\n15:21:44.826669 - Exit was requested from MC. Terminating MTC.\n",
        "updated_at": "2018-05-29T15:21:45.957+00:00",
        "uuid": "5b0d70093ac8300001000003"
      }
    ]
    ```
    
