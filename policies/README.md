# Policy for the IDS use case

When the IDS of NS2 detects an intrusion, it sets the metric `ip0` from 0 to a positive number. The policy creates a Prometheus monitoring alert that watches this metric and is active if `ip0 > 0`. This again leads to the policy manager triggering a reconfiguration event via the pub/sub system to the MANO and from there to the SSM.

The policy needs to be created via REST (or future Portal) and selected as default policy. Then it's activated automatically, when the service is instantiated.

See details here: https://github.com/sonata-nfv/tng-industrial-pilot/wiki/IDS-reconfiguration