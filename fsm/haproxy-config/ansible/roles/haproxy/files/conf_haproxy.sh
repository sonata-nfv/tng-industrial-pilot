sudo   haproxy -f /etc/haproxy.cfg \
           -D -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)
