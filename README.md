# PyCaptive

### A Captive Portal written in Python (and Flask).

## Purposes

- to provide a system for authentication of users who want to obtain access to the Internet (Wired or WI-FI) on a Transparent Proxy 
- to maintain a database and history of authenticated "Users" VS "IP addresses"
- to update ACL file used for IPTABLES/Netfilter rules

## Status

- Under Development

## Error Code Definition

##### IPTABLES/Netfilter
- 0x0000 - Successful
- 0x0fw1 - Exception
- 0x0fw2 - Not Found

##### Database/Login
- 0x0000 - Successful
- 0x0db1 - Exception
- 0x0db2 - User Not Found
- 0x0db3 - Wrong Password
- 0x0db4 - Login Record Failed


For any questions,

@ivanleoncz
