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

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0' #Random UA

OFFSET = 54 #ASCII encoding offset used by the API

api_addr = "https://parcelsapp.com/api/v2/parcels"

#parcelsapp.com API expects tracking numbers to be encoded in this specific way
#   :]

def apiEncodeChar(char):

    asciival = ord(char)
    tempval=asciival-OFFSET
    if tempval < 0:
        res=126+tempval
    else:
        res=tempval

    return chr(res)

def apiEncodeString(string):    
    res = ""
    for c in string:
        res+=apiEncodeChar(c)

    res = requests.utils.quote(res)
    return res

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

for number in numbers:

    parsedNumber = number.partition(' ')[0]

    
    enc_msgStr = apiEncodeString(parsedNumber)

    req_headers = { 'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8', 'User-Agent' : USER_AGENT, 'Origin' : 'https://parcelsapp.com' }

    req_data = { 'trackingId': enc_msgStr, 'carrier': "Auto-Detect", 'language': "en", 'country': "Auto-Detect", 'platform': "web-desktop", 'wd': "false", 'c': "false", 'p': "2", 'l': "2", 'se': "1" }


    print("{}".format(number))
    print("Making a request...")

    req = requests.post(api_addr, data=req_data, headers=req_headers)

    if not req.ok:
        print("{}Got {} HTTP code{}".format(RED, req.status_code, ENDC))
        raise SystemExit

    if "error" in req.text:
        print("{}Got {} error{}".format(RED, req.json()['error'], ENDC))
        print("(Either your tracking number is invalid, or the API encoding has changed.)") #API access mechanism does change rather frequently :/
        raise SystemExit

    data = req.json()

#    print("{}".format(number))
    print("{} -----------> {}".format(data['origin'], data['destination']))
    print("Status: {}\n".format(data['status']))

    for state in data['states']:
        print("{}{}\t\t{} {}{}\t\t{}".format(BLUE, state['date'], CYAN, data['carriers'][state['carrier']], ENDC, state['status']))

    print() #cosmetic blank line
