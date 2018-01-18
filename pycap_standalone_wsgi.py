#!/bin/bash

if [[ "$EUID" == 0 ]] ; then
	echo -e "\nPycaptive is running (standalone + WSGI).\n"
	gunicorn --preload --name gunicorn_master --user gunicorn --group gunicorn --workers 4 --pythonpath /opt/probe wsgi
else
	echo -e "\nMust have root privileges!\n\nRun: sudo ./standalone_wsgi.py\n"
fi
