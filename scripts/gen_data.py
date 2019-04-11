#!/usr/bin/env python3
import random
import socket
import sys
import os
import time

SYSLOGSOCK = None
HOST=os.environ.get("SYSLOG_HOST", None)
PORT=int(os.environ.get("SYSLOG_PORT", -1))

# Data types
callback_sources = ["cobaltstrike", "crowdcontrol", "reclaimer",
         "empire", "anomaly", "blackice", "anomaly-win"]

hosts = ["10.2.x.1",  "10.2.x.2", "10.2.x.3", "10.2.x.4", "10.2.x.5",
         "10.3.x.1", "10.3.x.2", "10.3.x.3"]

exploits = ["belt", "gg", "headshot", "nomnom", "trickshot"]

passes = ["123456", "12345", "123456789", "password", "iloveyou", "princess",
             "1234567", "rockyou", "12345678", "abc123", "nicole", "daniel",
             "babygirl", "monkey", "lovely", "jessica", "654321", "michael",
             "ashley", "qwerty", "111111", "iloveu", "000000", "michelle",
             "tigger", "sunshine", "chocolate", "password1", "soccer", "anthony",
             "friends", "butterfly", "purple", "angel", "jordan", "liverpool",
             "justin", "loveme", "fuckyou", "123123", "football", "secret", "andrea",
             "carlos", "jennifer", "joshua", "bubbles", "1234567890", "superman", "hannah"]

users = ["username", "administrator", "root", "user1", "admin", "alex", "pos", "demo", "hulto", "Admin", "sql"]

creds_sources = ["Reach", "PAM", "LSSAS"]

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


def gen_ip():
    return random.choice(hosts).replace("x", str(random.randint(1, 10)))


def gen_callback():
    typ = random.choice(callback_sources)
    if typ == "reclaimer":
        msg = "Reclaimer exploited with " + random.choice(exploits)
    else:
        msg = "Beacon received to " + typ

    return "{} BOXACCESS {} {}".format(typ, gen_ip(), msg)


def gen_cred():
    src = random.choice(creds_sources)
    if src == "Reach":
        typ = random.choice(["system", "system", "system", "system", "system", "system", "system", "db", "wordpress"])
    else:
        typ = "system"
    return "{} CREDENTIAL {} {} {} {}".format(src, gen_ip(), typ, random.choice(users), random.choice(passes))


def send_count(count):
    # Send just a bunch of data at once
    print("Sending", count, "logs")

    for i in range(count):
        send_syslog(gen_callback())
    for i in range(count//3):
        send_syslog(gen_cred())
    print("Complete.")


def send_timed(count, interval=30):
    """Send a bunch of data every few seconds to simulate actual callback stuff
    count: The max num of intervals to run for
    interval: about how many seconds to wait between sends
    """
    print("Sending data", count, "times at an interval of", interval, "seconds")
    for i in range(count):
        # 50% chance to send 2-5 creds
        if random.random() < 0.50:
            for j in range(random.randint(2, 5)):
                cred = gen_cred()
                print("Sending credential", cred)
                send_syslog(cred)
        # Send a 10-20 beacons every few seconds
        for j in range(random.randint(10,20)):
            callback = gen_callback()
            print("Sending callback", callback)
            send_syslog(callback)
            time.sleep(random.randint(0,3)) # Sleep for 1-3 seconds and then send the next beacon
        st = interval + random.randint(-15, 15)
        print("Sleeping for", st, "seconds. (Iteration {})".format(i))
        time.sleep(st)  # Sleep for interval +- 15 seconds

def main():
    if not HOST or PORT == -1:
        print(HOST, PORT)
        raise ValueError("SYSLOG_HOST and SYSLOG_PORT must be specified in the environment")
    try:
        count = int(sys.argv[1])
    except (IndexError, ValueError) as E:
        count = 100

    try:
        interval = int(sys.argv[2])
        send_timed(count, interval)
    except (IndexError, ValueError) as E:
        send_count(count)


main()


