#!/usr/bin/env python

import subprocess
import socket
import os
import sys

# Lookup the abuse reporting email for that IP using whois
def whois_lookup(ip):
    command = 'whois %s' % ip
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    cmd_output = process.communicate()

    for item in cmd_output[0].split('\n'):
        if 'OrgAbuseEmail' in item:
            abuse_email = item.strip().split()
    return abuse_email[1]


# Monitor SSH for brute force attempts, pass offenders to whois_lookup()
def ssh_monitor():
    if os.path.isfile("/var/log/auth.log"):
        authlog_f = file("/var/log/auth.log", "r")
    
                
def ip_check(ip):            
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def main():
    if ip_check(sys.argv[1]) == False:
        print "[+] Error: Bad IP address, exiting..."
        exit()
    print '[+] Sending to whois'
    email = whois_lookup(sys.argv[1])
    print '[+] Abuse email is: ' + email


if __name__ == '__main__':
    main()
