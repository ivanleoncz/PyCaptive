#!/usr/bin/env python3

import os
import json
from string import Template
import sys

from app.modules.helper import search_and_load_ini

# Loading pycaptive.ini file as flat dictionary.
ini = search_and_load_ini()

# expanding ini dictionary, by adding variables exported via install.sh
ini["USER"] = os.environ.get("USER")
ini["CONF_DIR"] = os.environ.get("CONF_DIR")
ini["INSTALL_DIR"] = os.environ.get("INSTALL_DIR")

# Templates (source and destination)
templates = {
    "gen_templates/iptables": "/tmp/rules.v4",
    "gen_templates/logrotate": "/tmp/pycaptive_logrotate",
    "gen_templates/nginx": "/tmp/pycaptive_nginx",
    "gen_templates/sudo": "/tmp/pycaptive_sudo",
    "gen_templates/systemd": "/tmp/pycaptive_systemd.conf"
}

def generate_file(template: str, new_file: str) -> None:
    """ Takes template path and writes new file, performing substitution of all
    template variables by key/values provided via search_and_load_ini.

    Args:
        template : template that is going to be used for file generation
        new_file : file to be created, based on template + ini
    """
    with open(template, 'r') as template_f:
        t = Template(template_f.read())
        with open(new_file, 'w') as new_f:
            new_f.write(t.substitute(ini))


if __name__ == "__main__":
    if os.environ.get("GEN_CALLER") == "install.sh":
        for template, new_file in templates.items():
            generate_file(template, new_file)
            if os.path.isfile(new_file):
                print(f" *** {template}: sucessfully generated.")
            else:
                print(f" !!! {template}: fail to generate (aborting).")
                sys.exit()
    else:
        print("[ERROR]: must execute it via install.sh")

