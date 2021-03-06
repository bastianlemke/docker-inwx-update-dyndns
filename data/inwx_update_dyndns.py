#!/usr/bin/env python3

import sys
import subprocess
import ipaddress
from time import sleep
import toml
import requests

def obtain_ip(commands, version):
    command, *fallbacks = commands
    cmd_string = " ".join(command)
    try:
        ip_string = subprocess.check_output(command).decode('ascii').strip()
        if version == 4:
            return ipaddress.IPv4Address(ip_string)
        elif version == 6:
            return ipaddress.IPv6Address(ip_string)
    except Exception as e:
        error_str = "Exception caught while running command \"{}\": {}"
        print(error_str.format(cmd_string, e), file=sys.stderr)
        if fallbacks:
            return obtain_ip(fallbacks, version)
        else:
            raise e

with open("/etc/inwx_update_dyndns.toml") as f:
    settings = toml.loads(f.read())

ipv6_enabled = settings["ipv6_enabled"]
ipv4_commands = settings["ipv4_commands"]
ipv6_commands = settings["ipv6_commands"] if ipv6_enabled else None
retry_after = settings["retry_after"]
if not ipv4_commands:
    print("At least one ipv4_command must be defined.", file=sys.stderr)
if not ipv6_commands:
    print("At least one ipv6_command must be defined.", file=sys.stderr)
ipv4 = None
ipv6 = None

while True:
    try:
        new_ipv4 = obtain_ip(ipv4_commands, 4)
        if ipv6_enabled:
            new_ipv6 = obtain_ip(ipv6_commands, 6)
        update_required = new_ipv4 != ipv4 or (ipv6_enabled and new_ipv6 != ipv6)
        if update_required:
            url = "https://dyndns.inwx.com/nic/update?myip={}".format(new_ipv4)
            if ipv6_enabled:
                url += "&myipv6={}".format(new_ipv6)
            for account in settings["account"]:
                r = requests.post(url, auth=(account["username"], account["password"]))
                print("inwx server replied:", r.text)
        ipv4 = new_ipv4
        ipv6 = new_ipv6
        sleep(settings["sleep_interval"])
    except:
        # Exception might be raised if there is no internet connectivity temporarily.
        print("All commands failed to obtain a valid IP address.", file=sys.stderr)
        sleep(retry_after)