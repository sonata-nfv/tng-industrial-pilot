# SSMs for industrial pilot

The SSM receives reconfiguration requests from either the policy manager (if the IDS detected an intrusion) or the control server (if triggered via the FMP). It forwards the reconfiguration request to the MDC FSM, which handles the actual reconfiguration.

More information about FSM/SSM implementations for this pilot can be found [here](https://github.com/sonata-nfv/tng-industrial-pilot/wiki/FSM-SSM-Development).

## Testing

The SSM can be tested with `tng-sdk-sm`:

```bash
# run in this directory
tng-sm execute -e configure -p configure_event.yml -s ns2-ssm
# prints the log outputs of the SSM
```

## Building and Publishing

The SSM is automatically built and published on DockerHub, whenever a PR is merged into `master`.