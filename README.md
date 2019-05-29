# MAC-changer

---

- This script requires python3.6 or later to run.
- This script currently only runs on Linux machines.
- You may need to use `sudo` to change MAC address.

This is a simple small python script that takes an interface (e.g. eth0) and a valid MAC address (e.g. 00:11:22:33:44:55) and changes the MAC address on the given interface.
Sometimes you want to change your MAC address so you can do certain things; for example, maybe a network only allows certain MAC addresses to connect, or maybe you're doing a security test of a network and need to spoof your MAC to pose as one of the network's legitimate machines while carrying out pentesting tasks.

**Usage:**

```bash
$python3 mac_changer.py -i [interface] -m [address]
```

`-i, --interface:` The interface to change MAC address for.
`-m, --new_mac:` The new MAC address to change to.

e.g.:

```bash
$python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
$python3 mac_changer.py --interface wlan0 --new_mac 00:11:44:33:22:55
```

## Caution

It is highly recommended to use this script in a virtual machine when just playing around with it, so you don't cause problems for the MAC address on your physical machine. It shouldn't be a critical problem, but it could be annoying and cause problems in future.
Just remember that this script will print the original MAC address it finds before changing to the new MAC address:

```bash
$python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
```

`Current MAC = 08:00:27:0d:da:1d`
`[+] Changing MAC address for eth0 to 00:11:22:33:44:55`
`[+] MAC address was successfully changed to 00:11:22:33:44:55`


So you can copy the original address and save somewhere then use this script again to change it back.
