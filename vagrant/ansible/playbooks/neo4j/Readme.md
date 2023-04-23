#### Vagrant and ansible to install/configure neo4j ####

To setup neo4j,

install vagrant, python (3.0+) and ansible (2.0+)

build the vm first. Run vagrant up command from vagrantfile folder.

```vagrant up```

Then run the ping script to see if you can ping the new vm through ansible.

```ansible cluster -m ping -i hosts```

you should see 

```
    127.0.0.1 | SUCCESS => {
            "ansible_facts": {
            "discovered_interpreter_python": "/usr/bin/python"
            },
            "changed": false,
            "ping": "pong"
        }
```

To install neo4j, 

```ansible-playbook ./neo4j-install.yml  -i hosts```

    Goto http://localhost:7474/browser/ to login and setup initial password.

To configure 

```ansible-playbook ./neo4j-config.yml  -i hosts```

To start
    
```ansible-playbook ./neo4j-start.yml  -i hosts```

To stop

```ansible-playbook ./neo4j-stop.yml  -i hosts```

To get logs

```ansible-playbook ./neo4j-get-logs.yml  -i hosts```

To uninstall

```ansible-playbook ./neo4j-uninstall.yml  -i hosts```

To access browser console

    http://localhost:7474/browser/


#### Todo ####

apoc jar - right version

set user creds 

extract variables

remove system db. set only one db default.

try query logs

use python 3

set ulimit - copy neo4j.j2 to /etc/default/neo4j