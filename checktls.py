#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import *
from dns import resolver

def get_mx(domain):
    mxes = [x.to_text().split()[1][:-1] for x in resolver.query(domain, 'MX')]
    return mxes

domains = ('finkenberger.org', 'gmx.de', 'web.de', 'hotmail.com', 'yahoo.com',
           'aol.com', 'gmail.com', 't-online.de')

tls_supported = []
tls_not_supported = []

for domain in domains:
    domain_mx = get_mx(domain)[0]
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((domain_mx, 25))
        recv = client_socket.recv(1024)
        client_socket.send('EHLO example.com\r\n')
        recv1 = client_socket.recv(1024)
        if 'STARTTLS' in recv1:
            tls_supported.append(domain)
            print domain, domain_mx, "unterstützt"
        else:
            tls_not_supported.append(domain)
            print domain, domain_mx, "NICHT unterstützt"
    except error, msg:
        print domain, domain_mx, 'FEHLER:', msg


print
print "TLS wird unterstützt von", len(tls_supported), "Servern"
print "TLS wird NICHT unterstützt von", len(tls_not_supported), "Servern"

