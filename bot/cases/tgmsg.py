#!/usr/bin/python
import subprocess

def action():
	subprocess.call("/var/www/avgbot/bot/cases/tgmsg.sh 'ANTIBRUTE' 'IP banned'", shell=True)
	pass
