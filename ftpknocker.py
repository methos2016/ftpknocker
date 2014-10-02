#!/usr/bin/env python3
from argparse import ArgumentParser
import iptools
import ftplib
import threading

argparser = ArgumentParser()
argparser.add_argument('targets', nargs='+')
argparser.add_argument('-t', '--threads',
                        action='store', default=20, type=int, dest='maxThreads', help='number of threads to use')
argparser.add_argument('-w', '--wait',
                        action='store', default=2, type=int, dest='timeout', help='seconds to wait before timeout')
# TODO: add option for specifing a file with hosts
# argparser.add_argument('-f', '--file',
#                        action='store', dest='hostlist', help='optional file with target hosts')
args = argparser.parse_args()

targets = iptools.IpRangeList(*[host for host in args.targets])

def tryFtpConnect(host):
	host = host.strip()
	ftp = ftplib.FTP()
	try:
		ftp.connect(host=host, timeout=args.timeout)
		if '230' in ftp.login():
			print(host + ' OK')
		else:
			print(host + ' DENIED')
	except ftplib.all_errors:
		print(host + ' ERROR')


for target in targets:
	while(threading.activeCount() >= args.maxThreads):
		continue
	threading.Thread(target=tryFtpConnect, args=(target,)).start()
