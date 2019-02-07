
<img align="left" width="200" height="160" src="https://raw.githubusercontent.com/ivanlmj/PyCaptive/master/app/static/pycaptive_logo.png">
<p>PyCaptive is a solution for Open WiFi Hotspots, working as a Captive Portal, providing Internet Access through its authentication service.

<p>Additionally, PyCaptive can provide an authentication service for Wired networks and it can also provide an authentication system for Proxies in Transparent Mode, since these are unable to provide such service on this mode.
<br><br>

### Machine Requirements
- 3.0Ghz
- RAM 2Gb
- HDD 32Gb
- 2 NICs (100/1000Mbps)

### Software Requirements
- NIX-Like OS (Debian/Ubuntu)
- Python 3.5 + pip3 packages ([Flask, Gunicorn WSGI...](https://github.com/ivanlmj/PyCaptive/blob/master/requirements.txt))
- MongoDB 3.4
- Nginx 1.6
- IPTABLES 1.4
- Routing Configuration for traffic between NICs (IPTABLES)
- Traffic Redirection for Authenticated and Non-Authenticated Users (IPTABLES)

### Status (under improvements)
- Refactoring code for a better installation and configuration process.


Best Regards,<br>@ivanleoncz
