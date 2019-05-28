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


options = get_arguments()
#change_mac(options.interface, options.new_mac)

# check_output() will run the command and return its output
# can save the output to a variable to print
ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
# have to convert bytes object to string
print(str(ifconfig_result, 'utf-8'))

# using regex to find mac address pattern in ifconfig command output
mac_address_search_result = re.search(r"(\w{2}:){5}\w{2}", str(ifconfig_result, 'utf-8'))
# check that the interface we gave can have a mac address
if mac_address_search_result:
    print(mac_address_search_result.group(0))
else:
    print("[-] Could not read MAC address.")
