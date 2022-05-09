"""
proxy id = policy based
proxy id = crypto acl
Assumptions:
    Steve sucks
    Palo Public IP will be 70.70.70.70, interface will be Ethernet1/1
    Zone: Name: VPN, Type: Layer3, Interfaces: tunnel.X
    Virtual Router: default-vrf
    Ike crypto profile: Name: ike-phase-1
    IPSec crypto profile: Name: ipsec-phase-2

Website:
    CLI: https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000ClHsCAK
    GUI: https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000ClJ3CAK
         https://www.gns3network.com/ipsec-tunnel-between-palo-alto-and-cisco-asa-firewall/
         https://www.youtube.com/watch?v=Kmi4DjBFgwA

"""

import ipaddress

# Public IP on the customer end
EXT_IP = ipaddress.IPv4Network("20.20.0.0/22")

# IP's on the customer side
CUSTOMER_CLIENTS = ipaddress.IPv4Network("10.20.0.0/22")

# ACY NESG IP
PALO_PUBLIC_IP = ipaddress.IPv4Address("70.70.70.70")
NEXT_HOP = ipaddress.IPv4Address("70.70.70.75")

# IP's in the NESG
NESG_SERVERS = ipaddress.IPv4Network("10.10.0.0/22")


def main():

    # Open a file
    # on_boarding_file = open("test_output.txt", "w")
    for i in range(0, 2):
        print("===============================================================================================")
        # Tunnel interface commands
        print(f"set network interface tunnel units tunnel.{i + 1} ipv6 enabled no")
        print(f"set network interface tunnel units tunnel.{i + 1} comment '{EXT_IP[i]} VPN'")
        print(f"set vsys vsys1 zone vpn network layer3 tunnel.{i + 1}")
        print(f"set vsys vsys1 import network interface tunnel.{i + 1}")
        print(f"set network virtual-router 'default-vrf' interface [ tunnel.{i + 1} ]")
        print("===============================================================================================")
        # network -> profile -> Ike gateway
        print(f"set network ike gateway IP-{EXT_IP[i]} authentication pre-shared-key key test123")
        print(f"set network ike gateway IP-{EXT_IP[i]} protocol ikev2 ike-crypto-profile ike-phase-1")
        print(f"set network ike gateway IP-{EXT_IP[i]} protocol ikev2 dpd enable yes")
        print(f"set network ike gateway IP-{EXT_IP[i]} protocol version ikev2")
        print(f"set network ike gateway IP-{EXT_IP[i]} local-address ip {PALO_PUBLIC_IP}")
        print(f"set network ike gateway IP-{EXT_IP[i]} local-address interface ethernet1/1")
        print(f"set network ike gateway IP-{EXT_IP[i]} protocol-common nat-traversal enable no")
        print(f"set network ike gateway IP-{EXT_IP[i]} protocol-common fragmentation enable no")
        print(f"set network ike gateway IP-{EXT_IP[i]} peer-address ip {EXT_IP[i]}")
        print(f"set network ike gateway IP-{EXT_IP[i]} local-id id {PALO_PUBLIC_IP}")
        print(f"set network ike gateway IP-{EXT_IP[i]} local-id type ipaddr")
        print(f"set network ike gateway IP-{EXT_IP[i]} peer-id id {EXT_IP[i]}")
        print(f"set network ike gateway IP-{EXT_IP[i]} peer-id type ipaddr")
        print("===============================================================================================")
        # network -> ipsec tunnels
        print(f"set network tunnel ipsec IP-{EXT_IP[i]} auto-key ike-gateway IP-{EXT_IP[i]}")
        print(f"set network tunnel ipsec IP-{EXT_IP[i]} auto-key proxy-id Test{i} protocol any")
        print(f"set network tunnel ipsec IP-{EXT_IP[i]} auto-key proxy-id Test{i} local {NESG_SERVERS[i]}")
        print(f"set network tunnel ipsec IP-{EXT_IP[i]} auto-key proxy-id Test{i} remote {CUSTOMER_CLIENTS[i]}")
        print(f"set network tunnel ipsec IP-{EXT_IP[i]} auto-key ipsec-crypto-profile ipsec-phase-2")
        print(f"set network tunnel ipsec IP-{EXT_IP[i]} tunnel-monitor enable no")
        print(f"set network tunnel ipsec IP-{EXT_IP[i]} tunnel-interface tunnel.{i + 1}")
        print("===============================================================================================")
        print(f"set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.{i + 1} interface tunnel.{i + 1}")
        print(f"set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.{i + 1} metric 10")
        print(f"set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.{i + 1} destination {CUSTOMER_CLIENTS[i]}")
        print("===============================================================================================")

    # Close opend file
    # on_boarding_file.close()


