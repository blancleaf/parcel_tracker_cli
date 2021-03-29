#!/usr/bin/python3

import sys
import requests
import json
from os import path

#Output coloring

BLUE    = '\033[94m'
RED     = '\033[91m'
CYAN    = '\033[96m'
ENDC    = '\033[0m'

OFFSET = 18 #ASCII encoding offset used by the API

if len(sys.argv) < 2:
    print("Usage: {} <argument>".format(sys.argv[0]))
    print("<argument> can be a universal tracking number or a path to a file containing 1 number per line")
    raise SystemExit

numbers = []

if path.exists(sys.argv[1]):
    with open(sys.argv[1], "r") as fp:
        numbers = fp.readlines()

else:
    numbers.append(sys.argv[1].upper())

enc_msg = []

for number in numbers:

    for c in number:
        enc_msg.append(chr(ord(c) + OFFSET))

    enc_msgStr = "".join(enc_msg)

    req_data = { 'trackingId': enc_msgStr, 'carrier': "Auto-Detect", 'language': "en", 'country': "Auto-Detect", 'platform': "web-desktop", 'wd': "false", 'c': "false", 'p': "2", 'l': "2", 'se': "1920x1080,Linux+x86_64,Gecko,Mozilla,Netscape,Google+Inc.,4g" }

    req = requests.post("https://parcelsapp.com/api/v2/parcels", data=req_data)

    if not req.ok:
        print("{}Got {} HTTP code{}".format(RED, req.status_code, ENDC))
        raise SystemExit

    if "error" in req.text:
        print("{}Got {} error{}".format(RED, req.json()['error'], ENDC))
        print("(Please check your tracking number)")
        raise SystemExit

    data = req.json()

    print("{}".format(number))
    print("{} -----------> {}".format(data['origin'], data['destination']))
    print("Status: {}\n".format(data['status']))

    for state in data['states']:
        print("{}{}\t{} carrier: {}{}\t{}".format(BLUE, state['date'], CYAN, data['carriers'][state['carrier']], ENDC, state['status']))
