# PyCaptive

Internet Access for Wi-Fi Hotspots based on Python.

PyCaptive is an authentication service for Open WiFi Hotspots, working as a Captive Portal. That means: users who wish to have Internet Access through an Open Wifi Hotspot which is backed by PyCaptive, must authenticate to open a session, which is based on Username, IP Address and Expire Time, according with Login Time.  Additionally, PyCaptive performs the authentication role for Wired networks and for network servers that have Transparent Proxy service, since that Proxies in Transparent mode, are not capable to provide authentication.

### Characteristics
- Front-end: HTML, CSS and Jinja2
- Back-end: Python, Flask, MongoDB, IPTABLES
- [See requirements.txt](https://github.com/ivanlmj/PyCaptive/blob/master/requirements.txt)

### Server Requirements
- two NICs (100/1000Mbps)
- NIX-Like Operating System (Debian, Ubuntu, etc.)
- IPTABLES Firewall
- Routing Configuration (traffic redirection between NICs)

For doubts, questions or suggestions: [@ivanleoncz](https://twitter.com/ivanleoncz)
