#!/usr/bin/env python3

import subprocess
import argparse
import re


PROGRAM_DESCRIPTION = """
mac_changer.py
Author: Wade
Email: wwrwade@gmail.com

A small python script to quickly change MAC address for a given interface.

Currently only works on Linux machines.

Usage:
$python3 mac_changer.py [interface] [new_mac]
"""

EPILOG = """
Examples:
$python3 mac_changer.py eth0 00:11:22:33:44:55
$python3 mac_changer.py wlan0 00:11:22:33:44:55
"""


def get_arguments():
    # Create argparse object and add options
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=PROGRAM_DESCRIPTION,
        epilog=EPILOG
    )
    # Interface to set new MAC address on
    parser.add_argument(
        "interface", help="The interface to set the new MAC address on."
    )
    # The new MAC address to set
    parser.add_argument(
        "new_mac", help="The new MAC address to change to."
    )
    # parse and return arguments
    return parser.parse_args()


def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    # bring interface down, change mac, then bring it back up again
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])


def get_current_mac(interface):
    # check_output() will run a terminal command and return its output
    # save the output of ifconfig to a variable
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    # use regex to find mac address pattern in ifconfig command output.
    # subprocess.check_output() will return value as bytes, so need to convert
    # to string before searching with regex pattern
    mac_address_search_result = re.search(
        r"(\w{2}:){5}\w{2}",
        str(ifconfig_result, 'utf-8')
    )

    # check that the interface we gave to script can have a MAC address
    # e.g. lo, or loopback interface, cannot have a MAC address.
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


if __name__ == "__main__":
    # Get initial args
    args = get_arguments()

    # Get current MAC address for interface and print
    current_mac = get_current_mac(args.interface)
    print(f"[+] Current MAC = {current_mac}")

    # Change the MAC address for the interface
    change_mac(args.interface, args.new_mac)

    # Check the interface's MAC address again to see if it changed
    current_mac = get_current_mac(args.interface)
    if current_mac == args.new_mac:
        print(f"[+] MAC address successfully changed to {current_mac}")
    else:
        print("[-] MAC address not changed.")
