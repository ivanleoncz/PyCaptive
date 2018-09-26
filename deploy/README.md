### Create PyCaptive Group and User
/usr/sbin/groupadd pycaptive -g 14090
/usr/sbin/useradd pycaptive -s /usr/sbin/nologin -c "PyCaptive Account" -u 14090 -g 14090

### Setting up Log Directory

/bin/mkdir /var/log/pycaptive
/bin/chmod 770 /var/log/pycaptive
/bin/chown pycaptive:pycaptive /var/log/pycaptive
/bin/echo "PyCaptive Deploy at: `/bin/date`" > /var/log/pycaptive/pycaptive.log
/bin/chown pycaptive:pycaptive /var/log/pycaptive/pycaptive.log
/bin/chmod 660 /var/log/pycaptive/pycaptive.log

### IPTABLES
/bin/mkdir /etc/iptables
/bin/bash /opt/Pycaptive/deploy/iptables/firewall_setup.sh
/bin/cp /opt/PyCaptive/deploy/rules.v4 /etc/iptables/

### Logrotate
/bin/cp /opt/PyCaptive/deploy/logrotate/pycaptive /etc/logrotate.d/
/bin/chmod 444 /etc/logrotate.d/pycaptive

### Sudoers
/bin/cp /opt/PyCaptive/deploy/sudoers.d/pycaptive /etc/sudoers.d
/bin/chmod 444 /etc/sudoers.d/pycaptive

### Nginx
/bin/cp /opt/PyCaptive/deploy/nginx/pycaptive /etc/nginx/sites-available/
/bin/ln -s /etc/nginx/sites-available/pycaptive /etc/nginx/sites-enabled/pycaptive
/bin/chmod 444 /etc/nginx/sites-enabled/pycaptive

### Supervisor
/bin/cp /opt/PyCaptive/deploy/supervisor/pycaptive /etc/supervisor/conf.d/pycaptive
/usr/bin/supervisorctl restart

