# Notice
> Due to the difference presented between distros for these packages and their
> directories/files, it is recommended to execute each action below, step by step,
> so you can adjust the paths for each binary, depending on your distro.

### MongoDB Repo (https://docs.mongodb.com/v3.4/tutorial/install-mongodb-on-debian/)
```
$ apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
$ echo "deb http://repo.mongodb.org/apt/debian jessie/mongodb-org/3.4 main" > /etc/apt/sources.list.d/mongodb-org-3.4.list
```

### Installing Packages
```
$ apt-get update
$ apt-get install python3-pip iptables conntrack nginx supervisor mongodb-org
```

### PyCaptive Group and User
```
$ groupadd pycaptive -g 14090
$ useradd pycaptive -s /usr/sbin/nologin -c "PyCaptive Account" -u 14090 -g 14090
```

### Log Directory
```
$ mkdir /var/log/pycaptive
$ chmod 770 /var/log/pycaptive
$ chown pycaptive:pycaptive /var/log/pycaptive
$ echo "PyCaptive Deploy at: `/bin/date`" > /var/log/pycaptive/pycaptive.log
$ chown pycaptive:pycaptive /var/log/pycaptive/pycaptive.log
$ chmod 660 /var/log/pycaptive/pycaptive.log
```

### IPTABLES
```
$ mkdir /etc/iptables
$ bash /opt/Pycaptive/deploy/iptables/firewall_setup.sh
$ cp /opt/PyCaptive/deploy/rules.v4 /etc/iptables/
```

### Sudoers
```
$ cp /opt/PyCaptive/deploy/sudoers.d/pycaptive /etc/sudoers.d
$ chmod 444 /etc/sudoers.d/pycaptive
```

### Nginx
```
$ cp /opt/PyCaptive/deploy/nginx/pycaptive /etc/nginx/sites-available/
$ ln -s /etc/nginx/sites-available/pycaptive /etc/nginx/sites-enabled/pycaptive
$ chmod 444 /etc/nginx/sites-enabled/pycaptive
```

### Python Packages
```
$ pip3 install -r /opt/PyCaptive/requirements.txt
```

### Logrotate
```
$ cp /opt/PyCaptive/deploy/logrotate/pycaptive /etc/logrotate.d/
$ chmod 444 /etc/logrotate.d/pycaptive
```

### Supervisor
```
$ cp /opt/PyCaptive/deploy/supervisor/pycaptive /etc/supervisor/conf.d/pycaptive
$ supervisorctl restart
```
