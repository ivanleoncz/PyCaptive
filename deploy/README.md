The steps defined below are designed for Debian-like distros (Red Hat-like distros
use different commands and files) and there might be differences from one distro
to another (also differences among distro versions), regarding packages, directories
and files. Due to this scenario, a step-by-step setup was defined below instead
of a automated process, in order to avoid installation problems.


### Cloning PyCaptive
```
$ cd /opt
$ git clone https://github.com/ivanlmj/PyCaptive.git
```

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

### Installing Python Packages
```
$ pip3 install -r /opt/PyCaptive/requirements.txt
```

### PyCaptive Group and User
```
$ groupadd pycaptive -g 14090
$ useradd pycaptive -s /usr/sbin/nologin -c "PyCaptive Account" -u 14090 -g 14090
```

### Sudoers
```
$ cp /opt/PyCaptive/deploy/sudoers.d/pycaptive /etc/sudoers.d
$ chmod 444 /etc/sudoers.d/pycaptive
```

### Log Directory
```
$ mkdir /var/log/pycaptive
$ chown pycaptive:pycaptive /var/log/pycaptive
$ chmod 770 /var/log/pycaptive
$ echo "PyCaptive Deploy at: `/bin/date`" > /var/log/pycaptive/pycaptive.log
$ chown pycaptive:pycaptive /var/log/pycaptive/pycaptive.log
$ chmod 660 /var/log/pycaptive/pycaptive.log
```

### Logrotate
```
$ cp /opt/PyCaptive/deploy/logrotate/pycaptive /etc/logrotate.d/
$ chmod 444 /etc/logrotate.d/pycaptive
```

### Nginx
```
$ cp /opt/PyCaptive/deploy/nginx/pycaptive /etc/nginx/sites-available/
$ ln -s /etc/nginx/sites-available/pycaptive /etc/nginx/sites-enabled/pycaptive
$ chmod 444 /etc/nginx/sites-enabled/pycaptive
$ service nginx restart
```

### Supervisor
```
$ cp /opt/PyCaptive/deploy/supervisor/pycaptive /etc/supervisor/conf.d/pycaptive
$ supervisorctl restart
```

### SYSCTL (uncomment/add: net.ipv4.ip_forward=1)
```
$ vim /etc/sysctl.conf
$ sysctl -p
```

### IPTABLES
```
$ mkdir /etc/iptables
$ sudo iptables-save > /etc/iptables/before_pycaptive.v4.bkp
$ bash /opt/Pycaptive/deploy/iptables/firewall_setup.sh
$ sudo iptables-save > /etc/iptables/rules.v4
```