if __name__ == "__main__":
    main()

"""
Output:
===============================================================================================
set network interface tunnel units tunnel.1 ipv6 enabled no
set network interface tunnel units tunnel.1 comment '20.20.0.0 VPN'
set vsys vsys1 zone vpn network layer3 tunnel.1
set vsys vsys1 import network interface tunnel.1
set network virtual-router 'default-vrf' interface [ tunnel.1 ]
===============================================================================================
set network ike gateway IP-20.20.0.0 authentication pre-shared-key key test123
set network ike gateway IP-20.20.0.0 protocol ikev2 ike-crypto-profile ike-phase-1
set network ike gateway IP-20.20.0.0 protocol ikev2 dpd enable yes
set network ike gateway IP-20.20.0.0 protocol version ikev2
set network ike gateway IP-20.20.0.0 local-address ip 70.70.70.70
set network ike gateway IP-20.20.0.0 local-address interface ethernet1/1
set network ike gateway IP-20.20.0.0 protocol-common nat-traversal enable no
set network ike gateway IP-20.20.0.0 protocol-common fragmentation enable no
set network ike gateway IP-20.20.0.0 peer-address ip 20.20.0.0
set network ike gateway IP-20.20.0.0 local-id id 70.70.70.70
set network ike gateway IP-20.20.0.0 local-id type ipaddr
set network ike gateway IP-20.20.0.0 peer-id id 20.20.0.0
set network ike gateway IP-20.20.0.0 peer-id type ipaddr
===============================================================================================
set network tunnel ipsec IP-20.20.0.0 auto-key ike-gateway IP-20.20.0.0
set network tunnel ipsec IP-20.20.0.0 auto-key proxy-id Test0 protocol any
set network tunnel ipsec IP-20.20.0.0 auto-key proxy-id Test0 local 10.10.0.0
set network tunnel ipsec IP-20.20.0.0 auto-key proxy-id Test0 remote 10.20.0.0
set network tunnel ipsec IP-20.20.0.0 auto-key ipsec-crypto-profile ipsec-phase-2
set network tunnel ipsec IP-20.20.0.0 tunnel-monitor enable no
set network tunnel ipsec IP-20.20.0.0 tunnel-interface tunnel.1
===============================================================================================
set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.1 interface tunnel.1
set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.1 metric 10
set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.1 destination 10.20.0.0
===============================================================================================
===============================================================================================
set network interface tunnel units tunnel.2 ipv6 enabled no
set network interface tunnel units tunnel.2 comment '20.20.0.1 VPN'
set vsys vsys1 zone vpn network layer3 tunnel.2
set vsys vsys1 import network interface tunnel.2
set network virtual-router 'default-vrf' interface [ tunnel.2 ]
===============================================================================================
set network ike gateway IP-20.20.0.1 authentication pre-shared-key key test123
set network ike gateway IP-20.20.0.1 protocol ikev2 ike-crypto-profile ike-phase-1
set network ike gateway IP-20.20.0.1 protocol ikev2 dpd enable yes
set network ike gateway IP-20.20.0.1 protocol version ikev2
set network ike gateway IP-20.20.0.1 local-address ip 70.70.70.70
set network ike gateway IP-20.20.0.1 local-address interface ethernet1/1
set network ike gateway IP-20.20.0.1 protocol-common nat-traversal enable no
set network ike gateway IP-20.20.0.1 protocol-common fragmentation enable no
set network ike gateway IP-20.20.0.1 peer-address ip 20.20.0.1
set network ike gateway IP-20.20.0.1 local-id id 70.70.70.70
set network ike gateway IP-20.20.0.1 local-id type ipaddr
set network ike gateway IP-20.20.0.1 peer-id id 20.20.0.1
set network ike gateway IP-20.20.0.1 peer-id type ipaddr
===============================================================================================
set network tunnel ipsec IP-20.20.0.1 auto-key ike-gateway IP-20.20.0.1
set network tunnel ipsec IP-20.20.0.1 auto-key proxy-id Test1 protocol any
set network tunnel ipsec IP-20.20.0.1 auto-key proxy-id Test1 local 10.10.0.1
set network tunnel ipsec IP-20.20.0.1 auto-key proxy-id Test1 remote 10.20.0.1
set network tunnel ipsec IP-20.20.0.1 auto-key ipsec-crypto-profile ipsec-phase-2
set network tunnel ipsec IP-20.20.0.1 tunnel-monitor enable no
set network tunnel ipsec IP-20.20.0.1 tunnel-interface tunnel.2
===============================================================================================
set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.2 interface tunnel.2
set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.2 metric 10
set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.2 destination 10.20.0.1
===============================================================================================
"""