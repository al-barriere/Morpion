#!/usr/bin/env python3
import socket
import select
import threading
import sys

l = []
clientAddr = []
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.connect((sys.argv[1],7777))
s.send(b"Connected")
while True:
    pass
s.close()
