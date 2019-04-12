#!/usr/bin/env python3

# Build lookup tables for a given topology
# Topologies are generated from https://github.com/RITRedteam/Topology-Generator

import json
import sys

def get_hosts(data):
    hosts = []
    for network in data['networks']:
        netip = network['ip']
        for nethost in network['hosts']:
            host = nethost.copy()
            if nethost['ip'].lower() == "dhcp":
                host['ip'] = "dhcp"
            else:
                host['ip'] = ".".join((netip, nethost['ip']))
            hosts += [host]
    return hosts


def build_teams_lookup(data):
    team_regex = set()
    # Get the network IPs from the data
    for network in data['networks']:
        base_regex = []
        ip = network['ip'].lower().split(".")
        # Build the new ip with digit regexs for unknown numbers
        for octet in ip:
            if octet == "x":
                base_regex += ["x"]
            elif octet == "0":
                base_regex += ["\\d+"]
            else:
                base_regex += [octet]
        # Pad short octets with any digit
        base_regex += ['\\d+'] * (4 - len(base_regex))
        team_regex.add(".".join(base_regex))
    
    result = {}
    # For each team and each regex, build a term for the output dictionary
    for regex in team_regex:
        for team in data['teams']:
            result[regex.replace("x", str(team))] = "Team"+str(team)
    
    return json.dumps(result, indent=2, sort_keys=True)

def build_os_lookup(data):
    result = {}
    for host in get_hosts(data):
        regex = host['ip'].replace("x", "\\d+")
        if host['ip'].lower() == "dhcp":
            continue

        result[regex] = host['os']
    return json.dumps(result, indent=2, sort_keys=True)
    

def main():
    with open(sys.argv[1]) as fil:
        data = json.load(fil)
    with open("/tmp/host_os.json", 'w') as fil:
        fil.write(build_os_lookup(data)+"\n")
    with open("/tmp/host_team.json", 'w') as fil:
        fil.write(build_teams_lookup(data)+"\n")
    print("Lookups written to /tmp/host_os.json and /tmp/host_team.json")

if __name__ == "__main__":
    main()