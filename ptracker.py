#!/usr/bin/python3

import requests as req
import sys
from os import path

API_BASE_URL = "https://api.ordertracker.com"
API_REFERENCE_URL = "public/trackinglinks"

class OUTPUT_COLORS:
    NONE    = "\033[0m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    CYAN    = "\033[96m"
    GRAY    = "\033[97m"

def perr(msg):
    print(f"{OUTPUT_COLORS.RED}ERROR: {msg}{OUTPUT_COLORS.NONE}")

def getTrackingLink(trackingNumber):
    r = req.get(f"{API_BASE_URL}/{API_REFERENCE_URL}?trackingstring={trackingNumber}")

    if not r.ok:
        return False

    return r.json()[0]['link']

def getTrackingInfo(link):

    r = req.get(link)

    if not r.ok:
        return False

    return r.json()

def outputTrackingInfo(trackingNumber, parcelStatus, shippingInfo, daysInTransit, comment):

    print(f"Tracking Number : {OUTPUT_COLORS.CYAN}{trackingNumber}{OUTPUT_COLORS.NONE}", end="")
    if comment:                     #if there was a comment in the inputFile, include it here
        print(f" - {OUTPUT_COLORS.GRAY}{comment}{OUTPUT_COLORS.NONE}")
    else:
        print()
    print(f"Status : ", end="")
    if parcelStatus == "shipped":
        print(f"{OUTPUT_COLORS.GREEN}", end="")
    print(f"{parcelStatus}{OUTPUT_COLORS.NONE}")
    print(f"{daysInTransit} days in transit")

    for i in shippingInfo:
        print(f"{i['time']} : {i['courier']['name']} - {i['lines'][0]}")

def main():

    #input parsing

    if len(sys.argv) != 2:
        perr("The script should be called with exactly 1 argument, being a Universal Tracking Number, or a path to a file with one such number per line")
        sys.exit(1)

    numbers = list()

    #check if argv[1] is a file path
    if path.exists(sys.argv[1]):
        try:
            with open(sys.argv[1], "r") as inputFile:
                numbers = inputFile.readlines()
        except FileNotFoundError:
            perr(f"Could not open {sys.argv[1]} for reading")
            sys.exit(1)

    #must be a tracking number then
    else:
        numbers.append(sys.argv[1])

    print("Making requests now, please be patient ^^")

    for line in numbers:

        line = line.strip()
        p = line.partition(' ')
        n = p[0]
        if len(p) > 2:
            description = p[2]
        else:
            description = None

        link = getTrackingLink(n)
        if not link:
            perr(f"Could not get a tracking link for the number : {n}")
            perr("The API could be blocking frequent requests")
            continue
        data = getTrackingInfo(link)
        if not data:
            perr(f"Could not get tracking info for the number : {n}")
            perr("The API could be blocking frequent requests")
            continue
        try:
            number = data['number']
            status = data['status']
            steps = data['steps']
            dit = data['daysInTransit']
        except KeyError:
            perr("Could not interpret tracking info correctly for the number : {n}")
            continue
        outputTrackingInfo(number, status, steps, dit, description)
        print() # cosmetic separator

main()
