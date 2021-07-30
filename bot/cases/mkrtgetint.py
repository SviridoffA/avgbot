#!/usr/bin/python
import routeros_api
import configparser
import sys

ip = sys.argv[1]
conf = sys.argv[2]
vpntype = sys.argv[3]

config = configparser.ConfigParser()
config.read("/var/www/avgbot/bot/cases/config.txt")
connection = routeros_api.RouterOsApiPool(ip, 
username=config[conf]['username'], password=config[conf]['password'], plaintext_login=True)
api = connection.get_api()
vpn = api.get_resource('/interface/' + vpntype)
result = 0
for i in vpn.get():
	print(i['id'] + ' - ' + i['name'])
