import winrm
import configparser

def action(trg):
	config = configparser.ConfigParser()
	config.read("/var/www/avgbot/bot/cases/config.txt")
	session = winrm.Session(trg.ip, auth = (config[trg.cred]['username'],config[trg.cred]['password']), transport='ntlm')
	cmd1 = 'get-service %s | select Status' % trg.service
	cmd2 = 'start-service %s' % trg.service
	status = session.run_ps(cmd1)
	result = 0

	if b'Stopped' in status.std_out:
		session.run_ps(cmd2)
		result = 2
	if b'Running' in status.std_out:
		result = 1
	return result
