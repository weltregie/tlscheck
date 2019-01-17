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

result_table=[]
result_tls_supported = []
result_tls_not_supported = []

for domain in domains:
    domain_mx_servers = get_mx_servers_by_priority(domain)
    if domain_mx_servers:
        for mx_server in domain_mx_servers:
            result_list = [domain]     # first element of list: domain
	    result_list.append(mx_server)
	    tls_result = check_mx_tls(mx_server)
            if tls_result:
                result_list.append('TLS supported')
                result_tls_supported.append(domain)
                break
            if tls_result == False:
                result_list.append('TLS not supported')
                result_tls_not_supported.append(domain)
		break
            if tls_result == None:
                result_list.append('no answer')
        result_table.append(result_list)
        print result_list[0].ljust(22), result_list[1].ljust(37), result_list[2].ljust(20)
