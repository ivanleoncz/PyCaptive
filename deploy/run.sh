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


if [ "$UID" == 0 ]
then
    user_setup
    log_setup
    sudoers_setup
else
    echo "You don't have root privileges!"
fi
