#!/bin/bash

PYCAPTIVE_USR="pycaptive"
INSTALL_TIMESTAMP="`/bin/date`"

function user_setup {

    COMMENT="Account for running PyCaptive"
    PC_SHELL="/usr/sbin/nologin"

    /usr/sbin/groupadd $PYCAPTIVE_USR -g 14090
    /usr/sbin/useradd $PYCAPTIVE_USR -s $PC_SHELL -c "$COMMENT" -u 14090 -g 14090

}

function log_setup {

    LOGDIR="/var/log/pycaptive"
    LOGFILE="$LOGDIR/pycaptive.log"

    mkdir $LOGDIR
    chown $PYCAPTIVE_USR:$PYCAPTIVE_USR $LOGDIR
    chmod 770 $LOGDIR
    echo "PyCaptive Deploy started at: $INSTALL_TIMESTAMP" > $LOGFILE
    chown $PYCAPTIVE_USR:$PYCAPTIVE_USR $LOGFILE
    chmod 660 $LOGFILE
    cp -p logrotate/pycaptive /etc/logrotate.d/

}

function sudoers_setup {

    SUDOERS_FILE="/etc/sudoers.d/pycaptive"
    CONNTRACK_BIN="/usr/sbin/conntrack"
    IPTABLES_BIN="/sbin/iptables"

    echo "$PYCAPTIVE_USR ALL=(root:root) NOPASSWD:$IPTABLES_BIN" > $SUDOERS_FILE
    echo "$PYCAPTIVE_USR ALL=(root:root) NOPASSWD:$CONNTRACK_BIN" >> $SUDOERS_FILE
    chmod 0440 $SUDOERS_FILE

}

function nginx_setup {

    NGINX_DIR="/etc/nginx"

    cp nginx/pycaptive "$NGINX_DIR/sites-available/"
    ln -s "$NGINX_DIR/sites-available/pycaptive" "$NGINX_DIR/sites_enabled/pycaptive"

}

function supervisor_setup {
    
    SUPERVISOR_DIR="/etc/supervisor/conf.d"
    
    cp supervisor/pycaptive "$SUPERVISOR_DIR/conf.d/"
}

function check_binnaries {

    packages=`dpkg-query -l | grep ^'.i' | awk '{print $2}' | \
              grep 'python3-pip\|nginx$\|iptables$\|conntrack$\|supervisor$\|mongo-org'`

    package_counter=0
    package_executable=0
    for pkg in $packages; do
	echo "Checking package: $pkg"
        ((package_counter++))
        for bin in `whereis $pkg`; do
            if [[ $bin =~ "bin" ]]; then
		echo "- binnary found: $bin"
                if [ -x $bin ]; then
		    echo "- executable: yes"
                    ((package_executable++))
		fi
            fi
        done
    done

    if [ $package_counter -q $package_executable ]; then
        echo "Final status: OK"
    else
	echo "Final status: NOK"
	echo -e "INFO: please, review installation for the following packages"
	echo "iptables\nconntrack\|nginx\|python3-pip\|supervisor\|mongod"
	exit
    fi

}


if [ "$UID" == 0 ]
then
    user_setup
    log_setup
    sudoers_setup
else
    echo "You don't have root privileges!"
fi
