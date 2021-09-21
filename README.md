# Ceph-based_file_manager

Steps to run the application:

1) enter into virtual machines with ssh root@172.16.3.233, ssh root@172.16.3.234, ssh root@172.16.3.235.

2) enter into machine's container and run server's instances:

1) on machine 172.16.3.233 -> lxc exec juju-cd6e1f-1-lxd-0 /bin/bash -> python3 server.py

2) on machine 172.16.3.234 -> lxc exec juju-cd6e1f-2-lxd-1 /bin/bash -> python3 server.py

3) on machine 172.16.3.235 -> lxc exec juju-cd6e1f-3-lxd-1 /bin/bash -> python3 server.py

3) on machine 172.16.3.234 run the client -> python3 client.py
4) do things with the client
