#!/bin/bash

if [[ "$EUID" == 0 ]] ; then
	if [ -f /usr/local/bin/gunicorn ]; then
		echo "Pycaptive is running: standalone (with WSGI)."
		/usr/local/bin/gunicorn --preload --name gunicorn_master --user gunicorn --group gunicorn --workers 4 --pythonpath /opt/probe wsgi
	else
		echo -e "\nNot found: /usr/local/bin/gunicorn\n"
	fi
else
	echo -e "\nMust have root privileges!\n    Ex.: sudo python3 run.py\n"
fi
