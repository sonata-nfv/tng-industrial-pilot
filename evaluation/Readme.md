# Evaluation

This directory contains scripts for evaluations and plotting

## Setup

1. Install vim-emu and the smart manufacturing VNFs
1. Install `pandas`, [`tng-sdk-package`](https://github.com/sonata-nfv/tng-sdk-package) inside a python3 virtualenv, which is later used to run the evaluation script
1. Install tng-sdk-benchmark
    * Clone: `git clone git@github.com:sonata-nfv/tng-sdk-benchmark.git`
    * Install with Python 2 (globally): `sudo python setup.py install`
1. Start server for starting/stopping emulation (incl. in tng-sdk-benchmark): `sudo tng-bench-emusrv`

## Usage

Activate the virtualenv, in which `pandas` and `tng-sdk-package` are installed.

```bash
python3 measure_runtimes.py (-n <runs>)
```

Optionally specify with `-n` how many runs per NS should be executed and measured (default is one).


## Other

### Starting/stopping emulator via REST API (incl. in tng-sdk-benchmark)

1. Start emulator: `curl -X post localhost:4999/api/v1/emulation`
1. Stop emulator: `curl -X delete localhost:4999/api/v1/emulation`

`curl -X get localhost:4999/api/v1/emulation` returns if the emulator is running (true/false)

To kill the emulator (if `exit` doesn't work): `sudo pkill python`
