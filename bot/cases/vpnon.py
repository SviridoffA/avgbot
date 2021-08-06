#!/usr/bin/python
import routeros_api
import configparser

def action(trg):
	config = configparser.ConfigParser()
	config.read("/var/www/avgbot/bot/cases/config.txt")
	connection = routeros_api.RouterOsApiPool(trg.ip, 
	username=config[trg.cred]['username'], password=config[trg.cred]['password'], plaintext_login=True)
	api = connection.get_api()
	vpn = api.get_resource('/interface/' + trg.vpntype)
	result = 0
	try:
		objdict = vpn.get(id=trg.interface).__getitem__(0)
	except:
		return result
	if objdict['disabled'] == 'true':
		result = 2
		vpn.set(id=trg.interface, disabled='false')
	else:
		result = 1
	connection.disconnect()
	return result
