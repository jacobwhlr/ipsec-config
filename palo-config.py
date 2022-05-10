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
SUBNET_RANGE = 1024

# IP's on the customer side
CUSTOMER_CLIENTS = ipaddress.IPv4Network("10.20.0.0/22")

# ACY NESG IP
PALO_PUBLIC_IP = ipaddress.IPv4Address("70.70.70.70")

# IP's in the NESG
NESG_SERVERS = ipaddress.IPv4Network("10.10.0.0/22")


def main():

    # Open a file
    on_boarding_file = open("test_output.txt", "w")
    for i in range(SUBNET_RANGE):

        print("===============================================================================================")
        # network -> interfaces -> tunnel
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
        print(f"set network ike gateway IP-{EXT_IP[i]} local-address ip {PALO_PUBLIC_IP}/30")
        print(f"set network ike gateway IP-{EXT_IP[i]} local-address interface ethernet1/1")
        print(f"set network ike gateway IP-{EXT_IP[i]} protocol-common nat-traversal enable no")
        print(f"set network ike gateway IP-{EXT_IP[i]} protocol-common fragmentation enable no")
        print(f"set network ike gateway IP-{EXT_IP[i]} peer-address ip {EXT_IP[i]}")
        print(f"set network ike gateway IP-{EXT_IP[i]} local-id type ipaddr id {PALO_PUBLIC_IP}")
        print(f"set network ike gateway IP-{EXT_IP[i]} peer-id type ipaddr id {EXT_IP[i]}")
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
        print(f"set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.{i + 1} destination {CUSTOMER_CLIENTS[i]}/32")
        print("===============================================================================================")
        #print(f"RJ stuff: Outside interface is: {EXT_IP[i]}")
        #print(f"RJ stuff: your acl is: {CUSTOMER_CLIENTS[i]} to {NESG_SERVERS[i]}")

        on_boarding_file.write(f"set network interface tunnel units tunnel.{i + 1} ipv6 enabled no \n")
        on_boarding_file.write(f"set network interface tunnel units tunnel.{i + 1} comment '{EXT_IP[i]} VPN' \n")
        on_boarding_file.write(f"set vsys vsys1 zone vpn network layer3 tunnel.{i + 1} \n")
        on_boarding_file.write(f"set vsys vsys1 import network interface tunnel.{i + 1} \n")
        on_boarding_file.write(f"set network virtual-router 'default-vrf' interface [ tunnel.{i + 1} ] \n")
        on_boarding_file.write(f"set network ike gateway IP-{EXT_IP[i]} authentication pre-shared-key key test123 \n")
        on_boarding_file.write(f"set network ike gateway IP-{EXT_IP[i]} protocol ikev2 ike-crypto-profile ike-phase-1 \n")
        on_boarding_file.write(f"set network ike gateway IP-{EXT_IP[i]} protocol ikev2 dpd enable yes \n")
        on_boarding_file.write(f"set network ike gateway IP-{EXT_IP[i]} protocol version ikev2 \n")
        on_boarding_file.write(f"set network ike gateway IP-{EXT_IP[i]} local-address ip {PALO_PUBLIC_IP}/30 \n")
        on_boarding_file.write(f"set network ike gateway IP-{EXT_IP[i]} local-address interface ethernet1/1 \n")
        on_boarding_file.write(f"set network ike gateway IP-{EXT_IP[i]} protocol-common nat-traversal enable no \n")
        on_boarding_file.write(f"set network ike gateway IP-{EXT_IP[i]} protocol-common fragmentation enable no \n")
        on_boarding_file.write(f"set network ike gateway IP-{EXT_IP[i]} peer-address ip {EXT_IP[i]} \n")
        on_boarding_file.write(f"set network ike gateway IP-{EXT_IP[i]} local-id type ipaddr id {PALO_PUBLIC_IP} \n")
        on_boarding_file.write(f"set network ike gateway IP-{EXT_IP[i]} peer-id type ipaddr id {EXT_IP[i]} \n")
        on_boarding_file.write(f"set network tunnel ipsec IP-{EXT_IP[i]} auto-key ike-gateway IP-{EXT_IP[i]} \n")
        on_boarding_file.write(f"set network tunnel ipsec IP-{EXT_IP[i]} auto-key proxy-id Test{i} protocol any \n")
        on_boarding_file.write(f"set network tunnel ipsec IP-{EXT_IP[i]} auto-key proxy-id Test{i} local {NESG_SERVERS[i]} \n")
        on_boarding_file.write(f"set network tunnel ipsec IP-{EXT_IP[i]} auto-key proxy-id Test{i} remote {CUSTOMER_CLIENTS[i]} \n")
        on_boarding_file.write(f"set network tunnel ipsec IP-{EXT_IP[i]} auto-key ipsec-crypto-profile ipsec-phase-2 \n")
        on_boarding_file.write(f"set network tunnel ipsec IP-{EXT_IP[i]} tunnel-monitor enable no \n")
        on_boarding_file.write(f"set network tunnel ipsec IP-{EXT_IP[i]} tunnel-interface tunnel.{i + 1} \n")
        on_boarding_file.write(f"set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.{i + 1} interface tunnel.{i + 1} \n")
        on_boarding_file.write(f"set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.{i + 1} metric 10 \n")
        on_boarding_file.write(f"set network virtual-router 'default-vrf' routing-table ip static-route Route_to_tunnel.{i + 1} destination {CUSTOMER_CLIENTS[i]}/32 \n")
        #on_boarding_file.write(f"RJ stuff: Outside interface is: {EXT_IP[i]} \n")
        #on_boarding_file.write(f"RJ stuff: your acl is: {CUSTOMER_CLIENTS[i]} to {NESG_SERVERS[i]} \n")
        on_boarding_file.write("\n")
        on_boarding_file.write("\n")

    # Close opend file
    on_boarding_file.close()


if __name__ == "__main__":
    main()
