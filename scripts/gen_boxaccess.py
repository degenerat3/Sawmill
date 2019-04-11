#!/usr/bin/env python3
import random
import socket
import sys
import os

SYSLOGSOCK = None
HOST=os.environ.get("SYSLOG_HOST", None)
PORT=int(os.environ.get("SYSLOG_PORT", -1))

def send_syslog(string):
    """Send a syslog to the server. Make sure the port is open though
    """
    global SYSLOGSOCK
    if not SYSLOGSOCK:
        print("Creating socket to", HOST, PORT)
        SYSLOGSOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SYSLOGSOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SYSLOGSOCK.connect((HOST, PORT))
    string = string.rstrip() + "\n"
    SYSLOGSOCK.sendall(string.encode())


def gen_callback():
    types = ["cobaltstrike", "crowdcontrol", "reclaimer",
             "empire", "anomaly", "blackice", "anomaly-win"]

    hosts = ["10.2.x.1",  "10.2.x.2", "10.2.x.3", "10.2.x.4", "10.2.x.5",
             "10.3.x.1", "10.3.x.2", "10.3.x.3"]

    exploits = ["belt", "gg", "headshot", "nomnom", "trickshot"]

    ip = random.choice(hosts).replace("x", str(random.randint(1, 10)))

    typ = random.choice(types)
    if typ == "reclaimer":
        msg = "Reclaimer exploited with " + random.choice(exploits)
    else:
        msg = "Beacon received to " + typ

    return "{} BOXACCESS {} {}\n".format(typ, ip, msg)

def main():
    if not HOST or PORT == -1:
        print(HOST, PORT)
        raise ValueError("SYSLOG_HOST and SYSLOG_PORT must be specified in the environment")
    try:
        count = int(sys.argv[1])
    except (IndexError, ValueError) as E:
        count = 100
    print("Sending", count, "logs")
    for i in range(count):
        send_syslog(gen_callback().rstrip())
    print("Complete.")

main()
