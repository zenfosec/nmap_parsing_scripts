#!/usr/bin/env python3
#
# Finds HTTP/HTTPS services and prints URLs with hostnames if available, otherwise IP address
# Updating 2013 python2 script to python3

import sys
import re
import socket

def get_hostname(ip_address):
    """
    Perform reverse DNS lookup to get the hostname for a given IP address.
    Returns the hostname if found, otherwise returns None.
    """
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname
    except socket.herror:
        return None

if len(sys.argv) != 2:
    print("Usage: http_parse.py <gnmap_file>")
    sys.exit()

# Open the input file using a context manager for better resource management
with open(sys.argv[1], "r") as infile:
    port_dict = {}

    for line in infile:
        if re.search("http", line, flags=re.IGNORECASE):
            httpentries = re.findall(
                r" \d*/open/[\w\|\-\. \?\(\)]*?/\w*/[\w\|\-\. \?\(\)]*http[\w\|\-\. \|\?\(\)]*/[\w\|\-\. \?\(\)]*/",
                line,
                flags=re.IGNORECASE,
            )
            for entry in httpentries:
                ip_address = line.split(" ")[1]
                port = entry.split("/")[0].strip()
                
                # Perform reverse DNS lookup
                hostname = get_hostname(ip_address)
                
                # Use hostname if available; fallback to IP address otherwise
                if re.search("ssl|https", entry, flags=re.IGNORECASE):
                    if hostname:
                        print(f"https://{hostname}:{port}")
                    else:
                        print(f"https://{ip_address}:{port}")
                else:
                    if hostname:
                        print(f"http://{hostname}:{port}")
                    else:
                        print(f"http://{ip_address}:{port}")
