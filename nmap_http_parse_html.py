#!/usr/bin/env python3
#
# Finds HTTP/HTTPS services and prints URLs with hostnames if available,
# formatted as clickable HTML links.
#
# 6/14/13 - zenfosec
# 4/4/25 - updating to python3

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

# Start the HTML document
print("<!DOCTYPE html>")
print("<html>")
print("<head>")
print("<title>HTTP/HTTPS Services</title>")
print("</head>")
print("<body>")
print("<h1>HTTP/HTTPS Services</h1>")
print("<ul>")

# Open the input file using a context manager for better resource management
with open(sys.argv[1], "r") as infile:
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
                
                # Construct the URL based on whether a hostname is available
                if re.search("ssl|https", entry, flags=re.IGNORECASE):
                    url = f"https://{hostname or ip_address}:{port}"
                else:
                    url = f"http://{hostname or ip_address}:{port}"
                
                # Print the URL as a clickable HTML link
                print(f'<li><a href="{url}" target="_blank">{url}</a></li>')

# End the HTML document
print("</ul>")
print("</body>")
print("</html>")
