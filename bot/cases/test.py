#!/usr/bin/python
import routeros_api
import configparser
import sys

config = configparser.ConfigParser()
config.read("/var/www/avgbot/bot/cases/config.txt")
connection = routeros_api.RouterOsApiPool(sys.argv[1], username=config[sys.argv[2]]['username'], password=config[sys.argv[2]]['password'], plaintext_login=True)
api = connection.get_api()
fw = api.get_resource('/ip/firewall/filter')
fwset = fw.get()
apifw = "8728"
apifwssl = "8729"
for s in fwset:
	try:
		if apifw == s['dst-port'] or apifwssl == s['dst-port']:
			print(s['dst-port'])
	except:
		print('NoDST')
