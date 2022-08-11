#!/usr/bin/env python
#
# Finds HTTP/HTTPS services and prints URLs
#
# 6/14/13 - zenfosec

import sys
import re

if len(sys.argv) != 2:
    print "Usage: http_parse.py <gnmap_file>"
    sys.exit()

infile = open(sys.argv[1], "r")

port_dict = {}

for line in infile:
    if re.search("http", line, flags=re.IGNORECASE):
        httpentries = re.findall(" \d*/open/[\w\|\-\. \?\(\)]*?/\w*/[\w\|\-\. \?\(\)]*http[\w\|\-\. \|\?\(\)]*/[\w\|\-\. \?\(\)]*/", line, flags=re.IGNORECASE)
        #httpentries = line.split(", ")
        for entry in httpentries:
            if re.search("ssl|https", entry, flags=re.IGNORECASE):
                sys.stdout.write("https://")
                sys.stdout.write(line.split(" ")[1])
                sys.stdout.write(":")
                sys.stdout.write(entry.split("/")[0].strip())
                print
            else:
                sys.stdout.write("http://")
                sys.stdout.write(line.split(" ")[1])
                sys.stdout.write(":")
                sys.stdout.write(entry.split("/")[0].strip())
                print