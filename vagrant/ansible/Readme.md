#### Vagrant and ansible
Prerequisites -  vagrant, python (3.0+) and ansible (2.0+)


##### vagrant vm commands
to bring up the vm's - 
```vagrant up```

to stop vagrant vm's - 
```vagrant halt```

to shell into vm - 
```vagrant ssh```

to destroy vm - 
```vagrant destroy -f```

state of the machines Vagrant is managing - ```vagrant status [name|id]```

To fetch a file from vagrant vm to host (as root)

```scp -P 2222 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ./.vagrant/machines/master/virtualbox/private_key  vagrant@127.0.0.1:~/* .
```

##### vagrant vm image commands

to list installed boxes - 
```vagrant box list```

to remove box - 
```vagrant box remove NAME```




