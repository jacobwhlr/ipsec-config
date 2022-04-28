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

# IP's in the NESG
PALO_SERVERS = ipaddress.IPv4Network("10.10.0.0/22")


def main():

    # Open a file
    # on_boarding_file = open("test_output.txt", "w")
    for i in range(0, 5):
        print(f"set network interface tunnel units tunnel.{i + 1} ipv6 enabled no")
        print(f"set network interface tunnel units tunnel.{i + 1} comment '{EXT_IP[i]} VPN'")
        print(f"set zone vpn network layer3 tunnel.{i + 1}")
        print(f"set network virtual-router 'default-vrf' interface [ tunnel.{i + 1} ]")
        print("\n")

    # Close opend file
    # on_boarding_file.close()


if __name__ == "__main__":
    main()
