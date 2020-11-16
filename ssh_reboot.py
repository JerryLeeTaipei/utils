#!/usr/bin/python3


import subprocess
import sys
import time
import fcntl
import syslog
import random

##########
# upload #
##########

def ssh_reboot(dst_account):	
	# 1. tag uploading
	cmd = [ '/usr/bin/ssh', dst_account, 'sudo', 'reboot']
	proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	(output, error) = proc.communicate()
	if len(error.decode()) != 0:
		print("invalid cmd:", cmd )
		print("error:", error.decode())
		return 1
	print("output:", output.decode())
	return 0

def ping():
	cmd = [ '/bin/ping', '-c', '1', '192.168.101.224']
	proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	(output, error) = proc.communicate()
	if len(error.decode()) != 0:
		print("error:", error.decode())
	else:
		result = output.decode()
		if ( result.find(', 0% packet loss,') != -1 ):
			print('contacted')
			return 0
		else:
			print('Not alive')
			return 1
########
# main #
########

if ( __name__ == '__main__' ):
	syslog.syslog("ssh_reboot.py:")
	dst_account = 'jerry-lee-tpe@192.168.101.182'
	count = 0
	while ( 1 ):
		if ( ping() == 0  ):
			syslog.syslog("ssh_reboot.py: to reboot")
			ssh_reboot(dst_account)
			count = count +1 
			print('rebooted: ', count)
			syslog.syslog("rebooted: ")
			timeout = random.randrange(60, 600)
			print('wait ', timeout)
			time.sleep(timeout)
		else:
			syslog.syslog("ssh_reboot.py: remote is not ready")
		time.sleep(10)
	#end of while


