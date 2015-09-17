#!/usr/bin/env python

import subprocess
import sys
print sys.argv[1]
command = 'whois %s' % (sys.argv[1])
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output = process.communicate()

#Pull the abuse email out so we can bitch
for item in output[0].split('\n'):
    if 'OrgAbuseEmail' in item:
        abuse_email = item.strip().split()
print abuse_email[1]
