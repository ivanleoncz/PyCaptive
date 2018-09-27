

    IPTABLES setup and workflow for PyCaptive operation


        *mangle:
          1. Ensures that INTERNET and PYCAPTIVE chains are created.
          2. INTERNET: receives traffic from authorized IPs (bypassing PyCaptive).
          3. PYCAPTIVE: receives traffic from UNauthorized IPs.
          4. Traffic to port 80 (TCP/UDP): directed to PYCAPTIVE chain
          5. Traffic to port 443 (TCP/UDP): DROPPED.
          6. Packets traversing PYCAPTIVE chain: directed and marked at MARK chain
          7. Packets traversing INTERNET chain: ACCEPTED.

        *nat:
          8. NOT MARKED packets: can access PyCaptive, after successful authentication.
          9. MARKED packets: directed to NGINX -> GUNICORN -> PyCaptive.

        *mangle:
          10. Successful authentication: rule added on top of *mangle table (INTERNET access).


###############################################################################

    Router (file: router.v4)

        Model:

          - TWO networks behind ONE interface
          - PyCaptive is enabled just for one network
          - rules for directing HTTP traffic for SQUID
          - rules for directing *marked* HTTPS traffic to PyCaptive
          - rules for allowed protocols
          - logging configuration

        Scenario:

          LAN -> eth2
          - network: 192.168.0.0/24 - 255.255.255.0 (PyCaptive)
          - gateway: 192.168.0.1
          -----------------------------------------
          - network: 10.255.255.0/26 - 255.255.255.192
          - gateway: 10.255.255.62

          WAN -> eth1

################################################################################

    Router + Transparent Proxy (file: router+transparent_proxy.v4)

	Model:

	# to be defined...

        Scenario:

          LAN -> eth2
          - network: 192.168.0.0/24 - 255.255.255.0
          - gateway: 192.168.0.1

          WAN -> eth1

################################################################################
