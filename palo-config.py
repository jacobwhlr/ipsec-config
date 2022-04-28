"""
proxy id = policy based
proxy id = crypto acl
Assumptions:
    Steve sucks
    Palo Public IP will be 70.70.70.70, interface will be Ethernet1/1

Website:
    CLI: https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000ClHsCAK
    GUI: https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000ClJ3CAK
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

    # TODO: step X: create zone
    # TODO: step X: create ike profile for phase 1
    # TODO: step X: create ipsec profile for phase 2
    # TODO: step X: create ike gateway




    # Close opend file
    # on_boarding_file.close()


if __name__ == "__main__":
    main()
