############################################################################### 
#                                                                               
#    Router                                                 
#                                                                               
#       Model                                                                    
#                                                                               
#         - TWO networks behind ONE interface                                            
#	  - PyCaptive is enabled just for one network                            
#         - rules for directing HTTP traffic for SQUID                           
#         - rules for directing *marked* HTTPS traffic to PyCaptive              
#         - rules for allowed protocols                                          
#         - logging configuration                                                
#                                                                               
#       Scenario:                                                                
#                                                                               
#         LAN -> eth2                                                              
#         - network: 192.168.0.0/24 - 255.255.255.0 (PyCaptive)                              
#         - gateway: 192.168.0.1                                                  
#         -----------------------------------------                              
#         - network: 10.255.255.0/26 - 255.255.255.192                               
#         - gateway: 10.255.255.62                                                  
#                                                                               
#         WAN -> eth1
#                                                              
################################################################################                                                                               


################################################################################
#                                                                               
#    Router + Transparent Proxy                                                 
#                                                                                                                                                       
#       Logic implemented (from table to table)                   
#                                                                               
#         *mangle:                                                                
#                                                                               
#           1. Ensure that INTERNET and PYCAPTIVE chains are created.           
#           2. Traffic with port 80 as destination (TCP/UDP) is directed to PYCAPTIVE chain.
#           3. Traffic with port 443 as destination (TCP/UDP) is DROPPED.       
#           4. Packets that traverse PYCAPTIVE chain, are directed to MARK chain, where each one receive "mark 1".
#           5. Packets that traverse INTERNET chain, are just ACCEPTED. (see 7. item).
#                                                                               
#         *nat:                                                                   
#           6. PyCaptive interface accessible after successful authentication, escaping "NOT MARKED packets" rules
#           7. MARKED PACKETS: directed to NGINX <-> GUNICORN <-> PyCaptive.    
#                                                                               
#         *mangle:                                                                
#                                                                               
#           8. After PyCaptive authentication (*nat table), rules are added     
#           on top of *mangle table (per IP), with INTERNET chain as destination.
#                                                                               
#       Scenario:                                                                  
#                                                                               
#         LAN -> eth2                                                             
#         - network: 192.168.0.0/24 - 255.255.255.0                               
#         - gateway: 192.168.0.1                                                  
#                                                                               
#         WAN -> eth1                                                             
#                                                                               
################################################################################
