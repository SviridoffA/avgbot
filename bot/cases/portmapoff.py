#!/usr/bin/python
import paramiko

def action(trg):
	ipport = trg.ip + ':'
	key = paramiko.RSAKey.from_private_key_file("/var/www/avgbot/avgbot/id_rsa")
	c = paramiko.SSHClient()
	c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	c.connect( hostname = "gw.dc-01.ru", port = 45623, username = "root", pkey = key )
	cmd = '/root/scripts/ruleoff.py %s' % ipport
	stdin, stdout, stderr = c.exec_command(cmd)
	result = stdout.read()
	c.exec_command('/usr/bin/ansible-playbook /etc/ansible/iptables_rules.yml')
	c.close
	return result
