#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import *
from dns import resolver
import smtplib


domains = ('gmx.de', 'web.de', 'hotmail.com', 'yahoo.com',
           'aol.com', 'gmail.com', 't-online.de')

def get_mx_servers_by_priority(domain):
    # returns list of mx servers sorted by priority
    try:
        mx_records = [x.to_text().split() for x in resolver.query(domain, 'MX')]
        mx_records.sort() 
        servers_by_priority = [record[1][:-1] for record in mx_records]
        return servers_by_priority
    except (resolver.NoAnswer, resolver.NXDOMAIN, resolver.Timeout):
        return None 

def check_mx_tls(domain_mx):
    try:
	smtp = smtplib.SMTP(domain_mx)
        smtp.ehlo()
	result = smtp.has_extn('STARTTLS')
	smtp.quit()
	return result
    except Exception:
	return None

tls_supported = []
tls_not_supported = []

for domain in domains:
    domain_mx = get_mx(domain)[0]
    if check_mx_tls(domain_mx):
        print domain, domain_mx, "TLS"
    else:
        print domain, domain_mx

