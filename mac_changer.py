#!/usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
    # Create OptionParser object and add options
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    arg_options, arguments = parser.parse_args()
    # if user doesn't give interface option, show error
    if not arg_options.interface:
        parser.error("[-] Please specify an interface, use --help for info.")
    # if user doesn't give mac address option, show error
    if not arg_options.new_mac:
        parser.error("[-] Please specify a new MAC address, use --help for info.")
    return arg_options


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
    mac_address_search_result = re.search(r"(\w{2}:){5}\w{2}", str(ifconfig_result, 'utf-8'))
    # check that the interface we gave to script can have a MAC address
    # e.g. lo, or loopback interface, cannot have a MAC address.
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


if __name__ == "__main__":
    # Get initial options
    options = get_arguments()

    # Get current MAC address for interface and print
    current_mac = get_current_mac(options.interface)
    print(f"Current MAC = {current_mac}")

    # Change the MAC address for the interface
    change_mac(options.interface, options.new_mac)

    # Check the interface's MAC address again to see if it changed
    current_mac = get_current_mac(options.interface)
    if current_mac == options.new_mac:
        print(f"[+] MAC address successfully changed to {current_mac}")
    else:
        print("[-] MAC address not changed.")
