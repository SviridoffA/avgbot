import winrm
import configparser

def action(trg):
	config = configparser.ConfigParser()
	config.read("/var/www/avgbot/bot/cases/config.txt")
	result = 1
	session = winrm.Session(trg.ip, auth = (config[trg.cred]['username'],config[trg.cred]['password']), transport='ntlm')
	cmd = 'shutdown /s /f /t 0'
	try:
		session.run_cmd(cmd)
		result = 2
	except:
		result = 1
	return result
