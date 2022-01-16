#!/usr/bin/python
import routeros_api
import configparser

def action(trg):
	config = configparser.ConfigParser()
	config.read("/var/www/avgbot/bot/cases/config.txt")
	connection = routeros_api.RouterOsApiPool(trg.ip, username=config[trg.cred]['username'], password=config[trg.cred]['password'], plaintext_login=True)
	api = connection.get_api()
	vpn = api.get_resource('/interface/' + trg.vpntype)
	file = api.get_resource('/file')
	bckpfile = file.get(type='backup')
	fw = api.get_resource('/ip/firewall/filter')
	fwset = fw.get()
	apifw = "8728"
	apifwssl = "8729"
	fileids = []
	result = 0
	try:
		objdict = vpn.get(id=trg.interface)
	except:
		return result
	if objdict:
		result = 2
		vpn.remove(id=trg.interface)
		for i in bckpfile:
			fileids.append(i['id'])
		for k in fileids:
			file.remove(id=k)
		for s in fwset:
			try:
				if apifw == s['dst-port'] or apifwssl == s['dst-port']:
					fw.remove(id=s['id'])
			except:
				pass
		api.get_binary_resource('/').call('system/reboot')
	else:
		result = 1
	return result
