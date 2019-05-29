#!/usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    arg_options, arguments = parser.parse_args()
    if not arg_options.interface:
        parser.error("[-] Please specify an interface, use --help for info.")
    if not arg_options.new_mac:
        parser.error("[-] Please specify a new MAC, use --help for info.")
    return arg_options


def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")

    # This method is unsafe because we can run our own linux commands inside
    # subprocess.run(f"ifconfig {interface} down", shell=True)
    # subprocess.run(f"ifconfig {interface} hw ether {new_mac}", shell=True)
    # subprocess.run(f"ifconfig {interface} up", shell=True)

    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])


def get_current_mac(interface):
    # check_output() will run the command and return its output
    # can save the output to a variable to print
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    # using regex to find mac address pattern in ifconfig command output
    mac_address_search_result = re.search(r"(\w{2}:){5}\w{2}", str(ifconfig_result, 'utf-8'))
    # check that the interface we gave can have a mac address
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


if __name__ == "__main__":
    options = get_arguments()

    current_mac = get_current_mac(options.interface)
    print(f"Current MAC = {current_mac}")

    change_mac(options.interface, options.new_mac)

    current_mac = get_current_mac(options.interface)
    if current_mac == options.new_mac:
        print(f"[+] MAC address was successfully changed to {current_mac}")
    else:
        print("[-] MAC address did not get changed.")
