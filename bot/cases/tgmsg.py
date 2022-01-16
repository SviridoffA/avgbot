#!/usr/bin/python
import subprocess

def action(trg):
	subprocess.call("/var/www/avgbot/bot/cases/tgmsg.sh 'TEST' 'ACTION'", shell=True)
	return 2
