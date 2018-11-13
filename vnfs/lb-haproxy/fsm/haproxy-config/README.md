# Haproxy Configuration FSM
FSM to configure the haproxy function that connects to Service Specific Registry (SMR) and performs a self-registration using the SSM/FSM template. Once the registration is done, it subscribes to configuration topic (son.configuration) to receive the VNFR which is sent by the SLM. Finally, it retrieves the VNF's IP address from the VNFR so that it can connect to the VNF and configure/reconfigure it.

## Requires
* Docker
* Python3.5
* RabbitMQ

## Implementation
* Implemented in Python 3.5
* Dependencies: amqp-storm
* The main implementation can be found in: `tng_fsm_css/tng_fsm_css.py`

## How to run it
* To run the FSM locally, you need:
 * a running RabbitMQ broker (see general README.md of [son-mano framework repository](https://github.com/sonata-nfv/son-mano-framework) for info on how to do this)
 * a running Service Specific Registry (SMR) connected to the broker (see general README.md of [SMR repository](https://github.com/sonata-nfv/son-mano-framework) for info on how to do this)

* Run the configuration FSM (in a Docker container):
 * (do in `tng-industrial-pilot`)
 * `docker build -t son-fsm-service-haproxyconfig1 -f fsm/haproxy-config/Dockerfile .`
 * `docker run -it --rm --link broker:broker --net sonata --name son-fsm-service-haproxyconfig1  son-fsm-service-haproxyconfig1`

* Or: Run the configuration FSM (directly in your terminal not in a Docker container):
 * Clone `son-sm` in tng-industrial-pilot
    * (In `son-sm/son-mano-framework/son-mano-base/`)
        * `python setup.py install`
    * (In `son-sm/son-sm-template/`)
        * `python setup.py install`
 * (In `fsm/haproxy-config/`)
    * `python setup.py`

## How to test it
* Do the following; each in a separate terminal.
    1. Run the SMR container
    2. Run the configuration container
    3. In `tng-industrial-pilot/fsm/haproxy-config/test` run `python3 testConf.py`
