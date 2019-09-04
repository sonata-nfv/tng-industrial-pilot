Dumb SSM Example
An empty SSM example that connects to Service Specific Manager (SMR) and performs a self-registration using the SSM/FSM template.

Requires
Docker
Python3.4
RabbitMQ
Implementation
Implemented in Python 3.4
Dependencies: amqp-storm
The main implementation can be found in: son-ssm-examples/dumb/dumb.py
How to run it
To run the dumb SSM locally, you need:

a running RabbitMQ broker (see general README.md of son-mano framework repository for info on how to do this)

a running Service Specific Registry (SMR) connected to the broker (see general README.md of SMR repository for info on how to do this)

Run the dumb SSM (in a Docker container):

(do in son-sm/)

docker build -t sonssmservice1dumb1 -f son-ssm-examples/dumb/Dockerfile .

docker run -it --rm --link broker:broker --name sonssmservice1dumb1 sonssmservice1dumb1

Or: Run the dumb SSM (directly in your terminal not in a Docker container):

(In son-sm/son-sm-template/)

python3.4 setup.py install
(In son-sm/son-ssm-examples/dumb/)

python3.4 setup.py develop
(In son-sm/)

python3.4 son-ssm-examples/dumb/dumb/dumb.py
How to test it
Do the following; each in a separate terminal.

Run the SMR container
Run the dumb container
The expected results are as follows:

In the SMR terminal:

DEBUG:son-mano-specific-manager-registry:registration request received for: sonssmservice1dumb1
INFO:son-mano-specific-manager-registry:sonssmservice1dumb1 status: UP and Running
In dumb terminal:

INFO:son-sm-base:Starting sonssmservice1dumb1 ...
INFO:son-sm-base:sonssmservice1dumb1 registered with uuid:2470f131-5f72-45b3-af81-6f2d6acfca9f
DEBUG:ssm-dumb-1:Received registration ok event.
WARNING:amqpstorm.channel:Received Basic.Cancel on consumer_tag: q.specific.manager.registry.ssm.registration.e18f8896-61c
