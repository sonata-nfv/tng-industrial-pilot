# FSMs for industrial pilot

This folder contains the FSMs for this pilot.

More information about FSM/SSM implementations for this pilot can be found [here](https://github.com/sonata-nfv/tng-industrial-pilot/wiki/FSM-SSM-Development).

## Testing

The SSM can be tested with `tng-sdk-sm`:

```bash
# run in this directory
tng-sm execute -e configure -p configure_event.yml -s mdc-fsm
# prints the log outputs of the SSM
```

## Building and Publishing

The SSM is automatically built and published on DockerHub, whenever a PR is merged into `master`.

