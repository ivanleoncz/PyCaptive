#!/bin/bash
#
# Use this script for install and uninstall purposes.
#
# For further information, use -h or --help.
#
# Author: @ivanleoncz


help () {
	basename $0
	echo -e "\t-h, --help:      displays this help"
	echo -e "\t-i, --install:   creates etc directory and .ini file, also creates pycaptive user"
	echo -e "\t-u, --uninstall: undo install instructions"
}

install () {
	PYCAPTIVE_ETC="/etc/pycaptive"
	echo "[INFO]: creating pycaptive user"
	/usr/bin/sudo /usr/sbin/useradd pycaptive -s /usr/sbin/nologin
	echo "[INFO]: creating ${PYCAPTIVE_ETC} directory" 
	/bin/mkdir /etc/pycaptive
	echo "[INFO]: installing pycaptive.ini to ${PYCAPTIVE_ETC} directory"
	/usr/bin/install -m 664 -o pycaptive -g pycaptive app/pycaptive.ini /etc/pycaptive
	echo "[INFO]: defining owner of ${PYCAPTIVE_ETC} directory"
	/bin/chown pycaptive:pycaptive ${PYCAPTIVE_ETC}
	echo "[INFO]: defining permission of ${PYCAPTIVE_ETC} directory"
	/bin/chmod 775 ${PYCAPTIVE_ETC}
}


uninstall () {
	PYCAPTIVE_ETC="/etc/pycaptive"
	echo "[INFO]: deleting ${PYCAPTIVE_ETC} directory and its contents"
	/bin/rm -rf /etc/pycaptive
	echo "[INFO]: deleting pycaptive user"
	/usr/sbin/userdel pycaptive
}

if [[ "$UID" == 0 ]]; then
	
	if [[ -z "$1" ]] ; then
		help
		exit 1
	fi

	case "$1" in
			-h|--help) help
			;;
			-i|--install) install
			;;
			-u|--uninstall) uninstall
			;;
			*) help
			;;
	esac
else
	echo "[ERROR]: script must be executed by root user (use sudo)"
fi
