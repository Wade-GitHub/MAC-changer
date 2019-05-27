#!/usr/bin/env python3

import subprocess
import optparse


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
change_mac(options.interface, options.new_mac)
