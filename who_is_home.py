#!/usr/bin/python

# For arp-scan
import subprocess
# For filtering out MAC addresses
import re
# For handling stored client info
from xml.dom.minidom import parse
import xml.dom.minidom
import os.path

# arp-scan configuration
arpscan = "arp-scan"
localnet = "--localnet"
timeout = "--timeout"
retry = "--retry"

timeout_val = "100" # ms
retry_val = "5"

# XML configuration
XML_VLIENTS_FILE = "clients.xml"
# Create clients file if not exists
if not os.path.isfile("clients.xml"):
	xml_clients = open(XML_VLIENTS_FILE , 'w')
	xml_clients.write("<clientlist>\n</clientlist>")
	xml_clients.close()

# Open client database
DOMTree = xml.dom.minidom.parse("clients.xml")
clientlist = DOMTree.documentElement


p = subprocess.Popen(["sudo", arpscan, localnet, timeout, timeout_val, retry, retry_val], stdout=subprocess.PIPE)
output, err = p.communicate()

result = re.findall("((?:[0-9a-f]{2}:?){6})", output);
print result
for macaddr in result:
	print macaddr;

# Get all clients
clients = clientlist.getElementsByTagName("client")

# Print detail of each client.
for client in clients:
	print "*****client*****"

	name = client.getElementsByTagName('name')[0]
	category = client.getElementsByTagName('category')[0]
	status = client.getElementsByTagName('status')[0]
	MAC = client.getElementsByTagName('MAC')[0]
	
	MAC_str = MAC.childNodes[0].data.lower()

	if MAC_str in output:
		status = "In"
	else:
		status = "out"

	print "Name: %s" % name.childNodes[0].data
	print "category: %s" % category.childNodes[0].data
	print "status: %s" % status
	print "MAC: %s" % MAC.childNodes[0].data

print output


