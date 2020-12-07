#!/usr/bin/env python

import socket, re
from ipaddress import IPv4Network

net = IPv4Network("192.168.3.0/24")

for addr in net:
	try:
		print(socket.gethostbyaddr(str(addr))[0])
		print(socket.gethostbyaddr(str(addr))[2])
		print(" ")
		print("*"*30)
	except:
		pass


