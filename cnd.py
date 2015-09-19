#!/usr/bin/env python

import subprocess
import re
import getpass
import socket
import os
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

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
    ip_list = {}
    if os.path.isfile("/var/log/auth.log"):
        authlog_f = file("/var/log/auth.log", "r")
        try:
            for line in authlog_f:
                line = line.rstrip()
                match = re.search("Failed password for", line)
                if match:
                    line = line.split(' ')
                    ip = line[-4]
                    if ip_check(ip) == True and ip not in ip_list:
                        ip_list[ip] = line
        except Exception, e:
            print "[!] An error in reading logs"
            print e
    return ip_list
                
def ip_check(ip):            
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def send_email(abuse_email, sender_email, subject, body, password):
    message = MIMEMultipart()
    message['from'] = sender_email
    message['to'] = abuse_email
    message['subject'] = subject
    message.attach(MIMEText(body))
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, sender_email, message.as_string())
    server.quit()


def main():
    if ip_check(sys.argv[1]) == False:
        print "[+] Error: Bad IP address, exiting..."
        exit()
    ip_list = ssh_monitor()
    print ip_list
    print '[+] Sending to whois'
    abuse_email = whois_lookup(sys.argv[1])
    password = getpass.getpass()
    sender_email = raw_input("Sender email: ")

    #subject and body are going to be assigned by log parsing
    send_email(abuse_email, sender_email, subject, body, password)


if __name__ == '__main__':
    main()
