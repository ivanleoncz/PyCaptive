#!/bin/bash
#
# Use this script for install and uninstall purposes.
#
# For further information, use -h or --help.
#
# Author: @ivanleoncz

# ---------------------------------------------------------------------------
#  Attention
# ---------------------------------------------------------------------------
#  These variables are used in two locations:
#    1. Here.
#    2. gen_config_files.py
#
#  Leave them as it is, specially GEN_CALLER, unless you have a good reason.
# ---------------------------------------------------------------------------
export USER="pycaptive"
export CONF_DIR="/etc/pycaptive"
export INSTALL_DIR="/opt/pycaptive"
export GEN_CALLER="install.sh"

help () {
	basename $0
	echo -e "\t-h, --help:      displays this help"
	echo -e "\t-i, --install:   creates etc directory and .ini file, also creates pycaptive user"
	echo -e "\t-u, --uninstall: undo install instructions"
}

install () {
	echo "[INFO]: creating ${USER} user"
	/usr/bin/sudo /usr/sbin/useradd ${USER} -s /usr/sbin/nologin
	echo "[INFO]: creating ${CONF_DIR} directory"
	/bin/mkdir ${CONF_DIR}
	echo "[INFO]: installing pycaptive.ini to ${CONF_DIR} directory"
	/usr/bin/install -m 664 -o ${USER} -g ${USER} app/pycaptive.ini ${CONF_DIR}
	echo "[INFO]: defining ${USER} as owner of ${CONF_DIR} directory"
	/bin/chown ${USER}:${USER} ${CONF_DIR}
	echo "[INFO]: defining permissions of ${CONF_DIR} directory"
	/bin/chmod 775 ${CONF_DIR}
	echo "[INFO]: installing repo files at ${INSTALL_DIR} directory"
	/usr/bin/rsync -a . ${INSTALL_DIR} --exclude .git --exclude .gitignore
	echo "[INFO]: defining ${USER} as owner of ${INSTALL_DIR} directory"
	/bin/chown -R ${USER}:${USER} ${INSTALL_DIR}
	echo "[INFO]: defining permissions on ${INSTALL_DIR} directory"
	/usr/bin/find ${INSTALL_DIR} -type d -exec chmod 775 {} \;
	/usr/bin/find ${INSTALL_DIR} -type f \( -name "*.py" -o -name "*.sh" \) -exec chmod 554 {} \;
	echo "[INFO]: generating configuration files for services, based on gen_templates files"
	python3 gen_config_files.py
}


uninstall () {
	echo "[INFO]: deleting ${CONF_DIR} directory and its contents"
	/bin/rm -rf ${CONF_DIR}
	echo "[INFO]: deleting ${INSTALL_DIR} directory and its contents"
	/bin/rm -rf ${INSTALL_DIR}
	echo "[INFO]: deleting pycaptive user"
	/usr/sbin/userdel ${USER}
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
