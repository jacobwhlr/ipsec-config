"""
Assumptions:

"""

import ipaddress

EXT_IP = ipaddress.IPv4Network("192.4.2.0/28")


def main():
    for i in EXT_IP:
        print(i)


if __name__ == "__main__":
    main()
